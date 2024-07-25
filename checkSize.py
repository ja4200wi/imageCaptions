import os
import sys
import site
from pathlib import Path

def get_package_size(package_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(package_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024

if __name__ == "__main__":
    site_packages = site.getsitepackages()[0]
    packages = [d for d in os.listdir(site_packages) if os.path.isdir(os.path.join(site_packages, d))]

    package_sizes = {}
    for package in packages:
        package_path = os.path.join(site_packages, package)
        package_size = get_package_size(package_path)
        package_sizes[package] = package_size

    sorted_packages = sorted(package_sizes.items(), key=lambda x: x[1], reverse=True)
    for package, size in sorted_packages:
        print(f"{package}: {human_readable_size(size)}")
