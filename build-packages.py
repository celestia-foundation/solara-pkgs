import yaml
import subprocess
import os
import shutil

with open("packages.yaml") as f:
    pkgs = yaml.safe_load(f)["packages"]

os.makedirs("/tmp/pkgout", exist_ok=True)

# Build solara-kernel FIRST (needed by headers)
kernel_built = False
for pkg in pkgs:
    clone_dir = f"/tmp/{pkg}"
    
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    
    # Clone from AUR
    result = subprocess.run(
        ["git", "clone", f"https://aur.archlinux.org/{pkg}.git", clone_dir]
    )
    if result.returncode != 0:
        print(f"SKIP: failed to clone {pkg}")
        continue
    
    # Build
    subprocess.run(["chown", "-R", "builder:builder", clone_dir], check=True)
    result = subprocess.run(
        ["su", "-", "builder", "-c", f"cd {clone_dir} && makepkg -s --noconfirm --noprogress --skippgpcheck"]
    )
    if result.returncode != 0:
        print(f"SKIP: build failed for {pkg}")
        continue
    
    # Copy package
    subprocess.run(f"cp {clone_dir}/*.pkg.tar.zst /tmp/pkgout/ || true", shell=True)
    
    # Install kernel FIRST so headers can find it
    if pkg == "solara-kernel":
        for f in os.listdir("/tmp/pkgout"):
            if f.endswith(".pkg.tar.zst") and "debug" not in f:
                subprocess.run(["chown", "root:root", f"/tmp/pkgout/{f}"])
                subprocess.run(["sudo", "pacman", "-U", "--noconfirm", f"/tmp/pkgout/{f}"])
                kernel_built = True

print("Done!")
