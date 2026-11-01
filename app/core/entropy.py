import math
from collections import Counter

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    length = len(data)
    counts = Counter(data)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def get_file_entropy(filepath: str, sample_size: int = 65536) -> float:
    try:
        with open(filepath, 'rb') as f:
            data = f.read(sample_size)
            return calculate_entropy(data)
    except Exception:
        return 0.0