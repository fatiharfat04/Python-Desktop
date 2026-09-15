umur = 20

if umur < 13:
    print("Anak-anak")
elif umur < 18:
    print("Remaja")
else:
    print("Dewasa")

# Operator logika: and, or, not
if umur >= 17 and umur < 60:
    print("Usia produktif")
elif umur >= 60:
    print("Lansia")
else:
    print("Anak-anak")

# Ternary (satu baris)
status = "Dewasa" if umur >= 18 else "Anak"