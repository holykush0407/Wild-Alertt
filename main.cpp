#include <iostream>
#include <limits.h>
#include <string>
#include <math.h>
#include <cstdlib>
#include <vector>
#include <fstream>
#include <time.h>
#include <windows.h> // For Windows-specific functions
#include <iomanip>  // For setw
#include <limits>   // For numeric_limits
#include <cctype>   // For tolower/toupper
#include <conio.h>  // For _getch()

// Cross-platform clear screen
void clearScreen() {
    system("cls"); // "cls" command for Windows
}

// Cross-platform delay function
void delay(unsigned int ms) {
    Sleep(ms); // Windows Sleep function
}

// Cross-platform gotoxy
void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

// Windows color codes
enum Colors {
    BLACK = 0,
    BLUE = 1,
    GREEN = 2,
    CYAN = 3,
    RED = 4,
    MAGENTA = 5,
    YELLOW = 6,
    WHITE = 7
};

// Set color using Windows console colors
void setColor(const string& color) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    WORD colorCode;
    
    if(color == "BLUE" || color == "blue")
        colorCode = BLUE;
    else if(color == "YELLOW" || color == "yellow")
        colorCode = YELLOW;
    else if(color == "PINK" || color == "pink" || color == "MAGENTA" || color == "magenta")
        colorCode = MAGENTA;
    else if(color == "RED" || color == "red")
        colorCode = RED;
    else if(color == "GREEN" || color == "green")
        colorCode = GREEN;
    else if(color == "VOILET" || color == "VIOLET" || color == "violet")
        colorCode = BLUE;
    else if(color == "AQUA" || color == "aqua")
        colorCode = CYAN;
    else if(color == "ORANGE" || color == "orange")
        colorCode = YELLOW;
    else
        colorCode = WHITE;
    
    SetConsoleTextAttribute(hConsole, colorCode);
}

// Reset text color
void resetColor() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, WHITE);
}

// In the Path function, replace the Unix-specific input handling with Windows version
void Path(float dist, int e, int st, int inter, int final_dest) {
    // ... existing code ...
    
    // Replace the Unix-specific input handling
    gotoxy(10, 39);
    cout << "Press any key to return to main menu...";
    _getch(); // Windows-specific function to get a character without echo
    
    // ... existing code ...
}

// ... existing code ... 