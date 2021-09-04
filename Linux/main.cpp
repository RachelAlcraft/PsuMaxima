#include <iostream>
#include "Ccp4.h"

int main(int, char**) 
{
        Ccp4 myCcp4("1rae");
        std::cout << myCcp4.getPdbCode() << " " << myCcp4.getResolution() << " " << myCcp4.isLoaded() << "\n";
}
