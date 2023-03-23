# Find all CUDA Compute Devices & Print Names per Index
import torch

if torch.cuda.is_available():
    print("CUDA detected, you are rich")
    for device_id in range(torch.cuda.device_count()):
        print(f"Device Index: {device_id} -- {torch.cuda.get_device_name(device_id)}")

else:
    print("CUDA not detected, not rich")


