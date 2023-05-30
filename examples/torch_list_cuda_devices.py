#!/usr/bin/env python
# Find all CUDA Compute Devices & Print Names per Index
import torch

if torch.cuda.is_available():
    print("CUDA detected, you are rich")
    for device_id in range(torch.cuda.device_count()):
        memory_gb = torch.cuda.get_device_properties(device_id).total_memory / 1000000000
        print(f"Device Index: {device_id} -- {torch.cuda.get_device_name(device_id)} has {memory_gb:.2f}GB of VRAM")

else:
    print("CUDA not detected, fail to be rich")





