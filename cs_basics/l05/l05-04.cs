using System;

public class RemainderDivision
{
    public static void Main ()
    {
        Int64 SecondsIn = 31719845;

        Int32 Years = Math.Floor(SecondsIn / (3600 * 24 * 365));
        Int32 Days = Math.Floor(SecondsIn / (3600 * 24));
        Int32 Hours = Math.Floor(SecondsIn / 3600);
        Int32 Minutes = Math.Floor(SecondsIn / 60); ;
        Int32 Seconds = 0;



    }
}