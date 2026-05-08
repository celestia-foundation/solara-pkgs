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
pkgver=7.0.3
pkgrel=1
pkgdesc="Solara Linux Kernel - CachyOS optimized, Solara branded"
arch=('x86_64')
url="https://github.com/ravecorelabs/solara"
license=('GPL2')
depends=('coreutils' 'kmod' 'initramfs')
optdepends=('wireless-regdb' 'linux-firmware' 'modprobed-db' 'scx-sched')

source=("https://cdn77.cachyos.org/repo/x86_64_v3/cachyos-v3/linux-cachyos-${pkgver}-${pkgrel}-x86_64_v3.pkg.tar.zst")
sha256sums=('SKIP')

package() {
    tar -xf "${srcdir}/linux-cachyos-${pkgver}-${pkgrel}-x86_64_v3.pkg.tar.zst" -C "${pkgdir}"
    
    # Remove metadata dotfiles that cause Pacman to reject the package
    rm -f "${pkgdir}"/.BUILDINFO "${pkgdir}"/.MTREE "${pkgdir}"/.PKGINFO
    
    for f in "${pkgdir}"/boot/vmlinuz-*; do
        [ -f "$f" ] && mv "$f" "${f/-cachyos/-solara}"
    done
    
    for d in "${pkgdir}"/usr/lib/modules/*; do
        [ -d "$d" ] && mv "$d" "${d/-cachyos/-solara}"
    done
    
    sed -i 's/linux-cachyos/solara-kernel/g' "${pkgdir}"/usr/lib/modprobe.d/*.conf 2>/dev/null || true
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
