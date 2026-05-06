n = int(input("Podaj liczbę ocen: "))

oceny = []
for i in range(n):
    ocena = int(input(f"Podaj ocenę {i + 1}: "))
    oceny.append(ocena)

srednia = sum(oceny) / n

print(f"\nŚrednia: {srednia:.2f}")

if srednia >= 3.0:
    print("Uczeń zdał.")
else:
    print("Uczeń nie zdał.")