# Verifying a Devium download

Checking the download is optional, but it proves the ISO is complete and really comes from Devium.

## 1. Is the download complete?
Every ISO has a `.sha256` file next to it.

- **Linux:** in the folder with both files, run `sha256sum -c devium-kdeplasma-<version>-x86_64.iso.sha256`.
  It should say `OK`.
- **Windows (PowerShell):** `Get-FileHash devium-kdeplasma-<version>-x86_64.iso` and compare the long code with
  the one in the `.sha256` file.
- **macOS:** `shasum -a 256 devium-kdeplasma-<version>-x86_64.iso`

## 2. Does it really come from Devium?
Releases from 1.0 on have `SHA256SUMS` and `SHA256SUMS.asc` (a signature made with Devium's private key).

1. Get Devium's public key: [`devium-signing-key.asc`](devium-signing-key.asc), and import it:
   `gpg --import devium-signing-key.asc`
2. Check the fingerprint it shows matches the one below.
3. Download `SHA256SUMS` and `SHA256SUMS.asc` from the release, then run:
   `gpg --verify SHA256SUMS.asc SHA256SUMS`
   It should say **Good signature from "Devium release signing"**.
4. Then check your ISO against the list: `sha256sum -c SHA256SUMS --ignore-missing`

Devium's signing key fingerprint: *(added when the key is created)*
