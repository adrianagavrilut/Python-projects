from itertools import combinations

# Generăm toate combinațiile posibile de 4 numere din cele 16
numere = list(range(1, 17))
comb = list(combinations(numere, 4))

# Verificăm care combinații au suma 34
comb_suma_34 = [c for c in comb if sum(c) == 34]

print("Aceste combinații sunt:")
for c in comb_suma_34:
    print(c)
print(f"Numărul de combinații care au suma 34 este: {len(comb_suma_34)}")
