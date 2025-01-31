#include <iostream>
#include <cstring>
#include <cstdlib>
#include <ctime>

#include "CStr.cpp"


using namespace std;



int main(){
    
    srand(static_cast<unsigned int>(time(nullptr)));

    CStr a("aaa");
    CStr b("bbb");
    CStr c;

    c = a += b;

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = " << c << endl;


    return 0;
}

