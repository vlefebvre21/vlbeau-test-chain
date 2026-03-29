def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else None

if __name__ == "__main__":
    print(add(5,3), subtract(5,3), multiply(5,3), divide(5,3), divide(5,0))
