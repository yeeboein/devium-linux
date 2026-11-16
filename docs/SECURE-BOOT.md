# Secure Boot and Devium

**Short version:** turn Secure Boot **off** in your computer's settings before starting the Devium USB. Devium
works perfectly with it off, and so does Windows if you dual boot.

## Why
Secure Boot only starts systems signed with keys your computer already trusts (mostly Microsoft's). Devium, like
Arch Linux, isn't signed by Microsoft yet, so with Secure Boot on the USB just won't start (you'll see a "Secure
Boot violation" or "invalid signature" message, or it goes straight back to Windows).

## How to turn it off
1. Restart and press the settings key as soon as the logo appears:

   | Brand | Key |
   |---|---|
   | Lenovo | F2 or Fn+F2 (or the small Novo button) |
   | HP | Esc, then F10 |
   | Dell | F2 |
   | Acer | F2 |
   | ASUS | F2 or Del |
   | MSI | Del |
   | Microsoft Surface | hold Volume Up while pressing Power |

   From Windows you can also go to **Settings > System > Recovery > Advanced startup > Restart now >
   Troubleshoot > Advanced options > UEFI Firmware Settings**.
2. Find **Secure Boot** (usually under **Security** or **Boot**) and set it to **Disabled**. On some computers you
   must set a supervisor password first; you can remove it again afterwards.
3. Save and exit (often F10), then start the Devium USB.

**BitLocker:** if Windows uses BitLocker, write down your recovery key first
(aka.ms/myrecoverykey). Windows may ask for it once after Secure Boot changes.

## Turning Secure Boot back on (optional, for experts)
After installing, you can use your own keys with `sbctl`, keeping Microsoft's keys so Windows still starts:
1. In the firmware settings, put Secure Boot in **Setup Mode** (often "Reset to setup mode" or "Clear keys").
2. In Devium: `sudo pacman -S sbctl`, then `sudo sbctl create-keys` and `sudo sbctl enroll-keys -m`
   (`-m` keeps Microsoft's keys).
3. Sign the boot files: `sudo sbctl verify`, then `sudo sbctl sign -s` each file it lists
   (for example `/boot/vmlinuz-linux` and `/boot/efi/EFI/Devium/grubx64.efi`). sbctl re-signs them after every update.
4. Turn Secure Boot back on.

If it won't start afterwards, turn Secure Boot off again and ask on the Devium Discord. A simpler, built-in way is
planned for a later Devium version.
