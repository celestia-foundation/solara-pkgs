import yaml
import subprocess
import os

with open("packages.yaml") as f:
    pkgs = yaml.safe_load(f)["packages"]

os.makedirs("/tmp/pkgout", exist_ok=True)

for pkg in pkgs:
    clone_dir = f"/tmp/{pkg}"
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
        ["su", "-", "builder", "-c", f"cd {clone_dir} && makepkg -s --noconfirm --noprogress"]
    )
    if result.returncode != 0:
        print(f"SKIP: build failed for {pkg}")
        continue

    subprocess.run(f"cp {clone_dir}/*.pkg.tar.zst /tmp/pkgout/ || true", shell=True)

print("Done!")
