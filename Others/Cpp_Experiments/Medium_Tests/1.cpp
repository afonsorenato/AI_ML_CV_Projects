#include <iostream>
#include <iomanip>
#include <ios> 

int main(){

    system("CLS");

    int col_width = 10;

    std::cout << "Hello" << std::endl;
    std::cout << "Hello" << std::endl;
    std::cout << std::setw(col_width) << "Hello" << std::endl;



    return 0;
}