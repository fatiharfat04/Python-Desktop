def sapa(nama):
    return f"Halo, {nama}!"

print(sapa("Budi"))

# Default parameter
def tambah(a, b=10):
    return a + b

# Multiple return values
def hitung(a, b):
    return a + b, a - b

jumlah, selisih = hitung(5, 3)

# Function dengan *args dan **kwargs
def contoh(*args, **kwargs):
    print(args)      # tuple
    print(kwargs)    # dictionary

# Lambda function
kali = lambda x, y: x * y