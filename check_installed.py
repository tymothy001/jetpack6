# -*- coding: utf-8 -*-
import sys



import os
import subprocess
import pkg_resources
import torch
import torchvision
import torchaudio
import tensorrt as trt
import numpy as np

def get_installed_packages():
    """Zwraca listę zainstalowanych pakietów Python."""
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    return installed_packages

def get_system_info():
    """Zwraca informacje o systemie."""
    system_info = {}
    try:
        # Informacje o systemie
        system_info["System"] = os.uname().sysname
        system_info["Node Name"] = os.uname().nodename
        system_info["Release"] = os.uname().release
        system_info["Version"] = os.uname().version
        system_info["Machine"] = os.uname().machine

        # Wersja CUDA
        cuda_version = subprocess.check_output(["nvcc", "--version"]).decode("utf-8")
        system_info["CUDA Version"] = cuda_version.split("release ")[1].split(",")[0]

        # Wersja TensorRT
        system_info["TensorRT Version"] = trt.__version__

        # Wersja PyTorch i zależności
        system_info["PyTorch Version"] = torch.__version__
        system_info["Torchvision Version"] = torchvision.__version__
        #system_info["Torchaudio Version"] = torchaudio.__version__

        # Wersja NumPy
        system_info["NumPy Version"] = np.__version__

        # Wersja JetPack (jeśli dostępna)
        try:
            jetpack_version = subprocess.check_output(["cat", "/etc/nv_tegra_release"]).decode("utf-8")
            system_info["JetPack Version"] = jetpack_version.strip()
        except FileNotFoundError:
            system_info["JetPack Version"] = "Nie znaleziono informacji o JetPack"

    except Exception as e:
        system_info["Error"] = f"Błąd podczas pobierania informacji: {e}"

    return system_info

def main():
    print("🔍 Sprawdzanie zainstalowanych pakietów i informacji o systemie...\n")

    # Pobierz zainstalowane pakiety
    installed_packages = get_installed_packages()
    print("📦 Zainstalowane pakiety Python:")
    for pkg, version in installed_packages.items():
        print(f"- {pkg}: {version}")

    # Pobierz informacje o systemie
    system_info = get_system_info()
    print("\n🖥️ Informacje o systemie:")
    for key, value in system_info.items():
        print(f"- {key}: {value}")

if __name__ == "__main__":
    main()
