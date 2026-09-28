
a = 1664525
c = 1013904223
m = 2**32
x = 12345  

print("Números aleatorios generados:")
for _ in range(20):
    x = (a * x + c) % m
    u = x / m
    print(f"{u:.10f}")