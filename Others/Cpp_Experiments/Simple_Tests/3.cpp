#include <iostream>
#include <string>

int main(){

    int age = 3;
    int number;
    std::string full_name;

    std::cout << "Please type your full name:  " << std::endl; 
    std::getline(std::cin, full_name);

    std::cout << "Type your age: " << std::endl;
    std::cin >> age;
    std::cout << "Hello " << full_name << "! You are " << age << " years old." << std::endl;

    std::cerr << "Error message: wrong!" << std::endl;
    std::clog << "Log message \n" << std::endl;

    return 0;
}