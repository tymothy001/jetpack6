import torch
from timeit import default_timer as timer


# check for cuda availability
print("Cuda: ", torch.cuda.is_available())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Device: ", device)


#GPU 
b = torch.ones(4000,4000).cuda() # Create matrix on GPU memory
start_time = timer() 
for _ in range(1000): 
    b += b 
elapsed_time = timer() - start_time 

print('GPU time = ',elapsed_time)


#CPU
a = torch.ones(4000,4000) # Create matrix on CPU memory
start_time = timer()
for _ in range(1000):
    a += a
elapsed_time = timer() - start_time

print('CPU time = ',elapsed_time)
