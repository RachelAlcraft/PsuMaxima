#include <iostream>
#include <cstdlib>

#include "Ccp4.h"
#include "helper.h"
#include "CoutReports.h"
#include "Interpolator.h"

int main(int argc, char* argv[]) 
{
    /******   OP SPECIFIC SETTINGS  ***************/
    // **** LINUX PANDORA **** //
    string ccp4directory = "/d/projects/u/ab002/Thesis/PhD/Data/Ccp4/";
    string pdbdirectory = "/d/projects/u/ab002/Thesis/PhD/Data/Pdb/";
    // **** Windows laptop rachel  **** //
    /***************************************************/
    //string ccp4directory = "C:/Dev/Github/ProteinDataFiles/ccp4_data/";
    //string pdbdirectory = "C:/Dev/Github/ProteinDataFiles/pdb_data/";
    /******   INPUTS  ***************/
    cout << "Started..." << "\n";
    string pdb = "1ejg";
    string COMMAND= "PEAKS";
    string INTERP = "THEVENAZ";
    double cX = 5;
    double cY = 5;
    double cZ = 5;
    double lX = 6;
    double lY = 6;
    double lZ = 6;
    double pX = 2;
    double pY = 2;
    double pZ = 13;
    double width = 5.0;
    double gap = 0.1;

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
                      

        if (COMMAND == "SLICES")
        {
            string central = inputs[2];
            string linear = inputs[3];
            string planar = inputs[4];
            string image_size = inputs[5];
            vector<string> cCoords = helper::stringToVector(central,"-");
            vector<string> lCoords = helper::stringToVector(linear,"-");
            vector<string> pCoords = helper::stringToVector(planar,"-");
            vector<string> imSize = helper::stringToVector(image_size,"-");
            cX = atof(cCoords[0].c_str());
            cY = atof(cCoords[1].c_str());
            cZ = atof(cCoords[2].c_str());
            lX = atof(lCoords[0].c_str());
            lY = atof(lCoords[1].c_str());
            lZ = atof(lCoords[2].c_str());
            pX = atof(pCoords[0].c_str());
            pY = atof(pCoords[1].c_str());
            pZ = atof(pCoords[2].c_str());
            width = atof(imSize[0].c_str());
            gap = atof(imSize[1].c_str());
                        
            cout << "(" << cX << "-" << cY << "-" << cZ << ")\n";
            cout << "(" << lX << "-" << lY << "-" << lZ << ")\n";
            cout << "(" << pX << "-" << pY << "-" << pZ << ")\n";
            cout << "(" << width << "-" << gap << ")\n";
        }

        cout << "END_USERINPUTS\n";  
    }
        
    /***************************************************/        
    Ccp4 myCcp4(pdb, ccp4directory);
    PdbFile myPdb(pdb, pdbdirectory);
    Interpolator* interp;
    if (INTERP == "NEAREST")
        interp = new Nearest(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);
    else
        interp = new Thevenaz(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);

    if (COMMAND == "PEAKS")    
        CoutReports::coutPeaks(&myCcp4,&myPdb,interp);                    
    else if (COMMAND == "ATOMS")                         
        CoutReports::coutAtoms(&myCcp4,&myPdb,interp);                    
    else if (COMMAND == "SLICES")   
        CoutReports::coutSlices(&myCcp4,&myPdb,interp, VectorThree(cX, cY, cZ), VectorThree(lX, lY, lZ), VectorThree(pX, pY, pZ),width,gap);
    
    cout << "Finished with no errros";
}

