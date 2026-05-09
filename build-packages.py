import yaml
import subprocess
import os
import shutil
import glob

with open("packages.yaml") as f:
    pkgs = yaml.safe_load(f)["packages"]

os.makedirs("/tmp/pkgout", exist_ok=True)

for pkg in pkgs:
    clone_dir = f"/tmp/{pkg}"
    
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    
    subprocess.run(["git", "clone", f"https://aur.archlinux.org/{pkg}.git", clone_dir])
    
    subprocess.run(["chown", "-R", "builder:builder", clone_dir])
    subprocess.run(["su", "-", "builder", "-c", f"cd {clone_dir} && makepkg -s --noconfirm --noprogress --skippgpcheck"])
    
    subprocess.run(f"cp {clone_dir}/*.pkg.tar.zst /tmp/pkgout/ || true", shell=True)
    
    if pkg == "solara-kernel":
        kernel_pkg = [f for f in glob.glob("/tmp/pkgout/solara-kernel-*.pkg.tar.zst") if "-debug-" not in f]
        if kernel_pkg:
            subprocess.run(["sudo", "pacman", "-U", "--noconfirm", kernel_pkg[0]])

print("Done!")
