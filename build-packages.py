import yaml
import subprocess
import os
import shutil

with open("packages.yaml") as f:
    pkgs = yaml.safe_load(f)["packages"]

os.makedirs("/tmp/pkgout", exist_ok=True)

for pkg in pkgs:
    clone_dir = f"/tmp/{pkg}"
    
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    
    # Clone from AUR
    subprocess.run(["git", "clone", f"https://aur.archlinux.org/{pkg}.git", clone_dir])
    
    # Build
    subprocess.run(["chown", "-R", "builder:builder", clone_dir])
    subprocess.run(["su", "-", "builder", "-c", f"cd {clone_dir} && makepkg -s --noconfirm --noprogress --skippgpcheck"])
    
    # Copy package
    subprocess.run(f"cp {clone_dir}/*.pkg.tar.zst /tmp/pkgout/ || true", shell=True)
    
    # Install kernel AFTER building so headers can find it
    if pkg == "solara-kernel":
        subprocess.run(["sudo", "pacman", "-U", "--noconfirm", f"/tmp/pkgout/solara-kernel-" + "7.0.5-1-x86_64.pkg.tar.zst"])

print("Done!")
