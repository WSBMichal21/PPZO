using System;

class Temperatura
{
    static void Main()
    {
        Console.Write("Podaj skalę temperatury C lub F: ");
        string skala = Console.ReadLine();

        Console.Write("Podaj wartość: ");
        double temp = double.Parse(Console.ReadLine());

        if (skala == "C")
            Console.WriteLine(temp * 1.8 + 32 + " °F");
        else if (skala == "F")
            Console.WriteLine((temp - 32) / 1.8 + " °C");
    }
}