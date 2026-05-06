skala = input("Podaj skalę temperatury C lub F: ")
temp = int(input("Podaj Wartość: "))
if skala == "C":
    print(temp* 1.8 + 32,"°F")
elif skala == "F":
    print(temp-32/1.8,"°C")