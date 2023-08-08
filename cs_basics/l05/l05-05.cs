using System;

public class SomeStrings
{
    public static void Main ()
    {
        SomeStrings.Q1();
        SomeStrings.Q2();
    }

    public static void Q1 ()
    {
        String Name = "Hans";
        Int16 Age = 16;

        String SomeString = "My name is {0} and I am {1} years old";
        String FormattedString = String.Format(SomeString, Name, Age);

        Console.WriteLine(FormattedString);
    }

    public static void Q2 ()
    {

        Int16 Number = 23;
        Double FloatNumber = 1.0/3.0;
        String Text = "hello";

        String Str0 = "0{0}";
        String Str0F = String.Format(Str0, Number);
        Console.WriteLine(Str0F);

        Double FloatRounded = Math.Round(FloatNumber, 2);
        Console.WriteLine(FloatRounded);

        String Str1 = "***{0}***";
        String Str1F = String.Format(Str1, Text);
        Console.WriteLine(Str1F);
    }
}