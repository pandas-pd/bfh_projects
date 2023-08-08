using System;

public class CommonDivider 
{
    public static void Main ()
    {
        Int32 number = 0;
        bool dividable = false;

        while (dividable == false)
        {
            number++;
            for (int divider = 1; divider <= 20; divider++)
            {
                if (number % divider != 0)
                {
                    break;
                } 
                if (divider == 20)
                {
                    dividable = true;
                }
            }
        }
        Console.WriteLine("Smallest number divideble by number 1 to 10 is:\n" + number);
    }
}