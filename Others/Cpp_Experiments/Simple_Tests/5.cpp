#include <iostream>

void print(int my_var){
    std::cout << my_var << std::endl;
}

int main(){

    system("CLS");

    int elephant_count;

    int lion_count{};
    print(lion_count);
    int dog_count {10};
    print(dog_count);
    int cat_count {15};
    print(cat_count);

    int domesticated_animals {dog_count + cat_count};
    print(domesticated_animals);

    return 0;
}