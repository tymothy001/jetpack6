import os
import sys
import importlib.util
import torch
import subprocess

# Lista wymaganych pakietów
REQUIRED_PACKAGES = [
    "torch",
    "torchvision",
    "torchaudio",
    "transformers",
    "optimum[onnxruntime]",
    "onnxruntime-gpu",
    "accelerate",
    "bitsandbytes",
    "mnemonic",
    "electrum"
]

# Sprawdza, czy pakiet jest zainstalowany
def is_installed(package):
    spec = importlib.util.find_spec(package)
    return spec is not None

# Sprawdza wersję pakietu
def get_package_version(package):
    try:
        return importlib.import_module(package).__version__
    except:
        return "Nie zainstalowano"

# Sprawdzenie dostępności GPU i TensorRT
def check_tensorrt():
    try:
        import tensorrt
        return f"TensorRT Zainstalowany - wersja: {tensorrt.__version__}"
    except ImportError:
        return "TensorRT NIE zainstalowany!"

def check_gpu():
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        return f"GPU wykryte: {device_name} ({torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB VRAM)"
    else:
        return "GPU NIE wykryte! Sprawdź sterowniki NVIDIA."

# Sprawdzenie Electrum
def check_electrum():
    try:
        output = subprocess.run(["electrum", "--version"], capture_output=True, text=True)
        return f"Electrum zainstalowany - wersja: {output.stdout.strip()}"
    except FileNotFoundError:
        return "Electrum NIE zainstalowany!"

# Sprawdzenie, czy można załadować modele
def check_models():
    try:
        from transformers import AutoModel
        model = AutoModel.from_pretrained("distilbert-base-uncased")
        return "Model BERT można załadować ✔"
    except Exception as e:
        return f"Błąd przy ładowaniu modelu BERT: {e}"

# Diagnostyka systemu
def system_diagnose():
    print("\n🔍 **SPRAWDZANIE KOMPONENTÓW AI DLA JETSON ORIN NX** 🔍\n")

    # Sprawdzanie pakietów Python
    print("📦 **Sprawdzanie wymaganych pakietów:**")
    for package in REQUIRED_PACKAGES:
        status = "✔ Zainstalowano" if is_installed(package) else "❌ BRAK"
        version = get_package_version(package) if is_installed(package) else "N/A"
        print(f"- {package}: {status} (wersja: {version})")

    # GPU i TensorRT
    print("\n🎮 **Sprawdzanie GPU i TensorRT:**")
    print(check_gpu())
    print(check_tensorrt())

    # Electrum
    print("\n💰 **Sprawdzanie Electrum:**")
    print(check_electrum())

    # Sprawdzanie modeli AI
    print("\n🧠 **Testowanie ładowania modeli AI:**")
    print(check_models())

    print("\n✅ **DIAGNOSTYKA ZAKOŃCZONA** ✅\n")

# Uruchomienie diagnostyki
if __name__ == "__main__":
    system_diagnose()

