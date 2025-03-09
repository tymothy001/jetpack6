import torch
import time

# Przykładowe obliczenia na GPU
x = torch.randn(10000, 10000, device="cuda")
y = torch.randn(10000, 10000, device="cuda")

# Pomiar czasu operacji macierzowej
torch.cuda.synchronize()
start_time = time.time()
z = torch.mm(x, y)
torch.cuda.synchronize()
end_time = time.time()

print(f"Czas obliczeń na GPU: {end_time - start_time:.6f} s")

