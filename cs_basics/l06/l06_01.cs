using System;

public class LongCalculation
{
    public static void Main ()
    {
        string LongCalc = "+8 +1 -4 +2 -4 -2 +1 -3 +2 -2 +5 +2 +4 +1 -2 +3 -4 +1 -5 +4 -5 -1 -5 +5 -3 -5 -5 -5 -4 +1 +4 +4 -1 -5 -4 -5 -2 +3 -5 -4 +5 -2 -1 +1 +1 +5 +2 +3 -4 -1 +4 +2 +3 +3 -1 +4 +1 +5 +2 +4 +1 +2 +5 +2 +2 -2 +5 +3 +5 +1 -3 -3 +1 +2 -4 +5 +2 +4 +2 -4 -2 -2 -3 -3 -3 -5 -1 -3 +2 -1 +3 -2 -4 -1 +3 -2 -2 -2 -1 -5 -2 +5 -2 +4";
        string[] CalcElements = LongCalc.Split(' ');
        int Result = 0;

        foreach (String CalcElement in CalcElements)
        {
            Result = Result + Convert.ToInt16(CalcElement);
        }

        Console.WriteLine("Result: " + Result);
    }
}