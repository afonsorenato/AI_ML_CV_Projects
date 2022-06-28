#include <iostream>

int main(){

    system("CLS");

    auto var1 {12};
    auto var2 {13.0};
    auto var3 {14.0f};
    auto var4 {115.0l};
    auto var5 {'e'};

    auto var6{123u};
    auto var7{123ul};
    auto var8{123ll};

    std::cout << sizeof(var1) << std::endl;
    std::cout << sizeof(var2) << std::endl;
    std::cout << sizeof(var3) << std::endl;
    std::cout << sizeof(var4) << std::endl;
    std::cout << sizeof(var5) << std::endl;
    std::cout << sizeof(var6) << std::endl;
    std::cout << sizeof(var7) << std::endl;


    return 0;
}