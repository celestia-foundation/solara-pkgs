import yaml
import subprocess
import os
import shutil

with open("packages.yaml") as f:
    pkgs = yaml.safe_load(f)["packages"]

os.makedirs("/tmp/pkgout", exist_ok=True)

# Compile from ZEN kernel source (actual compilation!)
CUSTOM_PKGBUILDS = {
    "solara-kernel": """pkgname=solara-kernel
pkgver=7.0.5-zen1
pkgrel=1
pkgdesc="Solara Linux Kernel - Compiled from Linux Zen kernel source"
arch=('x86_64')
url="https://github.com/ravecorelabs/solara"
license=('GPL2')
depends=('coreutils' 'kmod' 'initramfs')
optdepends=('wireless-regdb' 'linux-firmware' 'modprobed-db' 'scx-sched')
makedepends=('xz' 'zstd' 'bc' 'rsync' 'libelf' 'openssl' 'python' 'tar' 'gcc' 'make' 'patch' 'diffutils' 'git' 'curl' 'flex' 'bison' 'elfutils' 'inetutils' 'clang' 'lld' 'llvm')

# Download mainline Linux + ZEN patches
source=("https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-7.0.5.tar.xz"
        "https://github.com/zen-kernel/zen-kernel/releases/download/v2.0/7.0.5/linux-v7.0.5-zen1.patch.zst")
sha256sums=('SKIP' 'SKIP')

prepare() {
    cd linux-7.0.5
    
    # Extract and apply ZEN patches
    tar -xf "https://github.com/zen-kernel/zen-kernel/releases/download/v2.0/7.0.5/linux-v7.0.5-zen1.patch.zst"
    
    # Apply all patches from ZEN release
    for patch in *.patch; do
        [ -f "$patch" ] && patch -p1 -N < "$patch" || true
    done
    
    # Use ZEN defconfig
    make x86_64_defconfig
    make menuconfig  # Allow user customization
    
    echo "ZEN kernel configured!"
}

build() {
    cd linux-7.0.5
    
    # Compile with LLVM/Clang on EPYC
    make -j$(nproc) CC=clang LD=ld.lld LLVM=1 localmodconfig
    make -j$(nproc) CC=clang LLVM=1bzImage -y
    make -j$(nproc) CC=clang LLVM=1 modules -y
    
    echo "ZEN kernel compiled with LLVM! 🔥"
}

package() {
    cd linux-7.0.5
    DESTDIR="${pkgdir}" make modules_install install
    cp arch/x86_64/boot/bzImage "${pkgdir}/boot/vmlinuz-solara"
    depmod -a "${pkgdir}/usr/lib/modules/$(ls usr/lib/modules/)"
}
"""
}

for pkg in pkgs:
    clone_dir = f"/tmp/{pkg}"
    
    if pkg in CUSTOM_PKGBUILDS:
        os.makedirs(clone_dir, exist_ok=True)
        with open(f"{clone_dir}/PKGBUILD", "w") as f:
            f.write(CUSTOM_PKGBUILDS[pkg])
        print(f"Compiling {pkg} from ZEN source!")
    else:
        if os.path.exists(clone_dir):
            shutil.rmtree(clone_dir)
        result = subprocess.run(
            ["git", "clone", f"https://aur.archlinux.org/{pkg}.git", clone_dir]
        )
        if result.returncode != 0:
            print(f"SKIP: failed to clone {pkg}")
            continue

    subprocess.run(["chown", "-R", "builder:builder", clone_dir], check=True)
    result = subprocess.run(
        ["su", "-", "builder", "-c", f"cd {clone_dir} && makepkg -s --noconfirm --noprogress --skippgpcheck"]
    )
    if result.returncode != 0:
        print(f"SKIP: build failed for {pkg}")
        continue

    subprocess.run(f"cp {clone_dir}/*.pkg.tar.zst /tmp/pkgout/ || true", shell=True)

print("Done!")
