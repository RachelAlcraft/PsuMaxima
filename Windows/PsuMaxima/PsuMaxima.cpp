// PsuMaxima.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Ccp4.h"
#include "PdbFile.h"

int main()
{
    /******   COMMAND LINE INPUTS  ***************/
    string COMMAND = "PEAKS";
    string pdb = "6jvv";
    /***************************************************/
    /******   WINDOWS SPECIFIC SETTINGS  ***************/
    string ccp4directory = "C:/Dev/Github/ProteinDataFiles/ccp4_data/";
    string pdbdirectory = "C:/Dev/Github/ProteinDataFiles/pdb_data/";
    /***************************************************/
    Ccp4 myCcp4(pdb, ccp4directory);
    PdbFile myPdb(pdb, pdbdirectory);
    if (COMMAND == "PEAKS")
    {
        myCcp4.makePeaks(&myPdb);
    }
    

}


