#include <iostream>
#include "Ccp4.h"

int main(int, char**) 
{
    /******   WINDOWS SPECIFIC SETTINGS  ***************/
    string ccp4directory = "/d/projects/u/ab002/Thesis/PhD/Data/Ccp4/";
    /***************************************************/

        Ccp4 myCcp4("1ejg",ccp4directory);
        std::cout << myCcp4.getPdbCode() << " " << myCcp4.getResolution() << " " << myCcp4.isLoaded() << "\n";
}
