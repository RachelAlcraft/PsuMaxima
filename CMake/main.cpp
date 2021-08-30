#include <iostream>
#include "Ccp4.h"

using namespace std;

int main(int, char**) {
    std::cout << "Hello, world!\n";

    Ccp4 c4("4e9s.ccp4", "");
	cout << "Resolution is " << c4.Resolution() << endl;
	cout << "Success?" << c4.Loaded() << endl;

        
}
