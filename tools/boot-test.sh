#!/usr/bin/env bash
# Boot a Devium ISO in a virtual machine and check that it reaches the desktop.
#   tools/boot-test.sh ISO [seconds]
# Exit 0 = reached the desktop. Writes ISO.boot.log (the boot messages) and ISO.boot.png (a screenshot).
# Needs: qemu-system-x86_64, bsdtar, socat (and /dev/kvm to be fast).
set -uo pipefail
iso=${1:?usage: boot-test.sh ISO [seconds]}
limit=${2:-480}
name=$(basename "$iso" .iso)
log="$PWD/$name.boot.log"; shot="$PWD/$name.boot.png"
work=$(mktemp -d); qpid=""
trap 'kill "$qpid" 2>/dev/null; rm -rf "$work"' EXIT

# the kernel, initramfs and the live system's boot options, straight from the ISO
bsdtar -xf "$iso" -C "$work" arch/boot boot/syslinux 2>/dev/null
kernel=$(ls "$work"/arch/boot/x86_64/vmlinuz-* 2>/dev/null | head -1)
initrd=$(ls "$work"/arch/boot/x86_64/initramfs-*.img 2>/dev/null | grep -v fallback | head -1)
params=$(grep -rhoE 'archisobasedir=[^ ]+ archisosearchuuid=[^ ]+' "$work/boot/syslinux" 2>/dev/null | head -1)
[[ -f $kernel && -f $initrd && -n $params ]] || { echo "Couldn't read the boot files from $iso"; exit 2; }
echo "Booting $name: $params"

kvm=(); [[ -w /dev/kvm ]] && kvm=(-enable-kvm -cpu host)
qemu-system-x86_64 "${kvm[@]}" -m 4096 -smp 2 -machine q35 -vga virtio -display none \
    -cdrom "$iso" -kernel "$kernel" -initrd "$initrd" \
    -append "$params console=tty0 console=ttyS0,115200 systemd.show_status=1" \
    -serial file:"$log" -monitor unix:"$work/mon",server,nowait -no-reboot &
qpid=$!

screenshot() {
    echo "screendump $work/screen.ppm" | socat - UNIX-CONNECT:"$work/mon" >/dev/null 2>&1
    sleep 2
    if [[ -s $work/screen.ppm ]]; then
        if command -v convert >/dev/null; then convert "$work/screen.ppm" "$shot"; else cp "$work/screen.ppm" "${shot%.png}.ppm"; fi
    fi
}

result=1 start=$SECONDS
while (( SECONDS - start < limit )); do
    sleep 5
    kill -0 "$qpid" 2>/dev/null || { echo "The virtual machine stopped early."; break; }
    if grep -qE 'Kernel panic|emergency mode|Entering emergency|Failed to mount live' "$log" 2>/dev/null; then
        echo "Boot failed:"; grep -m3 -E 'Kernel panic|emergency|Failed to mount' "$log"; break
    fi
    if grep -q 'Reached target.*Graphical Interface' "$log" 2>/dev/null; then
        echo "Reached the desktop target after $((SECONDS - start)) s; waiting for the desktop to draw..."
        sleep 75
        result=0; break
    fi
done
(( result )) && (( SECONDS - start >= limit )) && echo "Timed out after $limit s."
screenshot
failed=$(grep -E 'Failed to start' "$log" 2>/dev/null | sed 's/.*Failed to start //' | sort -u)
[[ -n $failed ]] && { echo "Services that failed to start:"; echo "$failed" | sed 's/^/  - /'; }
echo "Log: $log"; [[ -f $shot ]] && echo "Screenshot: $shot"
exit $result
