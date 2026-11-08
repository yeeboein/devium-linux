# Devium guide: download, try and install

This guide takes you from nothing to a working Devium system. No Linux experience needed.

**Contents**
1. [Download the ISO](#1-download-the-iso)
2. [Try it in a virtual machine (safest)](#2-try-it-in-a-virtual-machine-safest)
3. [Make a bootable USB stick](#3-make-a-bootable-usb-stick)
4. [Boot a real computer from the USB](#4-boot-a-real-computer-from-the-usb)
5. [Install Devium to disk](#5-install-devium-to-disk)
6. [After installing](#6-after-installing)
7. [Problems and fixes](#7-problems-and-fixes)

---

## 1. Download the ISO

1. Sign in to GitHub and open **https://github.com/yeeboein/devium-linux/actions**.
2. Click the newest **Build Devium ISO** run with a green tick ✅.
3. Scroll to **Artifacts** at the bottom and click **devium-iso**.
4. Unzip the download. Inside is `devium-YYYY.MM.DD-x86_64.iso` (about 2–3 GB).

> No green run, or the download expired (14 days)? Click **Build Devium ISO** → **Run workflow** and wait 30–60 minutes.

---

## 2. Try it in a virtual machine (safest)

A virtual machine (VM) runs Devium in a window on your current computer. Nothing on your computer is changed.

### VirtualBox (Windows, Mac with Intel, Linux)

1. Install VirtualBox from **https://www.virtualbox.org**.
2. Click **New**.
   - **Name:** `Devium`
   - **ISO Image:** pick the Devium `.iso`
   - **Type:** Linux, **Version:** Arch Linux (64-bit)
   - Tick **Skip Unattended Installation**
3. **Hardware:** Memory **4096 MB** (2048 minimum), Processors **2**. Tick **Enable EFI** (optional).
4. **Hard disk:** **30 GB** (only used if you test installing).
5. Click **Finish**, then **Settings → Display**:
   - Video Memory: **128 MB**
   - Graphics Controller: **VMSVGA**
   - Tick **Enable 3D Acceleration**
6. Click **Start**.

### Other VM apps
- **VMware Workstation Player:** New VM → pick the ISO → "Other Linux 6.x kernel 64-bit" → 4 GB RAM, 30 GB disk.
- **GNOME Boxes / virt-manager (Linux):** create a new VM from the ISO, give it 4 GB RAM.

When it boots, pick **Devium Live** in the menu (it starts on its own after 10 seconds).
You'll land on the Devium desktop. The **Welcome** app opens by itself.

- Live user: **devium**, password: **devium**
- Nothing is saved in the live system after a restart.

---

## 3. Make a bootable USB stick

You need a USB stick of **8 GB or more**. **Everything on it will be erased.**

**Easiest: balenaEtcher** (Windows, Mac, Linux)
1. Download from **https://etcher.balena.io**.
2. **Flash from file** → pick the Devium `.iso`.
3. **Select target** → pick your USB stick (check it's the right one!).
4. **Flash!** and wait.

**Alternatives:** **Rufus** on Windows (choose "DD Image mode" if asked), or **Ventoy** (copy the `.iso` onto the stick like a normal file).

---

## 4. Boot a real computer from the USB

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
   | Mac (Intel) | hold Option ⌥ |

3. Choose the USB stick (it may say "UEFI: <USB name>").
4. Pick **Devium Live**.

> **"Secure Boot violation" or it won't boot?** Go into the BIOS/UEFI settings (usually F2 or Del at startup), turn **Secure Boot** off, save and try again.
>
> **Black screen?** Restart and choose **Devium Live – safe graphics**.

Try everything before installing: Wi-Fi, sound, touchpad, screen brightness.

---

## 5. Install Devium to disk

> ⚠️ **Back up your files first.** Installing can erase the whole disk. Test in a VM first if you can.

You need **internet** for the installer (connect to Wi-Fi from the network icon at the bottom right).

1. Double-click **Install Devium** on the desktop (or Welcome → **Install Devium**).
2. A terminal window opens. Read the notes, type **y** and press **Enter**.
3. Arch's installer menu appears. Move with the **arrow keys**, select with **Enter**, go back with **Esc**.

   Set these (leave everything else as it is):

   | Menu item | What to choose |
   |---|---|
   | **Locales** | your keyboard layout and language |
   | **Mirrors** | your country (faster downloads) |
   | **Disk configuration** | *Partitioning* → **Use a best-effort default partition layout** → pick your disk → filesystem **ext4** (simple) or **btrfs** (snapshots). **This erases that disk.** |
   | **Bootloader** | leave the default |
   | **Hostname** | a name for your computer, e.g. `devium` |
   | **Authentication** | **Root password**: set one. **User account**: add your username + password and answer **yes** to "superuser (sudo)" |
   | **Profile** | **Minimal** (Devium adds KDE Plasma and all its apps itself) |
   | **Audio** | **Pipewire** (may already be set) |
   | **Network configuration** | **Use NetworkManager** (may already be set) |
   | **Additional packages** | already filled in by Devium, leave it |
   | **Timezone** | your timezone |

4. Choose **Install** and confirm. It downloads and installs everything: **10–30 minutes** depending on your internet.
5. At the end it adds Devium's apps, look and ArchPill. If it asks to **chroot** into the new system, choose **no**.
6. When it says **Devium is installed!**, shut down, **remove the USB stick**, and turn the computer on.
7. Log in with the username and password you created.

---

## 6. After installing

On your first login:
- **ArchPill** sets itself up (move the mouse to the top-centre of the screen).
- **VS Code** gets its Python extension in the background.
- **Devium Welcome** opens. Good first steps:
  1. **Beginner / Pro** – pick how Devium should feel.
  2. **System → Restore points** – set up Timeshift, so you can undo a bad update.
  3. **Drivers** – install anything suggested for your computer (e.g. NVIDIA).
  4. **Update Manager** (Meta+U) – install the latest updates.

### Everyday tips

| To do this | Do this |
|---|---|
| Open apps | Click the Devium logo (bottom left) or press **Meta** |
| Screenshot an area | **Meta+Shift+S** – it's copied, just paste it |
| Get apps | **Discover** (the shopping bag icon) |
| Update everything | **Update Manager** or type `update` in a terminal |
| Start a Python project | Welcome → **Coding → New Python project** |
| See all shortcuts | Welcome → **Shortcuts** |

*Meta = the Windows key.*

---

## 7. Problems and fixes

| Problem | Fix |
|---|---|
| Black screen after the boot menu | Choose **safe graphics** in the boot menu. On NVIDIA laptops, install the NVIDIA driver from Welcome → Drivers afterwards. |
| USB stick doesn't show in the boot menu | Turn off **Secure Boot** and **Fast Boot** in the BIOS. Re-flash the stick with balenaEtcher. |
| No Wi-Fi | Click the network icon (bottom right). Broadcom card? Welcome → **Drivers**. Or use an Ethernet cable / phone USB tethering. |
| VM is very slow or the screen flickers | Give it 4 GB RAM and 2 CPUs, turn on 3D acceleration (VirtualBox: VMSVGA). |
| Installer says "No internet connection" | Connect to Wi-Fi first, then start the installer again. |
| Installer shows an error | Take a photo/screenshot of the message and [open an issue](https://github.com/yeeboein/devium-linux/issues). Nothing on the disk changes until you choose **Install**. |
| ArchPill doesn't appear | Open **ArchPill** from the app menu. Still nothing? Run `~/archpill/install.sh --no-packages` in a terminal. |
| Forgot the live password | It's **devium**. |
