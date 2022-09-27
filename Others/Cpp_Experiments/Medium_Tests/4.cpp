#include <iostream>
#include <iomanip>
#include <ios> 

using namespace std;


int main(){

    int age = 19;
    double gpa = 2.7;
    string name = "Mike";

    cout << "Age: " << &age << endl;;
    cout << "Gpa: " << &gpa << endl;;
    cout << "Name: " << &name << endl;;


    return 0;
}