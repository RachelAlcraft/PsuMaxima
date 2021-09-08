#include <iostream>
#include "Ccp4.h"

int main(int argc, char* argv[]) 
{
    /******   INPUTS  ***************/
    string userInput = "6eex";
    string COMMAND= "PEAKS";
    if (argc >= 2)
    {
        userInput = argv[1];
    }
    argv[1];
    //std::cout << userInput << "\n";
    /***************************************************/

    /******   OP SPECIFIC SETTINGS  ***************/
    string ccp4directory = "/d/projects/u/ab002/Thesis/PhD/Data/Ccp4/";
    string pdbdirectory = "/d/projects/u/ab002/Thesis/PhD/Data/Pdb/";
    /***************************************************/
    
    if (COMMAND == "PEAKS")
    {
        //std::cout << userInput << "\n";        
        Ccp4 myCcp4(userInput,ccp4directory);
        PdbFile myPdb(userInput, pdbdirectory);
        myCcp4.makePeaks(&myPdb);
    }
    else
    {
        //std::cout << myCcp4.getPdbCode() << " " << myCcp4.getResolution() << " " << myCcp4.isLoaded() << "\n";
    }
}
