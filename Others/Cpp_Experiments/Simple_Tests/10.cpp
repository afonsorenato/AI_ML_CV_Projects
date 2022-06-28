#include <iostream>

void print(int text_str){
    std::cout << text_str << std::endl;
}

int main(){
    system("CLS");

    int number1{2};
    int number2{7};

    int result = number1 + number2;
    std::cout << "Results1: " << result << std:: endl;

    int result2 = number2 - number1;
    print(result2);


    return 0;
}