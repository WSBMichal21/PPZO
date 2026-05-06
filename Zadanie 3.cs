using System;

class Oceny
{
    static void Main()
    {
        Console.Write("Podaj liczbę ocen: ");
        int n = int.Parse(Console.ReadLine());

        int[] oceny = new int[n];
        for (int i = 0; i < n; i++)
        {
            Console.Write($"Podaj ocenę {i + 1}: ");
            oceny[i] = int.Parse(Console.ReadLine());
        }

        double srednia = 0;
        foreach (int ocena in oceny)
            srednia += ocena;
        srednia /= n;

        Console.WriteLine($"\nŚrednia: {srednia:F2}");

        if (srednia >= 3.0)
            Console.WriteLine("Uczeń zdał.");
        else
            Console.WriteLine("Uczeń nie zdał.");
    }
}