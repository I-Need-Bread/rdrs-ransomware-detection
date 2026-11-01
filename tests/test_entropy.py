from app.core.entropy import calculate_entropy

def test_low_entropy():
    assert calculate_entropy(b"aaaaa") < 1.0

def test_high_entropy():
    assert calculate_entropy(bytes(range(256))) > 7.9