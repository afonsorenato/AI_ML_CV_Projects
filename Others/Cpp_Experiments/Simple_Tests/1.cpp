#include <iostream>

int addNumbers(int first_number, int second_number){
    int sum = first_number + second_number;
    return sum;
    
}

int func1()
{
    int firstNumber = 12;
    int secondNumber = 9;

    int sum =  firstNumber + secondNumber;

    std::cout << "The sum is: " << sum << std::endl;
    std::cout << "The sum is: " << addNumbers(23, 8) << std::endl;

    return 0;
}

int main()
{

    func1();

    return 0;
}