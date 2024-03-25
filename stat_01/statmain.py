"""Main module."""
def calculate_mean(data):
    return sum(data) / len(data)

def calculate_variance(data):
    mean = calculate_mean(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance