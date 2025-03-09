import subprocess
import re
import os
from termcolor import colored

def run_command(command):
    """Uruchamia komendę i zwraca wynik"""
    try:
        print(colored(f"Uruchamianie: {command}", "cyan"))
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(colored(f"Wynik:\n{result.stdout}", "yellow"))
        return result.stdout
    except Exception as e:
        print(colored(f"Błąd: {e}", "red"))
        return ""

def check_gpu_usage():
    """Sprawdza użycie GPU"""
    output = run_command("tegrastats | head -n 1")
    gpu_usage = re.search(r'GR3D_FREQ (\d+)%', output)
    if gpu_usage:
        print(f"GPU Użycie: {colored(gpu_usage.group(1) + '%', 'green')}")
    else:
        print(colored("GPU nieaktywny lub brak danych", "red"))

def check_tops_usage():
    """Sprawdza wykorzystanie TOPS"""
    output = run_command("jtop | head -n 20")
    tops_usage = re.search(r'TOPS\s+:\s+(\d+\.\d+)', output)
    if tops_usage:
        print(f"Aktualne TOPS: {colored(tops_usage.group(1), 'green')}")
    else:
        print(colored("Brak danych o TOPS", "red"))

def check_components():
    """Sprawdza kluczowe komponenty Jetsona"""
    components = {
        "CUDA": "nvcc --version",
        "TensorRT": "trtexec --version",
        "cuDNN": "dpkg -l | grep libcudnn8",
        "JetPack": "dpkg -l | grep nvidia-jetpack",
        "PyTorch": "python3 -c 'import torch; print(torch.__version__)'",
        "OpenCV": "python3 -c 'import cv2; print(cv2.__version__)'"
    }

    print("\nSprawdzanie komponentów:\n")
    for component, command in components.items():
        output = run_command(command)
        if output.strip():
            print(f"{component}: {colored('Zainstalowany', 'green')}")
        else:
            print(f"{component}: {colored('Nie znaleziono', 'red')}")

if __name__ == "__main__":
    print(colored("Sprawdzanie statusu Jetson Orin NX 16GB...", "yellow"))
    check_gpu_usage()
    check_tops_usage()
    check_components()

