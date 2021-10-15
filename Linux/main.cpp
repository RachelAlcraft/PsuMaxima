#include <iostream>
#include <cstdlib>

#include "Ccp4.h"
#include "helper.h"
#include "CoutReports.h"
#include "Interpolator.h"

int main(int argc, char* argv[])
{
    /******   OP SPECIFIC SETTINGS  ***************/
    bool isLinux = true;
    // **** LINUX PANDORA **** //
    string ccp4directory = "/d/projects/u/ab002/Thesis/PhD/Data/Ccp4/";
    string pdbdirectory = "/d/projects/u/ab002/Thesis/PhD/Data/Pdb/";
    string userCcp4directory = "/d/projects/u/ab002/Thesis/PhD/Data/UserCcp4/";
    string userPdbdirectory = "/d/projects/u/ab002/Thesis/PhD/Data/UserPdb/";
    string emdbCcp4directory = "/d/projects/u/ab002/Thesis/PhD/Data/EmdbCcp4/";
    string emdbPdbdirectory = "/d/projects/u/ab002/Thesis/PhD/Data/EmdbPdb/";
    string MAT_TYPE = "XRAY";
    if (!isLinux)
    {
        // **** Windows laptop rachel  **** //
        /***************************************************/
        ccp4directory = "C:/Dev/Github/ProteinDataFiles/ccp4_data/";
        pdbdirectory = "C:/Dev/Github/ProteinDataFiles/pdb_data/";
        emdbCcp4directory = "C:/Dev/Github/ProteinDataFiles/EMDB/ccp4_data/";
        emdbPdbdirectory = "C:/Dev/Github/ProteinDataFiles/EMDB/pdb_data/";
    }
    /******   INPUTS  ***************/
    cout << "Started..." << "\n";
    string pdbInput = "";
    string pdbCode = "";
    string ccp4Code = "";
    string COMMAND = "";    
    int INTERPNUM = 0;
    int Fos = 2;
    int Fcs = -2;
    double cX = 0;
    double cY = 0;
    double cZ = 0;
    double lX = 0;
    double lY = 0;
    double lZ = 0;
    double pX = 0;
    double pY = 0;
    double pZ = 0;
    double width = 0;
    double gap = 0;    
    //synthetic data params
    string atoms = "";    
    string model = "";

    // Inputs euither through code or command line called from python
    string INPUT = "";
    //INPUT = "TEXTCOUT|1ejg|5|-2|1|";
    //INPUT = "SLICES|1ejg|5|1|-1|9.373_7.688_15.546|9.5_9.079_14.937|9.64_7.542_16.748|50_0.5";
    //INPUT = "PEAKS|1ejg|5|2|-1|";
    //INPUT = "PEAKS|user_0abc|5|2|-1|";
    INPUT = "ATOMSDENSITY|emdb_22145_6xe9|5|2|-1|";
    //INPUT = "SLICES|1us0|5|0|0|9.373-7.688-15.546|9.5_9.079_14.937|9.64_7.542_16.748|3_0.1";
    //INPUT = "SYNTHETIC|@CA,9.5,9.079,14.937,1,2.4,1.00,-,-,-,-,-,-,- @C,9.373,7.688,15.546,2,2.6,1.00,-,-,-,-,-,-,- @O,9.64,7.542,16.748,3,2.6,1.00,-,-,-,-,-,-,- |iam|9.373-7.688-15.546|9.5-9.079-14.937|9.64-7.542-16.748|5-0.02";    
    //INPUT = "SYN_CCP4IAM|1ejg|5|2|-1|";
    
    //EMDB tests
    //INPUT = "TEXT|emdb_21995_5a1a|5|2|-1|";
    //INPUT = "SLICES|emdb_21995_5a1a|5|2|-1|148.265_93.322_67.859|147.349_93.606_66.761|149.223_94.495_68.019|3_0.1";
    //INPUT = "SLICES|5a1a|5|2|-1|148.265_93.322_67.859|147.349_93.606_66.761|149.223_94.495_68.019|5_0.05";
    //INPUT = "SLICES|emdb_21995_5a1a|5|0|1|148.265_93.322_67.859|147.349_93.606_66.761|149.223_94.495_68.019|10_0.05";
    
    if (argc >= 2)
        INPUT = argv[1];
    if (true)
    {
        vector<string> inputs = helper::stringToVector(INPUT, "|");
        cout << "BEGIN_USERINPUTS\n";
        cout << INPUT << "\n";
        cout << "User Input" << "\n";
        for (unsigned int i = 0; i < inputs.size(); ++i)
            cout << (string)inputs[i] << "\n";

        COMMAND = (string)inputs[0];
        pdbInput = (string)inputs[1];
        INTERPNUM = atol(inputs[2].c_str());
        Fos = atol(inputs[3].c_str());
        Fcs = atol(inputs[4].c_str());        
        cout << "pdb=" << pdbInput << "\n";

        if (COMMAND == "SLICES" || COMMAND == "SYNTHETIC")
        {
            string central = inputs[5];
            string linear = inputs[6];
            string planar = inputs[7];
            string image_size = inputs[8];
            vector<string> cCoords = helper::stringToVector(central, "_");
            vector<string> lCoords = helper::stringToVector(linear, "_");
            vector<string> pCoords = helper::stringToVector(planar, "_");
            vector<string> imSize = helper::stringToVector(image_size, "_");
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
        if (COMMAND == "SYNTHETIC")
        {
            atoms = (string)inputs[1];
            model = (string)inputs[2];
            cout << "atoms=" << atoms << "\n";
        }

        cout << "END_USERINPUTS\n";
    }
    //if the coder is USER_ tghen we have user uploaded data    
    pdbCode = pdbInput;
    ccp4Code = pdbInput;
    
    size_t user = pdbInput.find("user_");
    if (user != string::npos)
    {
        ccp4directory = userCcp4directory;
        pdbdirectory = userPdbdirectory;
        Fos = 2;
        Fcs = -1;
    }

    size_t emdb = pdbInput.find("emdb_");
    if (emdb != string::npos)
    {
        MAT_TYPE = "EM";
        ccp4directory = emdbCcp4directory;
        pdbdirectory = emdbPdbdirectory;
        Fos = 2;
        Fcs = -1;
        vector<string> cInputs = helper::stringToVector(pdbInput, "_");
        pdbCode = "emdb_" + cInputs[2];
        ccp4Code = "emdb_" + cInputs[1];
    }

    if (COMMAND == "SYNTHETIC")
    {        
        CoutReports::coutSyntheticSlice(atoms, model, new Algorithmic(), VectorThree(cX, cY, cZ), VectorThree(lX, lY, lZ), VectorThree(pX, pY, pZ), width, gap);
    }
    else if (COMMAND == "TEXT")
    {
        Ccp4 myCcp4(ccp4Code, MAT_TYPE,ccp4directory, Fos, Fcs);
        myCcp4.printText(ccp4directory);
    }
    else if (COMMAND == "TEXTCOUT")
    {
        Ccp4 myCcp4(ccp4Code, MAT_TYPE, ccp4directory, Fos, Fcs);
        CoutReports::coutText(&myCcp4);
    }
    else
    {
        /***************************************************/
        Ccp4 myCcp4(ccp4Code, MAT_TYPE,ccp4directory,Fos,Fcs);
        PdbFile myPdb(pdbCode, pdbdirectory);        
        //INTERPNUM is the encoded interpolator, so 0 == nearest
        if (COMMAND == "SYN_CCP4IAM")
        {
            CoutReports::coutSyntheticIAM(&myCcp4, &myPdb, new Algorithmic());
        }
        else
        {
            Interpolator* interp;
            if (COMMAND == "PEAKS")//TODO don't know why we need thvenaz for peaks...
                interp = new Thevenaz(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);
            else if (INTERPNUM == 0)
                interp = new Nearest(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);
            else
                interp = new Thevenaz(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);

            if (COMMAND == "PEAKS")
            {
                CoutReports::coutPeaks(&myCcp4, &myPdb, interp, INTERPNUM);
            }
            else if (COMMAND == "ATOMSDENSITY")
            {
                CoutReports::coutAtomsDensity(&myCcp4, &myPdb, interp);
            }
            else if (COMMAND == "ATOMSADJUSTED")
            {
                CoutReports::coutAtomsAdjusted(&myCcp4, &myPdb, interp);
            }
            else if (COMMAND == "SLICES")
            {
                if (Fos == 0 && Fcs == 0)
                {
                    interp = new Algorithmic();
                    interp->addAtoms(myPdb.Atoms);
                    CoutReports::coutSyntheticSlice("", "IAM", interp, VectorThree(cX, cY, cZ), VectorThree(lX, lY, lZ), VectorThree(pX, pY, pZ), width, gap);
                }
                else
                {
                    CoutReports::coutSlices(&myCcp4, &myPdb, interp, VectorThree(cX, cY, cZ), VectorThree(lX, lY, lZ), VectorThree(pX, pY, pZ), width, gap);
                }

                
            }
        }
        
    }
    
    cout << "Finished with no errros";
}

