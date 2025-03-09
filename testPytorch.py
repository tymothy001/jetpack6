import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("Number of GPUs:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))
    x = torch.rand(3, 3).cuda()
print(x)
print(torch.backends.cudnn.enabled)
print(torch.backends.cudnn.version())
