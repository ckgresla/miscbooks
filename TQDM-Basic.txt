# Misc - Really nice progress bar
from tqdm.notebook import tqdm

for i in tqdm(range(1500000000), desc='Progress Bar'):
    i = i+1
