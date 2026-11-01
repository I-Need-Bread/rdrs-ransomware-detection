import os
import time
import pathlib

sandbox = pathlib.Path('data/sandbox')
sandbox.mkdir(parents=True, exist_ok=True)

print("Creating normal files...")
for i in range(30):
    (sandbox / f"test_file_{i}.txt").write_text("This is a normal document.")
time.sleep(2)

print("🚨 Simulating Ransomware Attack...")
for f in list(sandbox.glob("*.txt")):
    f.write_bytes(os.urandom(20000)) 
    f.rename(f.with_suffix('.locked')) 
    time.sleep(0.1) # <--- ADD THIS LINE
print("Simulation complete.")