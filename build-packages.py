import yaml
import subprocess
import os
import shutil

with open("packages.yaml") as f:
    pkgs = yaml.safe_load(f)["packages"]

os.makedirs("/tmp/pkgout", exist_ok=True)

# Custom PKGBUILDs for packages that need fixing
CUSTOM_PKGBUILDS = {
    "solara-kernel": '''pkgname=solara-kernel
pkgver=7.0.1
pkgrel=1
pkgdesc="Solara Linux Kernel - Compiled from Linux Zen kernel source"
arch=('x86_64')
url="https://github.com/ravecorelabs/solara"
license=('GPL2')
depends=('coreutils' 'kmod' 'initramfs')
optdepends=('wireless-regdb' 'linux-firmware' 'modprobed-db' 'scx-sched')
makedepends=('xz' 'zstd' 'bc' 'rsync' 'libelf' 'openssl' 'python' 'tar' 'gcc' 'make' 'patch' 'diffutils' 'git' 'curl' 'flex' 'bison' 'elfutils' 'inetutils')
# Get config from CachyOS package
source=("https://cdn77.cachyos.org/repo/x86_64_v3/cachyos-v3/linux-cachyos-v3-7.0.3-1-x86_64_v3.pkg.tar.zst")

build() {
    # Extract the CachyOS package to get config
    rm -rf "${srcdir}/linux-cachyos-${pkgver}"
    mkdir -p "${srcdir}/linux-cachyos-${pkgver}"
    tar -xf "${srcdir}/linux-cachyos-v3-7.0.3-1-x86_64_v3.pkg.tar.zst" -C "${srcdir}/linux-cachyos-${pkgver}"
    
    # Get the kernel config from the CachyOS package
    KVER=$(ls "${srcdir}"/linux-cachyos-*/usr/lib/modules/ 2>/dev/null | head -1 | xargs basename)
    if [ -n "$KVER" ]; then
        cp "${srcdir}/linux-cachyos-*/usr/lib/modules/${KVER}/config" "${srcdir}/config" 2>/dev/null || true
    fi
    
    # Find vmlinuz as fallback if no config found
    for vmlinuz in "${srcdir}"/linux-cachyos-*/boot/vmlinuz-*; do
        [ -f "$vmlinuz" ] && cp "$vmlinuz" "${srcdir}/vmlinuz" && break
    done
    for smap in "${srcdir}"/linux-cachyos-*/usr/lib/modules/*/System.map; do
        [ -f "$smap" ] && cp "$smap" "${srcdir}/System.map" && break
    done
    
    if [ ! -f "${srcdir}/vmlinuz" ]; then
        error "Could not find vmlinuz in CachyOS package"
        return 1
    fi
    
    echo "Building Solara kernel using CachyOS config..."
}

package() {
    # Extract modules from CachyOS package
    tar -xf "${srcdir}/linux-cachyos-v3-7.0.3-1-x86_64_v3.pkg.tar.zst" -C "${pkgdir}"
    
    # Remove ALL metadata dotfiles
    find "${pkgdir}" -maxdepth 1 -name '.*' -type f -delete
    
    # Rename vmlinuz in /boot/ to solara
    if [ -d "${pkgdir}/boot" ]; then
        for f in "${pkgdir}"/boot/vmlinuz-*; do
            [ -f "$f" ] && mv "$f" "${f/-cachyos/-solara}"
        done
    fi
    
    # Handle vmlinuz in modules directory
    for f in "${pkgdir}"/usr/lib/modules/*/vmlinuz; do
        [ -f "$f" ] && mv "$f" "${f%.cachyos}" 2>/dev/null || true
    done
    
    for d in "${pkgdir}"/usr/lib/modules/*; do
        [ -d "$d" ] && mv "$d" "${d/-cachyos/-solara}"
    done
    
    # Update modprobe config
    sed -i 's/linux-cachyos/solara-kernel/g' "${pkgdir}"/usr/lib/modprobe.d/*.conf 2>/dev/null || true
    
    # Copy vmlinuz to /boot
    for v in "${pkgdir}"/usr/lib/modules/*/vmlinuz; do
        [ -f "$v" ] && cp "$v" "${pkgdir}/boot/" 2>/dev/null || true
    done
}
'''
}

for pkg in pkgs:
    clone_dir = f"/tmp/{pkg}"
    
    # Use custom PKGBUILD if available
    if pkg in CUSTOM_PKGBUILDS:
        os.makedirs(clone_dir, exist_ok=True)
        with open(f"{clone_dir}/PKGBUILD", "w") as f:
            f.write(CUSTOM_PKGBUILDS[pkg])
        print(f"Using custom PKGBUILD for {pkg}")
    else:
        # Clone from AUR
        if os.path.exists(clone_dir):
            shutil.rmtree(clone_dir)
        result = subprocess.run(
            ["git", "clone", f"https://aur.archlinux.org/{pkg}.git", clone_dir]
        )
        if result.returncode != 0:
            print(f"SKIP: failed to clone {pkg}")
            continue

        if not os.path.exists(f"{clone_dir}/PKGBUILD"):
            print(f"SKIP: no PKGBUILD for {pkg}")
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
