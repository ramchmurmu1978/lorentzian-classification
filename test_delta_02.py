import  os
import pandas as pd

file_path = "data/processed/BTCUSD_1h_proc.csv"

print("\nFile exists :", os.path.exists(file_path))
print("File path: ", file_path)