# For loop
for i in range(5):          # 0,1,2,3,4
    print(i)

buah = ["apel", "jeruk", "mangga"]
for item in buah:
    print(item)

# While loop
counter = 0
while counter < 5:
    print(counter)
    counter += 1

# break & continue
for i in range(10):
    if i == 5:
        break        # hentikan loop
    if i % 2 == 0:
        continue     # skip iterasi
    print(i)