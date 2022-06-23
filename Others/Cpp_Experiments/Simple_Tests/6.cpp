
// Stopped ad 4.03.49s

#include <iostream>

int main(){

    system("CLS");

    int value1 {10};
    int value2 {-300};

    std::cout << value1 << std::endl;
    std::cout << value2 << std::endl;
    std::cout << "Size of v1: " <<  sizeof(value1) << std::endl;
    std::cout << "Size of v2: " <<  sizeof(value2) << std::endl;

    unsigned int value3 {4};
    signed int value4 {-5};

    return 0;
}