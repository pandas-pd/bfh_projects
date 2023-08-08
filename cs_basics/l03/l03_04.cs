using System;

public class Sundays
{
    public static void Main()
    {
        DateTime StartDate = new DateTime(1900, 01, 01);
        DateTime EndDate = new DateTime(2019, 12, 31);
        Int64 SundayCount = 0;

         while (StartDate.AddDays(1) <= EndDate)
        {

            if (StartDate.DayOfWeek == DayOfWeek.Sunday) 
            {
                SundayCount += 1;
            };

            StartDate = StartDate.AddDays(1);

        }

        Console.WriteLine("Number of Sundays:\t" + SundayCount);
    }
}