---

### Download

Pick one edition below and follow the [guide](https://github.com/yeeboein/devium-linux/blob/main/docs/GUIDE.md):
- **Devium KDE Plasma** (`devium-kdeplasma-<version>-x86_64.iso`): the main one, for most computers
- **Devium Xfce** (`devium-xfce-<version>-x86_64.iso`): lighter, for old laptops
- **Devium Hyprland** (`devium-hyprland-<version>-x86_64.iso`): a tiling desktop for keyboard lovers

Secure Boot must be off to start Devium (see [Secure Boot](https://github.com/yeeboein/devium-linux/blob/main/docs/SECURE-BOOT.md)).

If the ISO comes in parts (`.iso.000`, `.iso.001`, ...), download all parts and join them:
- Linux/macOS: `cat devium-*.iso.0* > devium.iso`
- Windows (Command Prompt): `copy /b devium-kdeplasma-<version>-x86_64.iso.000+devium-kdeplasma-<version>-x86_64.iso.001 devium.iso`

Check the download with the `.sha256` file (optional). When the release has `SHA256SUMS.asc`, you can also check it
really comes from Devium: see [Verifying downloads](https://github.com/yeeboein/devium-linux/blob/main/docs/VERIFY.md).

### Community
Questions, bugs or ideas? Join the **[Devium Discord](https://discord.gg/YTMattgyG3)**.
