using System;
using System.Linq;
using System.Collections;
using System.Collections.Generic;

public class NimGame 
{
    public static void Main ()
    {
        //main func
        string welcomeMessage = "\n\nGame NIM - Main Menu\nThe commands are as following\nn\tNew game\nq\tQuit the game\n1,2\tValid game inputs\n";
        string goodbyeMessage = "Thanks for playing. Goodbye";
        int heap = 20;
        bool gameRunning = false;

        //greeeitngs
        Console.WriteLine(welcomeMessage);

        //return values
        char uiChar;
        int uiInt;
        bool numeric;
        NimGame.UserInput(gameRunning, out uiChar, out uiInt, out numeric);

        while (numeric == true){
            NimGame.UserInput(gameRunning, out uiChar, out uiInt, out numeric);
        }

        //processing the ui commands
        if (uiChar == 'n'){
            NimGame.Game();
        }
        else if (uiChar == 'q'){
            Console.WriteLine(goodbyeMessage);
            return;
        }
    }

    public static void Game() {

        int heap = 20;
        char uiChar;
        int uiInt;
        bool numeric;
        string lastMove = "AI";

        Console.WriteLine("\nNew game started\n\nHeap:\t{0}", heap);

        while (heap > 0){

            //player move
            NimGame.UserInput(true, out uiChar, out uiInt, out numeric);

            if (numeric == false) {
                if (uiChar == 'q'){
                    NimGame.Main();
                    return;
                    break;
                }
                else if (uiChar == 'n'){
                    heap = 20;
                    NimGame.Game();
                }
            }
            lastMove = "AI";
            heap = heap - uiInt;
            if (heap <= 0) {
                break;
            }
            Console.WriteLine("Heap:\t\t{0}", heap);

            //ai move
            int aiInt = AiInput(heap);
            lastMove = "You";
            heap = heap -aiInt;
            if (heap <= 0) {
                break;
            }
            Console.WriteLine("AI input:\t{0}\nHeap:\t{1}", aiInt, heap);
        }

        Console.WriteLine("{0} WINS!\n Returning to Menu.", lastMove);
        NimGame.Main();
    }

    public static void UserInput (bool gameRunning, out char userInputChar, out int userInputInt, out bool isNumeric){

        Console.Write("Your input:\t");
        string userInput = Console.ReadLine();
        bool validInput = NimGame.UserInputValidation(userInput);

        while (validInput == false) {
            Console.Write("Your input:\t");
            userInput = Console.ReadLine();
            validInput = NimGame.UserInputValidation(userInput);
        }

        userInputInt = 0;
        userInputChar = '0';
        isNumeric = int.TryParse(userInput, out userInputInt);

        if (isNumeric == false) {
            userInputChar = char.Parse(userInput);
        }
    }

    public static bool UserInputValidation (string userInput){

        char userInputChar;
        bool isChar = char.TryParse(userInput, out userInputChar);

        List<char> validInputsList = new List<char>();
        string validInputs = "12nq";
        validInputsList.AddRange(validInputs);

        if (isChar & validInputs.Contains(userInputChar)) {
            return true;
        }
        else{
            return false;
        }
    }

    public static int AiInput (int heap){
        //ai that bitch
        Random rnd = new Random();
        int aiInt  = rnd.Next(1, 3);
        return aiInt;
    }
}