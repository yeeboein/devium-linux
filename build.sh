#!/usr/bin/env bash
# Build the Devium ISO. Run on Arch Linux (or in an archlinux container) as root:
#
#   sudo ./build.sh                    build the KDE Plasma edition into ./out
#   sudo EDITION=xfce ./build.sh       build the lighter Xfce edition
#   sudo ./build.sh --clean            remove the old work directory first
#
# Needs: archiso, git (installed automatically if missing).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${WORK_DIR:-$HERE/work}"
OUT="${OUT_DIR:-$HERE/out}"
STAGE="$WORK/profile"
EDITION="${EDITION:-kdeplasma}"
case "$EDITION" in
    kdeplasma|xfce) ;;
    *) echo "Unknown EDITION '$EDITION' (use kdeplasma or xfce)"; exit 1 ;;
esac

say()  { printf '\033[1;36m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33mwarning:\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31merror:\033[0m %s\n' "$*"; exit 1; }

[[ $EUID -eq 0 ]] || die "Run as root: sudo ./build.sh"
command -v pacman >/dev/null || die "This must run on Arch Linux (or an archlinux container)."

if [[ ${1:-} == --clean ]]; then
    say "Removing old work directory"
    rm -rf "$WORK"
fi

say "Installing build tools"
pacman -Sy --needed --noconfirm archiso git base-devel >/dev/null

# 1. Fresh copy of the profile, so the repo itself is never modified.
say "Preparing profile in $STAGE"
rm -rf "$STAGE"
mkdir -p "$STAGE" "$OUT"
cp -a "$HERE/profile/." "$STAGE/"
say "Edition: $EDITION"
# Package list for this edition: Xfce drops the "#kde" lines and adds its own desktop.
SRC_LIST="$WORK/packages.$EDITION"
if [[ $EDITION == xfce ]]; then
    grep -v '#kde' "$HERE/profile/packages.x86_64" > "$SRC_LIST"
    cat "$HERE/editions/xfce/packages.x86_64" >> "$SRC_LIST"
    cp -a "$HERE/editions/xfce/airootfs/." "$STAGE/airootfs/"
    # KDE-only files are harmless on Xfce, but drop the KDE desktop layout and login theme.
    rm -rf "$STAGE/airootfs/usr/share/plasma" "$STAGE/airootfs/usr/share/sddm" "$STAGE/airootfs/etc/sddm.conf.d"
    sed -i 's/^iso_application=.*/iso_application="Devium Xfce Live"/' "$STAGE/profiledef.sh"
else
    cp "$HERE/profile/packages.x86_64" "$SRC_LIST"
fi

# 2. Drop packages that don't exist (anymore), instead of failing the whole build.
say "Checking package list"
pacman -Sy >/dev/null
: > "$STAGE/packages.x86_64"
missing=()
while read -r pkg; do
    [[ $pkg == *"#install"* ]] && continue    # installed systems only, not on the ISO
    pkg="${pkg%%#*}"; pkg="${pkg//[[:space:]]/}"
    [[ -z $pkg ]] && continue
    if pacman -Si "$pkg" >/dev/null 2>&1 || pacman -Sg "$pkg" >/dev/null 2>&1; then
        echo "$pkg" >> "$STAGE/packages.x86_64"
    else
        missing+=("$pkg")
    fi
done < "$SRC_LIST"
if (( ${#missing[@]} )); then
    warn "Skipping packages not found in the repos: ${missing[*]}"
fi
desktop_must="plasma-desktop sddm"; [[ $EDITION == xfce ]] && desktop_must="xfce4-session lightdm"
for must in base linux mkinitcpio-archiso $desktop_must; do
    grep -qx "$must" "$STAGE/packages.x86_64" || die "Required package '$must' is missing."
done

# Package list for installed systems (live-ISO-only packages removed).
# Lines tagged "#live" are left out: users pick those in the Devium Setup wizard.
sed -n '/#live/!{s/#.*//;s/[[:space:]]//g;/./p}' "$SRC_LIST" \
    | grep -vxE 'mkinitcpio-archiso|syslinux|memtest86\+|memtest86\+-efi|edk2-shell|archinstall' \
    | while read -r p; do
        if pacman -Si "$p" >/dev/null 2>&1 || pacman -Sg "$p" >/dev/null 2>&1; then echo "$p"
        else echo "warning: install list: skipping missing package $p" >&2; fi
    done > "$STAGE/airootfs/usr/share/devium/install-packages.txt"
say "Installed systems get $(wc -l < "$STAGE/airootfs/usr/share/devium/install-packages.txt") packages (live ISO: $(wc -l < "$STAGE/packages.x86_64"))"

# 3. Bundle ArchPill (https://github.com/yeeboein/archpill).
say "Downloading ArchPill"
mkdir -p "$STAGE/airootfs/opt"
git clone --depth 1 https://github.com/yeeboein/archpill.git "$STAGE/airootfs/opt/archpill" \
    || warn "Could not download ArchPill now; it will be downloaded on first boot with internet."

# 3b. Bundle KDElite (https://github.com/yeeboein/kdelite) for the "KDE Lite" choice.
say "Downloading KDElite"
git clone --depth 1 https://github.com/yeeboein/kdelite.git "$STAGE/airootfs/opt/kdelite" \
    || warn "Could not download KDElite; the KDE Lite option will be hidden."

# 3c. Bundle linux-magnify (https://github.com/yeeboein/linux-magnify), the macOS-style dock option.
say "Downloading linux-magnify"
git clone --depth 1 https://github.com/yeeboein/linux-magnify.git "$STAGE/airootfs/opt/linux-magnify" \
    || warn "Could not download linux-magnify; the Magnify dock option will be hidden."

# 4. Release info (used by the installer to fetch Devium's files for the new system).
repo_url="https://github.com/yeeboein/devium-linux"
repo_ref="$(git -C "$HERE" rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
[[ $repo_ref == HEAD ]] && repo_ref=main
cat > "$STAGE/airootfs/etc/devium-release" <<EOF
DEVIUM_VERSION=${DEVIUM_VERSION:-$(date +%Y.%m.%d)}
DEVIUM_REPO=${DEVIUM_REPO:-$repo_url}
DEVIUM_REF=${DEVIUM_REF:-$repo_ref}
DEVIUM_EDITION=$EDITION
EOF

# 4a. Report a problem (Devium Tools) sends to a Discord webhook. The URL is a GitHub secret
#     (DEVIUM_REPORT_WEBHOOK), never stored in the repository. Without it, reports open a GitHub issue.
mkdir -p "$STAGE/airootfs/etc/devium"
if [[ ${DEVIUM_REPORT_WEBHOOK:-} == https://discord.com/api/webhooks/* ]]; then
    printf '%s\n' "$DEVIUM_REPORT_WEBHOOK" > "$STAGE/airootfs/etc/devium/report-webhook"
    say "Problem reports go to Discord"
fi
if [[ ${DEVIUM_DISCORD_INVITE:-} == https://discord.* ]]; then
    printf '%s\n' "$DEVIUM_DISCORD_INVITE" > "$STAGE/airootfs/etc/devium/discord-invite"
fi

# 4b. Build the point-and-click installer (Calamares) from the AUR into Devium's local repo.
build_aur() {   # build_aur <package>: build as an unprivileged user, install it, keep the package
    local name="$1" dir="$WORK/aur/$1" cache="$HERE/.aur-cache"
    mkdir -p "$cache"
    if compgen -G "$cache/$name-[0-9]*.pkg.tar.zst" >/dev/null; then   # built earlier in this run
        pacman -U --noconfirm --needed "$cache/$name"-[0-9]*.pkg.tar.zst >/dev/null
        cp "$cache/$name"-[0-9]*.pkg.tar.zst "$STAGE/airootfs/opt/devium-repo/"
        return 0
    fi
    rm -rf "$dir"; mkdir -p "$WORK/aur"
    git clone --depth 1 "https://aur.archlinux.org/$name.git" "$dir" || return 1
    chown -R devbuild: "$WORK/aur"
    su devbuild -c "cd '$dir' && makepkg -s --noconfirm --needed" || return 1
    pacman -U --noconfirm --needed "$dir"/*.pkg.tar.zst >/dev/null
    cp "$dir"/*.pkg.tar.zst "$STAGE/airootfs/opt/devium-repo/"
    cp "$dir"/*.pkg.tar.zst "$cache/"
}
id devbuild >/dev/null 2>&1 || useradd -m devbuild
echo "devbuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/devbuild
mkdir -p "$STAGE/airootfs/opt/devium-repo"
CALAMARES=0
if [[ ${DEVIUM_NO_CALAMARES:-0} != 1 ]]; then
    say "Building the Devium installer (Calamares) - this takes a while"
    if build_aur ckbcomp && build_aur calamares; then
        CALAMARES=1
    else
        warn "Could not build Calamares; the ISO will use the text installer instead."
    fi
fi

# 5. Package Devium's files as "devium-desktop" in a small repo on the ISO, so the installer
#    copies them onto the new system straight from the ISO (no internet or GitHub needed).
say "Packaging devium-desktop"
PKG="$WORK/devium-desktop"
[[ -n $WORK && $PKG == */devium-desktop ]] || die "bad work directory"
rm -rf "$PKG"; mkdir -p "$PKG/root"
tar -C "$STAGE/airootfs" \
    --exclude=./etc/shadow --exclude=./etc/passwd --exclude=./etc/hostname \
    --exclude=./etc/localtime --exclude=./etc/locale.conf \
    --exclude=./etc/mkinitcpio.conf.d --exclude=./etc/sudoers.d \
    --exclude=./etc/polkit-1 --exclude=./etc/sddm.conf.d/20-devium-live-autologin.conf \
    --exclude=./etc/lightdm/lightdm.conf.d/20-devium-live-autologin.conf --exclude=./usr/share/devium/xfce/live \
    --exclude=./etc/udev/rules.d/90-devium-live-quiet-disks.rules \
    --exclude=./etc/systemd/journald.conf.d/volatile-storage.conf --exclude=./etc/systemd/logind.conf.d \
    --exclude=./etc/systemd/system/etc-pacman.d-gnupg.mount --exclude=./etc/systemd/system/pacman-init.service \
    --exclude=./etc/systemd/system/multi-user.target.wants --exclude=./root \
    --exclude=./etc/pacman.d/hooks/zz-devium-live-setup.hook \
    --exclude=./etc/pacman.d/hooks/zzzz99-remove-custom-hooks-from-airootfs.hook \
    --exclude=./etc/pacman.d/hooks/uncomment-mirrors.hook \
    --exclude=./usr/share/applications/devium-install.desktop \
    --exclude=./usr/share/applications/devium-about-live.desktop \
    --exclude=./opt/devium-repo --exclude='*/.git' --exclude=./etc/calamares \
    -cf - . | tar -C "$PKG/root" -xf -
# Files other packages own go to overrides/ (devium-setup copies them into place).
for f in etc/skel/.bashrc etc/skel/.bash_profile etc/default/useradd etc/plymouth/plymouthd.conf \
         etc/lightdm/lightdm-gtk-greeter.conf; do
    if [[ -f $PKG/root/$f ]]; then
        mkdir -p "$PKG/root/usr/share/devium/overrides/$(dirname "$f")"
        mv "$PKG/root/$f" "$PKG/root/usr/share/devium/overrides/$f"
    fi
done
pkgver="$(sed -n 's/^DEVIUM_VERSION=//p' "$STAGE/airootfs/etc/devium-release" | tr -c 'a-zA-Z0-9.\n' '.')"
{
    echo "pkgname=devium-desktop"
    echo "pkgver=${pkgver:-1}"
    echo "pkgrel=1"
    echo "pkgdesc=\"Devium's apps, look and settings\""
    echo "arch=(any)"
    echo "url=\"https://github.com/yeeboein/devium-linux\""
    echo "license=(MIT)"
    echo "depends=(bash python python-pyqt6)"
    echo "install=devium.install"
    echo "options=(!strip !debug)"
    echo 'package() { cp -a "$startdir/root/." "$pkgdir/"; }'
} > "$PKG/PKGBUILD"
{
    echo 'post_install() { /usr/lib/devium/devium-setup --package; }'
    echo 'post_upgrade() { post_install; }'
} > "$PKG/devium.install"
chown -R devbuild: "$PKG"
su devbuild -c "cd '$PKG' && makepkg -f --nodeps --noconfirm" >/dev/null || die "Could not package devium-desktop"
cp "$PKG"/devium-desktop-*.pkg.tar.zst "$STAGE/airootfs/opt/devium-repo/"
repo-add -q "$STAGE/airootfs/opt/devium-repo/devium.db.tar.gz" "$STAGE"/airootfs/opt/devium-repo/*.pkg.tar.zst
echo devium-desktop >> "$STAGE/airootfs/usr/share/devium/install-packages.txt"

# The installer's packages step: everything an installed system needs (most is already on the
# ISO; the rest is downloaded), minus the live-only tools.
if (( CALAMARES )); then
    {
        echo "backend: pacman"
        echo "skip_if_no_internet: false"
        echo "update_db: true"
        echo "update_system: false"
        echo "pacman:"
        echo "    num_retries: 3"
        echo "    disable_download_timeout: false"
        echo "    needed_only: true"
        echo "operations:"
        echo "  - install:"
        grep -vx 'devium-desktop' "$STAGE/airootfs/usr/share/devium/install-packages.txt" | sed 's/^/      - /'
        echo "      - grub"
        echo "      - os-prober"
    } > "$STAGE/airootfs/etc/calamares/modules/packages.conf"
    if [[ $EDITION == xfce ]]; then
        sed -i 's/- sddm/- lightdm/' "$STAGE/airootfs/etc/calamares/modules/displaymanager.conf"
        sed -i 's/name: sddm/name: lightdm/' "$STAGE/airootfs/etc/calamares/modules/services-systemd.conf"
    fi
    # live ISO packages: the installer itself (from the local repo)
    printf 'calamares\nckbcomp\n' >> "$STAGE/packages.x86_64"
    sed -i 's/^DEVIUM_INSTALLER=.*//' "$STAGE/airootfs/etc/devium-release"
    echo "DEVIUM_INSTALLER=calamares" >> "$STAGE/airootfs/etc/devium-release"
else
    rm -rf "$STAGE/airootfs/etc/calamares"
fi
# mkarchiso installs the live packages with the profile's pacman.conf: add the local repo.
printf '\n[devium]\nSigLevel = Optional TrustAll\nServer = file://%s\n' "$STAGE/airootfs/opt/devium-repo" >> "$STAGE/pacman.conf"

# 6. Build.
say "Building the ISO (this takes a while)"
# Retry once: a mirror hiccup shouldn't waste a whole build (mkarchiso resumes where it stopped).
mkarchiso -v -r -w "$WORK/build" -o "$OUT" "$STAGE" || {
    warn "Build step failed - retrying once in 20 seconds"
    sleep 20
    mkarchiso -v -r -w "$WORK/build" -o "$OUT" "$STAGE"
}

iso="$(ls -t "$OUT"/devium-*.iso | head -n1)"
say "Done: $iso ($(du -h "$iso" | cut -f1))"
