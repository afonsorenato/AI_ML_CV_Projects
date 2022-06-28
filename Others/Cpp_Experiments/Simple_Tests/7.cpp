#include <iostream>


int main(){
    system("CLS");

    bool red_light {true};
    bool green_light{false};

    if(green_light){
        std::cout << "Stop!\n" << std::endl;
    }else{
        std::cout << "Go through! \n" << std::endl;
    }

    std::cout << "size of: " << sizeof(bool) << std::endl;
    std::cout << red_light << std::endl;
    std::cout << green_light << std::endl;


    return 0;

}