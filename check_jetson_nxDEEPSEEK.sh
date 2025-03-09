#!/bin/bash

# Funkcja do animacji ramki
animate_frame() {
    local delay=0.1
    local frames=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
    while true; do
        for frame in "${frames[@]}"; do
            printf "\r${frame} %s" "$1"
            sleep $delay
        done
    done
}

# Funkcja do wyświetlania ramki
print_frame() {
    local text=$1
    local color=$2
    local length=${#text}
    local border=$(printf '%0.s═' $(seq 1 $((length + 2))))
    echo -e "${color}╔${border}╗"
    echo -e "║ ${text} ║"
    echo -e "╚${border}╝\e[0m"
}

# Kolory NVIDIA
COLOR_NVIDIA_GREEN="\e[32m"
COLOR_NVIDIA_GRAY="\e[37m"
COLOR_NVIDIA_BLACK="\e[30m"

# Animacja ładowania
animate_frame "Pobieranie informacji o systemie..." &
animation_pid=$!
sleep 2
kill $animation_pid
wait $animation_pid 2>/dev/null

# Informacje o systemie
SYSTEM_INFO=$(uname -s)
NODE_NAME=$(uname -n)
RELEASE=$(uname -r)
VERSION=$(uname -v)
MACHINE=$(uname -m)
CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $6}')
TENSORRT_VERSION=$(dpkg -l | grep tensorrt | awk '{print $3}' | head -n 1)
PYTORCH_VERSION=$(python3 -c "import torch; print(torch.__version__)" 2>/dev/null || echo "Nie zainstalowano")
ONNX_VERSION=$(python3 -c "import onnxruntime; print(onnxruntime.__version__)" 2>/dev/null || echo "Nie zainstalowano")
TORCHVISION_VERSION=$(python3 -c "import torchvision; print(torchvision.__version__)" 2>/dev/null || echo "Nie zainstalowano")
JETPACK_VERSION=$(dpkg -l | grep "jetpack" | awk '{print $3}' | head -n 1)

# Wyświetlanie informacji o systemie
print_frame "Informacje o systemie" $COLOR_NVIDIA_GREEN
echo -e "${COLOR_NVIDIA_GRAY}System: ${SYSTEM_INFO}"
echo -e "Node Name: ${NODE_NAME}"
echo -e "Release: ${RELEASE}"
echo -e "Version: ${VERSION}"
echo -e "Machine: ${MACHINE}"
echo -e "CUDA Version: ${CUDA_VERSION}"
echo -e "TensorRT Version: ${TENSORRT_VERSION}"
echo -e "PyTorch Version: ${PYTORCH_VERSION}"
echo -e "ONNX Runtime Version: ${ONNX_VERSION}"
echo -e "Torchvision Version: ${TORCHVISION_VERSION}"
echo -e "JetPack Version: ${JETPACK_VERSION}\e[0m"

# Informacje o CUDA
CUDA_AVAILABLE=$(python3 -c "import torch; print(torch.cuda.is_available())" 2>/dev/null || echo "False")

# Wyświetlanie informacji o CUDA
print_frame "Informacje o CUDA" $COLOR_NVIDIA_GREEN
echo -e "${COLOR_NVIDIA_GRAY}torch.cuda: ${CUDA_AVAILABLE}\e[0m"

# Informacje o bibliotekach Python obsługujących CUDA
print_frame "Informacje o bibliotekach Python obsługujących CUDA" $COLOR_NVIDIA_GREEN
echo -e "${COLOR_NVIDIA_GRAY}Sprawdzanie dostępności bibliotek...\e[0m"

# Lista bibliotek do sprawdzenia
LIBRARIES=("torch" "torchvision" "torchaudio" "onnxruntime-gpu" "tensorflow" "tensorrt")

# Sprawdzanie dostępności bibliotek
for lib in "${LIBRARIES[@]}"; do
    if python3 -c "import ${lib}" 2>/dev/null; then
        echo -e "${COLOR_NVIDIA_GRAY}${lib}: Dostępny\e[0m"
    else
        echo -e "${COLOR_NVIDIA_GRAY}${lib}: Nie zainstalowano\e[0m"
    fi
done

# Wykaz bibliotek do zainstalowania
print_frame "Wykaz bibliotek do zainstalowania" $COLOR_NVIDIA_GREEN
echo -e "${COLOR_NVIDIA_GRAY}Jeśli któreś z powyższych bibliotek nie są dostępne, zainstaluj je za pomocą pip:\e[0m"
echo -e "${COLOR_NVIDIA_GRAY}pip install torch torchvision torchaudio onnxruntime-gpu tensorflow tensorrt\e[0m"
