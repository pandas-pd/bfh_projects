using System;

public class Factorial
{
    public static void Main()
    {
        int fact = int.Parse(System.Console.ReadLine());
        int result = 1;

        for (int i = 1; i <= fact; i++)
        {
            result = result * i;
        }

        Console.WriteLine("Factorial of " + fact + " is:\t" + result);
    }
}