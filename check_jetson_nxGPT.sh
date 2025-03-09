#!/bin/bash
# Skrypt NVIDIA Info z ulepszonymi ramkami (grube linie) i rozszerzonym sprawdzaniem modułów
# Autor: Arisa
# Tomaszu, skrypt prezentuje informacje o systemie, wersjach bibliotek, akceleracji GPU
# oraz dodatkowe moduły i przykładowe komendy instalacyjne.

# Ustawienia kolorów (zielony w stylu NVIDIA)
NV_GREEN="\e[1;32m"
NV_RESET="\e[0m"

# Znaki ramki - grube linie
TL="┏"   # top left
TR="┓"   # top right
BL="┗"   # bottom left
BR="┛"   # bottom right
HOR="━"  # horizontal
VER="┃"  # vertical
MIDL="┣" # middle left
MIDR="┫" # middle right

# Funkcja animacji spinnera
animate_spinner() {
  local duration=$1
  local spinstr='|/-\'
  local end_time=$(( $(date +%s) + duration ))
  while [ $(date +%s) -lt $end_time ]; do
    for (( i=0; i<${#spinstr}; i++ )); do
      printf "\r${NV_GREEN}Przetwarzanie... ${spinstr:$i:1}${NV_RESET}"
      sleep 0.1
    done
  done
  printf "\r"
}

# Funkcja drukująca ramkę z tytułem i zawartością
print_frame() {
  local title="$1"
  shift
  local content=("$@")
  # Oblicz maksymalną długość linii (dla estetyki ramki)
  local max_length=${#title}
  for line in "${content[@]}"; do
    if [ ${#line} -gt $max_length ]; then
      max_length=${#line}
    fi
  done
  # Dodaj margines (2 spacje po obu stronach)
  local frame_width=$((max_length + 4))
  local border=$(printf '%*s' "$frame_width" '' | tr ' ' "$HOR")
  
  # Top border
  echo -e "${NV_GREEN}${TL}${border}${TR}${NV_RESET}"
  # Wycentrowany tytuł (dodajemy dwie spacje marginesu)
  local title_padding_left=$(( (max_length - ${#title}) / 2 ))
  local title_padding_right=$(( max_length - ${#title} - title_padding_left ))
  local title_line=$(printf "%*s%s%*s" $title_padding_left "" "$title" $title_padding_right "")
  printf "${NV_GREEN}${VER}  %s  ${VER}${NV_RESET}\n" "$title_line"
  # Separator
  echo -e "${NV_GREEN}${MIDL}${border}${MIDR}${NV_RESET}"
  # Zawartość
  for line in "${content[@]}"; do
    printf "${NV_GREEN}${VER}  %-$(($max_length))s  ${VER}${NV_RESET}\n" "$line"
  done
  # Bottom border
  echo -e "${NV_GREEN}${BL}${border}${BR}${NV_RESET}"
}

# Funkcja pobierająca wersję modułu Pythona lub zwracająca False wraz z komendą instalacyjną
get_py_version() {
    local module=$1
    local install_cmd=$2
    version=$(python3 -c "import $module; print(getattr($module, '__version__', 'Brak'))" 2>/dev/null)
    if [ $? -ne 0 ]; then
         echo "False | $install_cmd"
    else
         echo "$version"
    fi
}

# Funkcja sprawdzająca dostępność CUDA w PyTorch
check_torch_cuda() {
    result=$(python3 -c "import torch; print(torch.cuda.is_available())" 2>/dev/null)
    if [ $? -ne 0 ]; then
      echo "False | pip3 install torch"
    else
      echo "$result"
    fi
}

# Pobranie informacji o systemie
sys_system=$(uname -s)
sys_nodename=$(uname -n)
sys_release=$(uname -r)
sys_version=$(uname -v)
sys_machine=$(uname -m)

# Informacje o CUDA przy użyciu nvcc
if command -v nvcc &> /dev/null; then
  cuda_info=$(nvcc --version | head -n 4 | tr '\n' ' ')
else
  cuda_info="False | sudo apt install nvidia-cuda-toolkit"
fi

# Informacje o TensorRT (przy użyciu dpkg)
if command -v dpkg &> /dev/null; then
  tensorrt_info=$(dpkg -l | grep -i 'tensorrt' | head -n 1)
  if [ -z "$tensorrt_info" ]; then
    tensorrt_info="False | postępuj zgodnie z dokumentacją NVIDIA dla TensorRT"
  fi
else
  tensorrt_info="False | Sprawdź menedżera pakietów lub instalację TensorRT"
fi

# Informacje o JetPack (dla urządzeń Jetson)
if command -v jetson_release &> /dev/null; then
  jetpack_info=$(jetson_release | grep -i 'JetPack' | head -n 1)
  if [ -z "$jetpack_info" ]; then
    jetpack_info="False | Zainstaluj JetPack"
  fi
else
  jetpack_info="False | Zainstaluj JetPack dla urządzeń Jetson"
fi

# Pobranie wersji bibliotek Python
torch_version=$(get_py_version torch "pip3 install torch")
torchaudio_version=$(get_py_version torchaudio "pip3 install torchaudio")
torchvision_version=$(get_py_version torchvision "pip3 install torchvision")
tensorflow_version=$(get_py_version tensorflow "pip3 install tensorflow")
onnxruntime_version=$(get_py_version onnxruntime "pip3 install onnxruntime-gpu")

# Sprawdzenie dostępności akceleracji GPU w PyTorch
torch_cuda=$(check_torch_cuda)

# Sprawdzanie dodatkowych modułów:
# NVIDIA SMI
if command -v nvidia-smi &> /dev/null; then
    nvidia_smi_info=$(nvidia-smi --query-gpu=name,driver_version --format=csv,noheader | head -n 1)
else
    nvidia_smi_info="False | Zainstaluj sterowniki NVIDIA"
fi

# Dodatkowe moduły Python dla GPU
cupy_version=$(get_py_version cupy "pip3 install cupy")
pycuda_version=$(get_py_version pycuda "pip3 install pycuda")
numba_version=$(get_py_version numba "pip3 install numba")

# Przygotowanie sekcji informacji o systemie
system_info=(
  "System: $sys_system"
  "Node Name: $sys_nodename"
  "Release: $sys_release"
  "Version: $sys_version"
  "Machine: $sys_machine"
  "CUDA Info: $cuda_info"
  "TensorRT: $tensorrt_info"
  "JetPack: $jetpack_info"
)

# Przygotowanie sekcji wersji bibliotek
libraries_info=(
  "PyTorch: $torch_version"
  "Torchvision: $torchvision_version"
  "Torchaudio: $torchaudio_version"
  "TensorFlow: $tensorflow_version"
  "ONNX Runtime: $onnxruntime_version"
)

# Przygotowanie sekcji dotyczącej akceleracji GPU
gpu_info=(
  "torch.cuda: $torch_cuda"
)

# Przygotowanie sekcji z dodatkowymi modułami
additional_info=(
  "NVIDIA SMI: $nvidia_smi_info"
  "CuPy: $cupy_version"
  "PyCUDA: $pycuda_version"
  "Numba: $numba_version"
)

# Przygotowanie sekcji z przykładowymi komendami instalacyjnymi
install_commands=(
  "pip3 install torch torchvision torchaudio"
  "pip3 install tensorflow"
  "pip3 install onnxruntime-gpu"
  "pip3 install cupy"
  "pip3 install pycuda"
  "pip3 install numba"
  "# Dla TensorRT: postępuj zgodnie z dokumentacją NVIDIA Jetson"
)

clear

# Animacja startowa
echo -e "${NV_GREEN}Inicjalizacja skryptu NVIDIA Info...${NV_RESET}"
animate_spinner 2

# Drukowanie sekcji z informacjami
print_frame "Informacje o systemie" "${system_info[@]}"
echo ""
print_frame "Wersje bibliotek" "${libraries_info[@]}"
echo ""
print_frame "Akceleracja GPU" "${gpu_info[@]}"
echo ""
print_frame "Dodatkowe moduły GPU" "${additional_info[@]}"
echo ""
print_frame "Komendy instalacyjne" "${install_commands[@]}"
echo ""

# Animacja końcowa
echo -e "${NV_GREEN}Operacja zakończona. Dziękuję za korzystanie, Tomaszu!${NV_RESET}"

