import subprocess
import sys
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

def install_required_packages():
    """Instaluje wymagane pakiety"""
    print(colored("Instalowanie zależności systemowych...", "blue"))
    packages = [
        "python3-pip", "libopenblas-dev", "libjpeg-dev", "libpng-dev", "tensorrt", "libnvinfer8", "libnvinfer-plugin8", "libnvinfer-dev",
        "nvidia-jetpack", "libopencv-dev", "python3-opencv"
    ]
    run_command(f"sudo apt update && sudo apt install -y {' '.join(packages)}")

def uninstall_old_pytorch():
    """Usuwa stare wersje PyTorch, torchvision, torchaudio"""
    print(colored("Usuwanie starych wersji PyTorch...", "blue"))
    run_command("pip3 uninstall -y torch torchvision torchaudio")
    run_command("rm -rf ~/.local/lib/python3.8/site-packages/torch*")

def install_pytorch():
    """Instaluje PyTorch, torchvision, torchaudio dla Jetson Orin NX"""
    print(colored("Pobieranie i instalacja PyTorch dla Jetson Orin NX...", "blue"))
    torch_whl = "https://developer.download.nvidia.com/compute/redist/jp/v51/pytorch/torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl"
    torchvision_whl = "https://developer.download.nvidia.com/compute/redist/jp/v51/pytorch/torchvision-0.15.2+nv23.05-cp38-cp38-linux_aarch64.whl"
    torchaudio_whl = "https://developer.download.nvidia.com/compute/redist/jp/v51/pytorch/torchaudio-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl"
    
    run_command(f"wget {torch_whl} && pip3 install torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl")
    run_command(f"wget {torchvision_whl} && pip3 install torchvision-0.15.2+nv23.05-cp38-cp38-linux_aarch64.whl")
    run_command(f"wget {torchaudio_whl} && pip3 install torchaudio-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl")

def verify_installations():
    """Sprawdza, czy wszystkie komponenty są poprawnie zainstalowane"""
    print(colored("\nSprawdzanie instalacji...", "green"))
    components = {
        "CUDA": "nvcc --version",
        "TensorRT": "trtexec --version",
        "cuDNN": "dpkg -l | grep libcudnn8",
        "JetPack": "dpkg -l | grep nvidia-jetpack",
        "PyTorch": "python3 -c 'import torch; print(torch.__version__)'",
        "CUDA w PyTorch": "python3 -c 'import torch; print(torch.version.cuda)'",
        "torchvision": "python3 -c 'import torchvision; print(torchvision.__version__)'",
        "torchaudio": "python3 -c 'import torchaudio; print(torchaudio.__version__)'",
        "OpenCV": "python3 -c 'import cv2; print(cv2.__version__)'"
    }
    
    for component, command in components.items():
        output = run_command(command)
        if output.strip():
            print(f"{component}: {colored('Zainstalowany', 'green')}")
        else:
            print(f"{component}: {colored('Nie znaleziono', 'red')}")

if __name__ == "__main__":
    install_required_packages()
    uninstall_old_pytorch()
    install_pytorch()
    verify_installations()

