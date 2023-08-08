using System;

public class SomeMath
{
    public static void Main()
    {
        Int16 a = 2 + 2;
        Int16 b = 3 * 2;
        double c = Math.Pow(3,3);

        System.Console.WriteLine(c);
        System.Console.WriteLine("Pi: \t" + Math.PI);
        System.Console.WriteLine("Cos of 1:\t" + Math.Cos(1));
        System.Console.WriteLine("Rounding:\t" + Math.Round(2.3456, 1));

    }
}
