import os
import torch
import sys
import subprocess

def check_cuda():
    """Sprawdza, czy CUDA i cuDNN są dostępne"""
    if torch.cuda.is_available():
        print("✅ CUDA jest dostępna.")
        print(f"  - Urządzenie: {torch.cuda.get_device_name(0)}")
        print(f"  - Wersja CUDA: {torch.version.cuda}")
    else:
        print("❌ CUDA NIE jest dostępna. Sprawdź sterowniki GPU.")

def check_cudnn():
    """Sprawdza, czy cuDNN działa"""
    try:
        if torch.backends.cudnn.is_available():
            print(f"✅ cuDNN jest dostępne (wersja: {torch.backends.cudnn.version()})")
        else:
            print("❌ cuDNN NIE jest dostępne.")
    except AttributeError:
        print("❌ Problem z cuDNN – brak dostępu.")

def check_torch():
    """Sprawdza, czy PyTorch jest zainstalowany i obsługuje CUDA"""
    try:
        import torch
        print(f"✅ PyTorch jest zainstalowany (wersja: {torch.__version__})")
        if torch.cuda.is_available():
            print("✅ PyTorch obsługuje CUDA.")
        else:
            print("⚠️ PyTorch NIE obsługuje CUDA.")
    except ImportError:
        print("❌ PyTorch NIE jest zainstalowany.")

def check_transformers():
    """Sprawdza, czy Transformers (Hugging Face) jest zainstalowane"""
    try:
        import transformers
        print(f"✅ Transformers jest zainstalowane (wersja: {transformers.__version__})")
    except ImportError:
        print("❌ Transformers NIE jest zainstalowane.")

def check_bitsandbytes():
    """Sprawdza, czy bitsandbytes do kwantyzacji 4-bitowej jest zainstalowane"""
    try:
        import bitsandbytes as bnb
        print("✅ bitsandbytes (4-bitowa kwantyzacja) jest dostępne.")
    except ImportError:
        print("❌ bitsandbytes NIE jest zainstalowane.")

def check_optimum():
    """Sprawdza, czy Optimum (dla optymalizacji modelu) jest zainstalowane"""
    try:
        import optimum
        print("✅ Optimum (dla optymalizacji modeli) jest zainstalowane.")
    except ImportError:
        print("❌ Optimum NIE jest zainstalowane.")

def check_tensorrt():
    """Sprawdza, czy TensorRT jest dostępne"""
    try:
        import tensorrt
        print(f"✅ TensorRT jest zainstalowane (wersja: {tensorrt.__version__})")
    except ImportError:
        print("❌ TensorRT NIE jest zainstalowane.")

def check_onnx():
    """Sprawdza, czy ONNX jest dostępne"""
    try:
        import onnx
        print(f"✅ ONNX jest zainstalowane (wersja: {onnx.__version__})")
    except ImportError:
        print("❌ ONNX NIE jest zainstalowane.")

def check_system_packages():
    """Sprawdza, czy podstawowe pakiety systemowe są zainstalowane"""
    def is_installed(pkg):
        return subprocess.run(["dpkg", "-s", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    
    print("\n📌 Sprawdzanie pakietów systemowych:")
    required_pkgs = ["build-essential", "cmake", "python3-pip", "git"]
    for pkg in required_pkgs:
        if is_installed(pkg):
            print(f"✅ {pkg} jest zainstalowany.")
        else:
            print(f"❌ {pkg} NIE jest zainstalowany.")

def check_all():
    """Uruchamia wszystkie testy"""
    print("🔍 Sprawdzanie środowiska AI na Jetson Orin NX...\n")
    check_cuda()
    check_cudnn()
    check_torch()
    check_transformers()
    check_bitsandbytes()
    check_optimum()
    check_tensorrt()
    check_onnx()
    check_system_packages()
    print("\n✅ Sprawdzenie zakończone!")

if __name__ == "__main__":
    check_all()

