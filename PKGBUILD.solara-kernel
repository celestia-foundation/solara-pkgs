# Maintainer: Celestia Ludenberg <ash8820@proton.me>
# Celestial Gothic | STAY AWAY FROM MY VODKA | untz/untz

pkgname=solara-kernel
pkgver=7.0.5
pkgrel=zen1
pkgdesc="Solara Linux Kernel - Compiled from Linux ZEN kernel source 🔥"
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
    tar -xf "${srcdir}/linux-v7.0.5-zen1.patch.zst"
    
    # Apply all ZEN patches
    for patch in *.patch; do
        [ -f "$patch" ] && patch -p1 -N < "$patch" || true
    done
    
    # Use ZEN defconfig
    make x86_64_defconfig
    
    # 🔥 SOLARA BRANDING 🔥
    sed -i 's/CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION="-solara"/g' .config
    sed -i 's/CONFIG_DEFAULT_HOSTNAME=.*/CONFIG_DEFAULT_HOSTNAME="solara"/g' .config
    sed -i 's/CONFIG_LOCALVERSION_AUTO=.*/CONFIG_LOCALVERSION_AUTO=n/g' .config
    
    echo "🔥 SOLARA BRANDING APPLIED! 🔥"
}

build() {
    cd linux-7.0.5
    
    # Compile with LLVM/Clang on EPYC
    make -j$(nproc) CC=clang LD=ld.lld LLVM=1 localmodconfig
    make -j$(nproc) CC=clang LLVM=1 bzImage -y
    make -j$(nproc) CC=clang LLVM=1 modules -y
    
    echo "🔥 ZEN kernel compiled with LLVM! 🔥"
}

package() {
    cd linux-7.0.5
    DESTDIR="${pkgdir}" make modules_install install
    cp arch/x86_64/boot/bzImage "${pkgdir}/boot/vmlinuz-solara"
    depmod -a "${pkgdir}/usr/lib/modules/$(ls usr/lib/modules/)"
}
