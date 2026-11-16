#!/usr/bin/env bash
# Make Devium's release signing key (run once, on your own computer, not on a server).
#   bash tools/make-signing-key.sh
# It writes two files to ~/devium-signing-key/:
#   private-key.asc  -> paste into GitHub as the secret DEVIUM_SIGNING_KEY, then keep a copy somewhere safe
#                       (a USB stick or password manager) and delete it from the laptop
#   public-key.asc   -> safe to share: it goes in the repo as docs/devium-signing-key.asc
set -euo pipefail
command -v gpg >/dev/null || { echo "gpg is not installed (sudo pacman -S gnupg)"; exit 1; }
out="$HOME/devium-signing-key"
[[ -e $out/private-key.asc ]] && { echo "$out/private-key.asc already exists - not making another key."; exit 1; }
mkdir -p "$out" && chmod 700 "$out"
export GNUPGHOME="$(mktemp -d)"
trap 'rm -rf "$GNUPGHOME"' EXIT
# No passphrase: GitHub Actions signs releases unattended. The key only lives in the GitHub secret and your backup.
gpg --batch --quiet --passphrase '' --quick-gen-key "Devium release signing" ed25519 sign 5y 2>/dev/null
fpr=$(gpg --batch --with-colons --list-keys | awk -F: '/^fpr/ {print $10; exit}')
gpg --batch --armor --export "$fpr" > "$out/public-key.asc"
gpg --batch --armor --export-secret-keys "$fpr" > "$out/private-key.asc"
chmod 600 "$out/private-key.asc"
cat <<MSG

Done! Key fingerprint: $fpr

1. Open https://github.com/yeeboein/devium-linux/settings/secrets/actions
   New repository secret -> Name: DEVIUM_SIGNING_KEY -> Secret: everything in
   $out/private-key.asc  (cat it and copy all of it, including the BEGIN/END lines)
2. Copy private-key.asc to a USB stick or password manager, then delete it from this laptop:
   rm $out/private-key.asc
3. Send the public key ($out/public-key.asc) and the fingerprint above so they go in the repo.
   The public key is safe to share; the private one never is.
MSG
