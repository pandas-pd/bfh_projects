using System;
using System.Linq;

public class CharCount{
    public static void Main (){

        string theInput= "GZOOEHHCTRJYXXVUECLTFFFNKBHYHXXBYYYUUEYYGGLOHHGAAAASCWARRCHWYXXLBIZAAAXXLIWWWWWDDDDDRRHMMPPUUUHZNKKTXACCBJEYUIKHZZDPAKEMRCGCFFHHIIIFDDUUUGFFHR";
        char[] charList = theInput.ToCharArray();

        int count = 0;
        char lastChar = '0';

        for (int i = 0; i < charList.Length; i ++) {

            if (charList[i] == lastChar) {
                count += 1;
            }
            lastChar = charList[i];
        }
        Console.WriteLine("Result:\t{0}", count);
    }
}