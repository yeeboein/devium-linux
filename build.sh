#!/usr/bin/env bash
# Build the Devium ISO. Run on Arch Linux (or in an archlinux container) as root:
#
#   sudo ./build.sh            build into ./out
#   sudo ./build.sh --clean    remove the old work directory first
#
# Needs: archiso, git (installed automatically if missing).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${WORK_DIR:-$HERE/work}"
OUT="${OUT_DIR:-$HERE/out}"
STAGE="$WORK/profile"

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
pacman -Sy --needed --noconfirm archiso git >/dev/null

# 1. Fresh copy of the profile, so the repo itself is never modified.
say "Preparing profile in $STAGE"
rm -rf "$STAGE"
mkdir -p "$STAGE" "$OUT"
cp -a "$HERE/profile/." "$STAGE/"

# 2. Drop packages that don't exist (anymore), instead of failing the whole build.
say "Checking package list"
pacman -Sy >/dev/null
: > "$STAGE/packages.x86_64"
missing=()
while read -r pkg; do
    pkg="${pkg%%#*}"; pkg="${pkg//[[:space:]]/}"
    [[ -z $pkg ]] && continue
    if pacman -Si "$pkg" >/dev/null 2>&1 || pacman -Sg "$pkg" >/dev/null 2>&1; then
        echo "$pkg" >> "$STAGE/packages.x86_64"
    else
        missing+=("$pkg")
    fi
done < "$HERE/profile/packages.x86_64"
if (( ${#missing[@]} )); then
    warn "Skipping packages not found in the repos: ${missing[*]}"
fi
for must in base linux mkinitcpio-archiso plasma-desktop sddm; do
    grep -qx "$must" "$STAGE/packages.x86_64" || die "Required package '$must' is missing."
done

# Package list for installed systems (live-ISO-only packages removed).
grep -vxE 'mkinitcpio-archiso|syslinux|memtest86\+|memtest86\+-efi|edk2-shell|archinstall' \
    "$STAGE/packages.x86_64" > "$STAGE/airootfs/usr/share/devium/install-packages.txt"

# 3. Bundle ArchPill (https://github.com/yeeboein/archpill).
say "Downloading ArchPill"
mkdir -p "$STAGE/airootfs/opt"
git clone --depth 1 https://github.com/yeeboein/archpill.git "$STAGE/airootfs/opt/archpill" \
    || warn "Could not download ArchPill now; it will be downloaded on first boot with internet."

# 4. Release info (used by the installer to fetch Devium's files for the new system).
repo_url="https://github.com/yeeboein/devium-linux"
repo_ref="$(git -C "$HERE" rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
[[ $repo_ref == HEAD ]] && repo_ref=main
cat > "$STAGE/airootfs/etc/devium-release" <<EOF
DEVIUM_VERSION=$(date +%Y.%m.%d)
DEVIUM_REPO=${DEVIUM_REPO:-$repo_url}
DEVIUM_REF=${DEVIUM_REF:-$repo_ref}
EOF

# 5. Build.
say "Building the ISO (this takes a while)"
mkarchiso -v -r -w "$WORK/build" -o "$OUT" "$STAGE"

iso="$(ls -t "$OUT"/devium-*.iso | head -n1)"
say "Done: $iso ($(du -h "$iso" | cut -f1))"
