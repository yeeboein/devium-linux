# Devium guide: download, try, install and keep it updated

This guide takes you from nothing to a working Devium. No Linux experience needed.
Devium is Arch-based and **rolling**: you install it once and keep updating, you never reinstall for a new version
([how updates work](ROLLING.md)).

**Contents**
1. [Pick an edition and check your computer](#1-pick-an-edition-and-check-your-computer)
2. [Download the ISO](#2-download-the-iso)
3. [Try it in a virtual machine (safest)](#3-try-it-in-a-virtual-machine-safest)
4. [Make a bootable USB stick](#4-make-a-bootable-usb-stick)
5. [Boot a real computer from the USB](#5-boot-a-real-computer-from-the-usb)
6. [Install Devium to disk](#6-install-devium-to-disk)
7. [Installing next to Windows (dual boot)](#7-installing-next-to-windows-dual-boot)
8. [Your first boot: Devium Configure](#8-your-first-boot-devium-configure)
9. [Everyday tips and shortcuts](#9-everyday-tips-and-shortcuts)
10. [Updating Devium](#10-updating-devium)
11. [Taking Devium off again](#11-taking-devium-off-again)
12. [Problems and fixes](#12-problems-and-fixes)
13. [Getting help](#13-getting-help)

---

## 1. Pick an edition and check your computer

| Edition | Best for | File name |
|---|---|---|
| **KDE Plasma** (main) | most computers, the full Devium experience | `devium-kdeplasma-<version>-x86_64.iso` |
| **Xfce** | old or slow laptops, lowest RAM use | `devium-xfce-<version>-x86_64.iso` |
| **Hyprland** | keyboard lovers, automatic tiling windows | `devium-hyprland-<version>-x86_64.iso` |

Not sure? Take **KDE Plasma**. On a computer with 4 GB of RAM or less, or a very old processor, take **Xfce**.

**What you need**
- A 64-bit computer (Intel or AMD), made in the last 12 years or so.
- **4 GB of RAM** is comfortable (the installer needs at least 2 GB).
- **At least 10 GB** of free disk space, 30 GB or more is better.
- **Internet** during the install (Wi-Fi or a cable).
- A **USB stick of 8 GB or more** (it gets erased).
- Secure Boot turned **off** (see [Secure Boot](SECURE-BOOT.md)). Devium doesn't start with it on.

---

## 2. Download the ISO

1. Open **https://github.com/yeeboein/devium-linux/releases** and pick the newest release.
2. Under **Assets**, download the `.iso` for your edition.
   - If the ISO comes in parts (`.iso.000`, `.iso.001`, ...), download all parts and join them:
     - Linux/Mac: `cat devium-*.iso.0* > devium.iso`
     - Windows (Command Prompt): `copy /b devium-kdeplasma-<version>-x86_64.iso.000+devium-kdeplasma-<version>-x86_64.iso.001 devium.iso`
3. **Optional but a good idea: check the download.** Download the matching `.sha256` file too, and compare. Steps:
   [Verifying downloads](VERIFY.md).

> Download keeps stopping? Use a download manager, or try again on a different connection. The file is about 1.6–1.9 GB.

---

## 3. Try it in a virtual machine (safest)

A virtual machine (VM) runs Devium in a window on your current computer. Nothing on your computer changes.

### VirtualBox (Windows, Mac with Intel, Linux)

1. Install VirtualBox from **https://www.virtualbox.org**.
2. Click **New**.
   - **Name:** `Devium`
   - **ISO Image:** pick the Devium `.iso`
   - **Type:** Linux, **Version:** Arch Linux (64-bit)
   - Tick **Skip Unattended Installation**
3. **Hardware:** Memory **4096 MB**, Processors **2**. Tick **Enable EFI**.
4. **Hard disk:** **20 GB** or more.
5. **Settings > Display:** Video Memory **128 MB**, Graphics Controller **VMSVGA**, tick **Enable 3D Acceleration**.
6. Click **Start**.

After installing inside the VM, **remove the ISO** (Settings > Storage) so it boots from the disk.

### Other VM apps
- **VMware Workstation Player:** New VM, pick the ISO, "Other Linux 6.x kernel 64-bit", 4 GB RAM, 20 GB disk.
- **GNOME Boxes / virt-manager (Linux):** new VM from the ISO, 4 GB RAM, turn on UEFI.
- **Apple Silicon Macs** can't run these x86 ISOs at full speed. Use a real PC or an Intel Mac.

When it boots, pick **Devium Live** (it starts on its own after 10 seconds). You land on a live desktop where you
can look around. Nothing is saved after a restart.

- Live user: **devium**, password: **devium**

---

## 4. Make a bootable USB stick

You need a USB stick of **8 GB or more**. **Everything on it will be erased.**

**Easiest: balenaEtcher** (Windows, Mac, Linux)
1. Download it from **https://etcher.balena.io**.
2. **Flash from file** and pick the Devium `.iso`.
3. **Select target** and pick your USB stick (check it's the right one!).
4. **Flash!** and wait.

**Alternatives:** **Rufus** on Windows (choose "DD Image mode" if it asks), or **Ventoy** (copy the `.iso` onto the stick like a normal file).

---

## 5. Boot a real computer from the USB

1. Plug in the USB stick and restart the computer.
2. Right as it starts, tap the **boot menu key** over and over:

   | Brand | Boot menu key |
   |---|---|
   | Dell | F12 |
   | HP | F9 or Esc |
   | Lenovo | F12 (or the small Novo button) |
   | Acer | F12 |
   | ASUS | F8 or Esc |
   | MSI | F11 |
   | Mac (Intel) | hold Option |

3. Choose the USB stick (it may say "UEFI: <USB name>").
4. Pick **Devium Live**.

> **"Secure Boot violation" or it won't start?** Turn **Secure Boot** off in the BIOS/UEFI settings (usually F2 or
> Del at startup), save and try again. Step by step for each brand: [Secure Boot](SECURE-BOOT.md).
>
> **Black screen?** Restart and choose **Devium Live - safe graphics**.

**Try everything before installing:** Wi-Fi, sound, touchpad, brightness, the screen. If something doesn't work, tell
us on Discord before you install, it helps other people too.

---

## 6. Install Devium to disk

> **Back up your files first.** Some choices below erase a whole disk. If in doubt, try it in a VM first.

1. On the live desktop, open **Install Devium**.
2. The installer (Calamares) opens. It checks that your computer has enough space, memory and internet. Connect to
   Wi-Fi first from the network icon if it says there is no internet.
3. Go through the pages with **Next**:

   | Page | What to do |
   |---|---|
   | **Welcome** | pick your language |
   | **Location** | pick your region and time zone (click the map) |
   | **Keyboard** | pick your layout and test it in the box |
   | **Partitions** | choose how to use the disk (see below) |
   | **Users** | your name, a computer name, and a password. The password is also used for the administrator account |
   | **Summary** | check everything, then click **Install** |

4. **Partitions: which option?**

   | You want | Choose |
   |---|---|
   | Devium only, wipe the whole disk | **Erase disk** |
   | Devium next to Windows | **Install alongside** (see [section 7](#7-installing-next-to-windows-dual-boot)) |
   | Use one specific partition | **Replace a partition** |
   | Full control | **Manual partitioning** (advanced) |

   Extras on this page:
   - **File system:** **ext4** is the simple choice. **btrfs** is for snapshots later.
   - **Encrypt system:** tick it to protect your files if the laptop is lost. You'll type a passphrase at every start.
     Don't forget it, there is no way to recover it.
   - **Swap:** "No swap" is fine on most machines. "Swap to file" helps small-RAM machines.

5. The install takes **10 to 30 minutes** depending on your internet. A slideshow shows what's coming.
6. When it says **All done**, tick **Restart now**, click **Done**, and **remove the USB stick** when the screen
   goes dark.
7. Log in with the name and password you chose.

---

## 7. Installing next to Windows (dual boot)

1. **Back up your Windows files.** Dual boot is safe when done carefully, but a backup costs you nothing.
2. In Windows:
   - If you use **BitLocker**, write down the recovery key (Microsoft account > devices) or turn it off first.
   - Turn off **Fast Startup** (Control Panel > Power Options > Choose what the power buttons do).
   - Optional: shrink the Windows partition in **Disk Management** to leave at least 30 GB of free space.
3. Boot the Devium USB (Secure Boot off) and open **Install Devium**.
4. On the **Partitions** page choose **Install alongside**. Drag the divider to say how much space Devium gets
   (30 GB or more is comfortable).
5. Finish the install as normal. When the computer starts you'll see a menu with **Devium** and **Windows**.

If Windows doesn't show in the menu, log in to Devium and run `sudo grub-mkconfig -o /boot/grub/grub.cfg`.

---

## 8. Your first boot: Devium Configure

On your first login **Devium Configure** opens by itself. This is where you choose what to install: browser, file
manager, terminal, code editor, languages, Python libraries, developer tools, games and apps. It shows how much
space each pick needs, and only what you pick is installed.

- Go through the pages, click **Skip** on any you don't need, then **Install**.
- **The first time, you can't close Configure until Devium is fully set up.** Let it finish. It takes a few minutes.
- At the end, **log out and back in** (or restart) so everything is ready.
- You can run Configure again whenever you want (type "configure" in Spotlight) to add or remove things.
- ArchPill (the pill at the top of the screen), the dock and the desktop widgets are set up for you. Turn them off in
  Devium Tools > Look.

---

## 9. Everyday tips and shortcuts

*Meta = the Windows key (Super).*

| To do this | Do this |
|---|---|
| Search apps, files, maths, the web | **Meta+Space** (or Alt+Space), type, press Enter |
| Run a command from the search box | type `> ` then the command |
| Open Devium Tools | **Meta+T** |
| Open Updates | **Meta+U** |
| Take a screenshot and mark it up | **Meta+Ctrl+S** (Devium Screenshot Editor) |
| Get apps | **Discover** (the shopping bag icon) |
| See all terminal commands | type `support` |
| Fix common problems | type `support fix` |
| Learn the terminal in 10 short lessons | type `support learn` |
| Start a coding project | `devium-new-project myapp` |
| Quick notes | `note "call mum"` then `note` to see them |
| Free up space | Devium Tools > Clean up |
| Back up to a USB stick | Devium Tools > Backup and move |

**Hyprland edition:** press **Super+/** for the shortcuts cheat sheet. Windows tile themselves.
**KDE edition:** automatic tiling is optional (Devium Configure > Customise).

**Tip for beginners:** if you break the look, Devium Tools > Look > **Reset desktop** puts it back.

---

## 10. Updating Devium

Devium is rolling, so you update the same system again and again.

1. Open **Devium Updater** (Meta+U). It shows what is waiting. Click **Update**.
2. When a new **Devium release** is out (for example beta19), use the **Update Devium** button. It updates Devium's
   own apps and look, and keeps your files and apps.
3. Restart now and then, especially after a kernel update.
4. Something broke after an update? Use **Undo** in Devium Tools > Updates, or `support fix`.

More detail: [How Devium updates](ROLLING.md).

---

## 11. Taking Devium off again

**Devium on its own disk:** install another system over it, or wipe the disk.

**Devium next to Windows:**
1. Back up anything you want from Devium.
2. In Windows, open **Disk Management**, delete the Devium partitions (ext4/btrfs) and extend the Windows partition
   into the space.
3. The Devium boot menu may stay. To get Windows' own boot back, open Command Prompt as administrator and run
   `bcdboot C:\Windows`. If you're unsure, ask on Discord before deleting anything.

**In a VM:** delete the virtual machine in VirtualBox. Nothing else changes.

---

## 12. Problems and fixes

| Problem | Fix |
|---|---|
| Black screen after the boot menu | Choose **safe graphics** in the boot menu. On NVIDIA laptops install the driver afterwards (Devium Tools > Drivers). |
| USB stick doesn't show in the boot menu | Turn off **Secure Boot** and **Fast Boot** in the BIOS. Re-flash the stick with balenaEtcher. |
| "Secure Boot violation" | [Secure Boot guide](SECURE-BOOT.md) |
| No Wi-Fi | Click the network icon (bottom right). Broadcom card? Devium Tools > Drivers. Or use an Ethernet cable or phone USB tethering. |
| Installer says "no internet" | Connect to Wi-Fi first, then start the installer again. |
| Installer says not enough space | Free up space or choose a bigger disk. Devium needs at least 10 GB. |
| Installer shows an error | Take a photo of the message and [open an issue](https://github.com/yeeboein/devium-linux/issues). Nothing on the disk changes until you click **Install**. |
| VM is very slow or flickers | Give it 4 GB RAM and 2 CPUs, turn on 3D acceleration (VirtualBox: VMSVGA). |
| Computer starts Windows, not Devium | Turn off Fast Startup in Windows, pick Devium in the BIOS boot menu. Still stuck? Ask on Discord. |
| Forgot the live password | It's **devium**. |
| Forgot your own password | Boot the USB, open a terminal and use `passwd` in a chroot, or ask on Discord how. Encrypted disks can't be recovered. |
| Something broke after an update | Devium Tools > Updates > **Undo**, or boot **Safe mode** from the boot menu. |
| Screen too small or too big (HiDPI) | System Settings > Display > Scale. |

---

## 13. Getting help

- **Discord:** https://discord.gg/YTMattgyG3 is the fastest. Say which edition and version you use, and what you did.
- **Bugs and ideas:** https://github.com/yeeboein/devium-linux/issues has forms for bugs, hardware and ideas.
- **In Devium:** `support` lists helpful commands, and Devium Tools > Help has a bug-report button.
- **Hardware works or doesn't?** Tell us. It helps everyone else with the same computer.

Devium is Arch-based and is not affiliated with or endorsed by Arch Linux.
