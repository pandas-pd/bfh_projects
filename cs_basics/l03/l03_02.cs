using System;

public class OneTimesOne
{
    public static void Main ()
    {
        for (int i = 1; i < 37; i++)
        {
            if (i%6 == 0)
            {
                Console.WriteLine(i + "\t");
            } else {
                Console.Write(i + "\t");
            }
        }
    }
}

//test