using System;

class Kalkulator
{
    static void Main()
    {
        Console.Write("Wybierz liczbę a: ");
        int liczba = int.Parse(Console.ReadLine());

        Console.Write("Wybierz liczbę b: ");
        int liczba2 = int.Parse(Console.ReadLine());

        Console.WriteLine("Wybierz znak + - * /");
        string znak = Console.ReadLine();

        if (znak == "+")
            Console.WriteLine(liczba + liczba2);
        else if (znak == "-")
            Console.WriteLine(liczba - liczba2);
        else if (znak == "*")
            Console.WriteLine(liczba * liczba2);
        else if (znak == "/")
            Console.WriteLine((double)liczba / liczba2);
    }
}