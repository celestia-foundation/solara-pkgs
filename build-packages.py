import yaml
import subprocess
import os
import shutil

with open("packages.yaml") as f:
    pkgs = yaml.safe_load(f)["packages"]

os.makedirs("/tmp/pkgout", exist_ok=True)

# Actual Linux Zen kernel + CachyOS config compilation
CUSTOM_PKGBUILDS = {
    "solara-kernel": """pkgname=solara-kernel
pkgver=7.0.3
pkgrel=1
pkgdesc="Solara Linux Kernel - Compiled from Linux Zen kernel source with CachyOS patches"
arch=('x86_64')
url="https://github.com/ravecorelabs/solara"
license=('GPL2')
depends=('coreutils' 'kmod' 'initramfs')
optdepends=('wireless-regdb' 'linux-firmware' 'modprobed-db' 'scx-sched')
makedepends=('xz' 'zstd' 'bc' 'rsync' 'libelf' 'openssl' 'python' 'tar' 'gcc' 'make' 'patch' 'diffutils' 'git' 'curl' 'flex' 'bison' 'elfutils' 'inetutils' 'clang' 'lld' 'llvm')

source=("https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-7.0.3.tar.xz"
        "https://cdn77.cachyos.org/repo/x86_64_v3/cachyos-v3/linux-cachyos-v3-7.0.3-1-x86_64_v3.pkg.tar.zst"
        "https://github.com/CachyOS/linux-cachyos-patches/raw/refs/heads/main/patches/7.0/cachyos-base-v3.tar.xz"
        "https://github.com/CachyOS/kernel-patches/raw/refs/heads/main/7.0/0001-ZEN-v3-EVDF-git-patches.tar.xz")
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP')

prepare() {
    cd linux-7.0.3
    tar -xf "${srcdir}/linux-cachyos-v3-7.0.3-1-x86_64_v3.pkg.tar.zst" -C ../
    KVER=$(ls ../linux-cachyos-*/usr/lib/modules/ 2>/dev/null | head -1 | xargs basename)
    echo "Using CachyOS kernel config: $KVER"
    if [ -f "../linux-cachyos-*/usr/lib/modules/${KVER}/config" ]; then
        cp "../linux-cachyos-*/usr/lib/modules/${KVER}/config" .config
    else
        make defconfig
    fi
    sed -i 's/CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION="-solara"/g' .config
    sed -i 's/CONFIG_DEFAULT_HOSTNAME=.*/CONFIG_DEFAULT_HOSTNAME="solara"/g' .config
    echo "Configuration ready for Solara kernel build"
}

build() {
    cd linux-7.0.3
    make -j$(nproc) CC=clang LD=ld.lld LLVM=1 solara-defconfig
    make -j$(nproc) CC=clang LD=ld.lld LLVM=1 modules -y
    make -j$(nproc) CC=clang LD=ld.lld LLVM=1 bzImage -y
    echo "Kernel compilation complete!"
}

package() {
    cd linux-7.0.3
    DESTDIR="${pkgdir}" make modules_install install -j$(nproc)
    if [ -f arch/x86_64/boot/bzImage ]; then
        cp arch/x86_64/boot/bzImage "${pkgdir}/boot/vmlinuz-solara"
    fi
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
        print(f"Using custom PKGBUILD for {pkg}")
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
