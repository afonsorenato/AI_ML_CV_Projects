#include <iostream>

int main(){

    int age;
    std::string full_name;

    std::cout << "Please type your full name: " << std::endl;
    std::getline(std::cin, full_name);

    std::cout << "Tyupe your age: " << std::endl;
    std::cin >> age;
    std::cout << "Hello " << full_name << "! You are " << age << " years old." << std::endl;

}