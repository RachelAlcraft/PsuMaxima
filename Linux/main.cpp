#include <iostream>
#include "Ccp4.h"
#include "helper.h"

int main(int argc, char* argv[]) 
{
    /******   INPUTS  ***************/
    cout << "Started..." << "\n";
    string pdb = "6jvv";
    string COMMAND= "DENSITY";
    if (argc >= 2)
    {                
        vector<string> inputs = helper::stringToVector(argv[1],"|");
        cout << "BEGIN_USERINPUTS\n";    
        cout <<  argv[1] << "\n";   
        cout << "User Input" << "\n";
        for (unsigned int i = 0; i < inputs.size(); ++ i)
            cout << (string)inputs[i] << "\n";

        COMMAND = (string)inputs[0];
        pdb = (string)inputs[1];
        cout << "pdb=" << pdb << "\n";
        cout << "END_USERINPUTS\n";                
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
        Ccp4 myCcp4(pdb,ccp4directory);
        PdbFile myPdb(pdb, pdbdirectory);
        myCcp4.makePeaks(&myPdb);                
    }
    else if (COMMAND == "DENSITY")
    {
        Ccp4 myCcp4(pdb,ccp4directory);
        PdbFile myPdb(pdb, pdbdirectory);        
        VectorThree central(0,0,0);
        VectorThree linear(0,0,0);
        VectorThree planar(0,0,0);
        myCcp4.makeSlices(central,linear,planar);
    }

    cout << "Finished with no errros";
}

