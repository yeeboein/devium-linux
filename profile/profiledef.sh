#!/usr/bin/env bash
# shellcheck disable=SC2034
# Devium archiso profile (based on Arch Linux's "releng" profile).

iso_name="devium"
iso_label="DEVIUM_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"
iso_publisher="Devium <https://github.com/yeeboein/devium-linux>"
iso_application="Devium Live"
iso_version="$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y.%m.%d)"
install_dir="arch"
buildmodes=('iso')
bootmodes=('bios.syslinux'
           'uefi.systemd-boot')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'zstd' '-Xcompression-level' '15' '-b' '1M')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/etc/sudoers.d"]="0:0:750"
  ["/etc/sudoers.d/10-devium-live"]="0:0:440"
  ["/root"]="0:0:750"
  ["/root/.gnupg"]="0:0:700"
  ["/usr/local/bin/devium-welcome"]="0:0:755"
  ["/usr/local/bin/devium-update-manager"]="0:0:755"
  ["/usr/local/bin/devium-update-check"]="0:0:755"
  ["/usr/local/bin/devium-install"]="0:0:755"
  ["/usr/local/bin/devium-firstrun"]="0:0:755"
  ["/usr/local/bin/devium-new-project"]="0:0:755"
  ["/usr/local/bin/support"]="0:0:755"
  ["/usr/local/bin/devium-about"]="0:0:755"
  ["/usr/local/bin/devium-setup-wizard"]="0:0:755"
  ["/usr/local/bin/devium-updater"]="0:0:755"
  ["/usr/lib/devium/devium-helper"]="0:0:755"
  ["/usr/lib/devium/devium-setup"]="0:0:755"
  ["/usr/lib/devium/install-progress.py"]="0:0:755"
)
