#include <iostream>
#include <cstdlib>
#include <fstream>

#include "Ccp4.h"
#include "helper.h"
#include "CoutReports.h"
#include "Interpolator.h"
#include "Logger.h"

int main(int argc, char* argv[])
{
    /* FULL LIST OF COMMAND AND INPUTS
    * Inputs are command and piped paramaters
    * 0 = commands: TEXTCOUT, TEXT500, TEXT, SLICES, PEAKS, ATOMSDENSITY, ATOMSADJUSTEDFILE, SYNTHETIC, SYN_CCP4IAM, SAMPLES, EMBELLISH witha further FILE for file instead of cout output
    * 1 = pdb code
    * 2 = interpolation number
    * 3 = Fos
    * 4 = Fcs
    * 5 = image size as width_gap
    * 6 = points list of central:linear:planar+ cx_cy_cz:lx_ly_lz:px_py_pz+...
    * 7 = logfile
    * 8 = pdbDirectory
    * 9 = ccp4Directory    
    * 
    */
    /******   OP SPECIFIC SETTINGS  ***************/
    bool isLinux = false;
    // **** LINUX PANDORA **** //
    string ccp4directory = "/d/projects/u/ab002/Thesis/PhD/Data/Ccp4/";
    string pdbdirectory = "/d/projects/u/ab002/Thesis/PhD/Data/Pdb/";
    string logdirectory = "/d/projects/u/ab002/Thesis/PhD/Data/Log/";
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
        logdirectory = "C:/Dev/Github/ProteinDataFiles/LeicippusTesting/Log/";
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
    vector<VectorThree> cs;
    vector<VectorThree> ls;
    vector<VectorThree> ps;    
    double width = 0;
    double gap = 0;    
    //synthetic data params
    string atoms = "";    
    string model = "";

    // Inputs euither through code or command line called from python
    string INPUT = "";
    //INPUT = "TEXTCOUT|1ejg|5|-2|1|";
    //INPUT = "TEXT500|7a6a|5|-2|1|";
    //INPUT = "TEXT|7a6a|5|-2|1|";
    //INPUT = "SLICESFILE|1ejg|5|1|-1|9.373_7.688_15.546|9.5_9.079_14.937|9.64_7.542_16.748|50_0.5";
    //INPUT = "PEAKSFILE|7a6a|5|2|-1|";
    //INPUT = "PEAKS|user_0abc|5|2|-1|";
    //INPUT = "ATOMSDENSITY|7a6a|5|2|-1|";
    //INPUT = "ATOMSADJUSTEDFILE|7a6a|5|2|-1|";
    //INPUT = "SLICESFILE|1us0|5|0|0|9.373-7.688-15.546|9.5_9.079_14.937|9.64_7.542_16.748|3_0.1";
    //INPUT = "SYNTHETIC|@CA,9.5,9.079,14.937,1,2.4,1.00,-,-,-,-,-,-,- @C,9.373,7.688,15.546,2,2.6,1.00,-,-,-,-,-,-,- @O,9.64,7.542,16.748,3,2.6,1.00,-,-,-,-,-,-,- |iam|9.373-7.688-15.546|9.5-9.079-14.937|9.64-7.542-16.748|5-0.02";    
    //INPUT = "SYN_CCP4IAM|1ejg|5|2|-1|";
    //INPUT = "SAMPLES|1ejg|5|2|-1|";
    //INPUT = "SAMPLESFILE|7a6a|5|2|-1|";

    //INPUT = "SLICESFILE|6zwh|5|1|0|20_0.1|-23.614_5.319_-16.667:-26.679_6.306_-18.075:-21.176_4.092_-17.251";

    //INPUT = "SLICESFILE|3nir|5|1|0|20_0.1|9.71_-12.376_15.907:0.975_-15.224_7.167:2.52_-13.584_7.06"; // a sulphuer in the middle
    //INPUT = "SLICESFILE|3nir|5|1|0|5_0.01|10.033_-10.398_12.281:10.727_-9.27_12.088:9.868_-11.242_11.386"; //a peptide bond
    //INPUT = "SLICESFILE|1ejg|5|1|0|5_0.01|10.033_-10.398_12.281:10.727_-9.27_12.088:9.868_-11.242_11.386"; //a peptide bond
    //INPUT = "SYN_CCP4IAMFILE|6eex|5|2|-1|";
    //INPUT = "EMBELLISHFILE|6eex|5|1|0|";
    

    //Adjusted
    //INPUT = "SLICESFILE|7a6a|5|2|-1|8_0.05|89.534_86.68_95.214:89.319_87.836_95.507:90.861_86.277_95.507+95.214_86.68_146.626:95.507_87.836_146.841:95.507_86.277_145.299+146.626_95.214_86.68:146.841_95.507_87.836:145.299_95.507_86.277+86.681_95.214_89.534:87.836_95.507_89.319:86.278_95.507_90.861+146.626_86.681_140.946:146.841_87.836_140.653:145.299_86.277_140.653+146.626_149.479_95.214:146.841_148.324_95.506:145.299_149.882_95.507+140.946_149.479_146.626:140.653_148.324_146.841:140.653_149.882_145.299+89.534_149.48_140.946:89.319_148.324_140.653:90.861_149.883_140.653+89.534_95.214_149.479:89.319_95.507_148.324:90.861_95.507_149.882+95.214_146.626_149.479:95.506_146.841_148.324:95.507_145.299_149.882+140.946_89.534_149.48:140.653_89.319_148.324:140.653_90.861_149.883+146.626_140.946_149.479:146.841_140.653_148.324:145.299_140.653_149.882+149.48_140.946_89.534:148.324_140.653_89.319:149.883_140.653_90.861+149.479_89.534_95.214:148.324_89.319_95.507:149.882_90.861_95.507+149.479_146.626_140.946:148.324_146.841_140.653:149.882_145.299_140.653+149.479_95.214_146.626:148.324_95.506_146.841:149.882_95.507_145.299+95.214_89.534_86.681:95.507_89.319_87.836:95.507_90.861_86.278+86.68_146.626_95.214:87.836_146.841_95.507:86.277_145.299_95.507+86.681_89.534_140.946:87.836_89.32_140.654:86.278_90.861_140.653+89.534_140.946_86.681:89.32_140.654_87.836:90.861_140.653_86.278+140.946_146.626_86.68:140.654_146.841_87.836:140.653_145.299_86.277";
    //Original
    //INPUT = "SLICESFILE|7a6a|5|2|-1|8_0.05|89.564_86.65_95.184:89.241_87.885_95.429:90.688_86.173_95.494+140.976_86.651_89.564:140.731_87.885_89.241:140.666_86.174_90.688+95.184_149.509_89.564:95.429_148.275_89.241:95.494_149.986_90.688+86.651_140.976_146.596:87.885_140.731_146.919:86.174_140.666_145.472+95.184_86.65_146.596:95.429_87.885_146.919:95.494_86.173_145.472+146.596_95.184_86.65:146.919_95.429_87.885:145.472_95.494_86.173+86.651_95.184_89.564:87.885_95.429_89.241:86.174_95.494_90.688+146.596_86.651_140.976:146.919_87.885_140.731:145.472_86.173_140.666+146.596_149.509_95.184:146.919_148.275_95.428:145.472_149.986_95.494+140.976_149.509_146.596:140.731_148.275_146.919:140.666_149.986_145.472+89.564_149.51_140.976:89.241_148.275_140.731:90.688_149.987_140.666+89.564_95.184_149.509:89.241_95.429_148.275:90.688_95.494_149.986+95.184_146.596_149.509:95.428_146.919_148.275:95.494_145.472_149.986+140.976_89.564_149.51:140.731_89.241_148.275:140.666_90.688_149.987+146.596_140.976_149.509:146.919_140.731_148.275:145.472_140.666_149.986+149.51_140.976_89.564:148.275_140.731_89.241:149.987_140.666_90.688+149.509_89.564_95.184:148.275_89.241_95.429:149.986_90.688_95.494+149.509_146.596_140.976:148.275_146.919_140.731:149.986_145.472_140.666+149.509_95.184_146.596:148.275_95.428_146.919:149.986_95.494_145.472+95.184_89.564_86.651:95.429_89.241_87.885:95.494_90.688_86.174+86.65_146.596_95.184:87.885_146.919_95.429:86.173_145.472_95.494+86.651_89.564_140.976:87.885_89.242_140.732:86.174_90.688_140.666+89.564_140.976_86.651:89.242_140.732_87.885:90.688_140.666_86.174+140.976_146.596_86.65:140.732_146.919_87.885:140.666_145.472_86.173";
    
    //EMDB tests
    //INPUT = "TEXT|emdb_21995_5a1a|5|2|-1|";
    //INPUT = "SLICES|emdb_21995_5a1a|5|2|-1|148.265_93.322_67.859|147.349_93.606_66.761|149.223_94.495_68.019|3_0.1";
    //INPUT = "SLICES|5a1a|5|2|-1|148.265_93.322_67.859|147.349_93.606_66.761|149.223_94.495_68.019|5_0.05";
    //INPUT = "SLICES|emdb_21995_5a1a|5|0|1|148.265_93.322_67.859|147.349_93.606_66.761|149.223_94.495_68.019|10_0.05";
    //INPUT = "EMBELLISHFILE|3nir|5|1|0|GRIDSIZE|CENTRAL|LINEAR|PLANAR|Csv/";
    //INPUT = "TEXT500|1aho|5|1|0|GRIDSIZE|CENTRAL|LINEAR|PLANAR|Csv/";
    //ccp4directory = "C:/Dev/Github/ProteinDataFiles/mtz_data/";
    //INPUT = "TEXT|1aho|5|-2|1|";
    INPUT = "DEFORMATIONFILE|6eex|5|2|-1|x|x|C:/Dev/Github/LeucipPipelines/Pipelines/DeformationDensity/1EMData/Data/|C:/Dev/Github/LeucipPipelines/Pipelines/DeformationDensity/1EMData/Data/|C:/Dev/Github/LeucipPipelines/Pipelines/DeformationDensity/1EMData/Data/";

        
    if (argc >= 2)
        INPUT = argv[1];    
    vector<string> inputs = helper::stringToVector(INPUT, "|");
    
    COMMAND = (string)inputs[0];
    pdbInput = (string)inputs[1];
    if (inputs.size() > 2)
        string interpNum = (string)inputs[2];        
    if (inputs.size() > 3)
        string Fos = (string)inputs[3];
    if (inputs.size() > 4)
        string Fcs = (string)inputs[4];
    if (inputs.size() > 5)
        string gridSize = (string)inputs[5];
    if (inputs.size() > 6)
        string coords = (string)inputs[6];                
    if (inputs.size() > 7)
        logdirectory = inputs[7];
    if (inputs.size() > 8)
        pdbdirectory = inputs[8];
    if (inputs.size() > 9)
        ccp4directory = inputs[9];        
    
    bool diverted = false;
    string newCOMMAND = Logger::getInstance().init(logdirectory, COMMAND, pdbInput);

    for (int i = 0; i < argc; ++i)
    {
        string inp = argv[i];
        Logger::getInstance().log(inp);
    }

    //##############################
    std::streambuf* psbuf, * backup;
    std::ofstream resfile;
    resfile.open((logdirectory + pdbInput + "_" + COMMAND + ".csv").c_str());
    backup = std::cout.rdbuf();     // back up cout's streambuf
    psbuf = resfile.rdbuf();        // get file's streambuf
    std::cout.rdbuf(psbuf);         // assign streambuf to cout
    //##############################
    Logger::getInstance().log(INPUT);
    
    if (newCOMMAND == COMMAND)
    {
        diverted = false;        
        std::cout.rdbuf(backup);        // restore cout's original streambuf
        resfile.close();
    }
    else
    {
        COMMAND = newCOMMAND;
    }
    

    if (true)
    {        
        cout << "BEGIN_USERINPUTS\n";
        cout << INPUT << "\n";
        cout << "User Input" << "\n";
        for (unsigned int i = 0; i < inputs.size(); ++i)
            cout << (string)inputs[i] << "\n";
                       
        INTERPNUM = atol(inputs[2].c_str());
        Fos = atol(inputs[3].c_str());
        Fcs = atol(inputs[4].c_str());        
        cout << "pdb=" << pdbInput << "\n";

        if (COMMAND == "SLICES" || COMMAND == "SYNTHETIC")
        {
            string image_size = inputs[5];
            vector<string> imSize = helper::stringToVector(image_size, "_");
            width = atof(imSize[0].c_str());
            gap = atof(imSize[1].c_str());

            vector<string> points = helper::stringToVector(inputs[6], "+");
            for (unsigned int p = 0; p < points.size(); ++p)
            {
                string point = points[p];
                vector<string> each_point = helper::stringToVector(point, ":");

                string central = each_point[0];
                string linear = each_point[1];
                string planar = each_point[2];

                vector<string> cCoords = helper::stringToVector(central, "_");
                vector<string> lCoords = helper::stringToVector(linear, "_");
                vector<string> pCoords = helper::stringToVector(planar, "_");
                
                double cX = atof(cCoords[0].c_str());
                double cY = atof(cCoords[1].c_str());
                double cZ = atof(cCoords[2].c_str());
                double lX = atof(lCoords[0].c_str());
                double lY = atof(lCoords[1].c_str());
                double lZ = atof(lCoords[2].c_str());
                double pX = atof(pCoords[0].c_str());
                double pY = atof(pCoords[1].c_str());
                double pZ = atof(pCoords[2].c_str());
                cs.push_back(VectorThree(cX,cY,cZ));                                
                ls.push_back(VectorThree(lX, lY, lZ));
                ps.push_back(VectorThree(pX, pY, pZ));
                
                cout << "(" << cX << "-" << cY << "-" << cZ << ")\n";
                cout << "(" << lX << "-" << lY << "-" << lZ << ")\n";
                cout << "(" << pX << "-" << pY << "-" << pZ << ")\n";
                
            }
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
        CoutReports::coutSyntheticSlices(atoms, model, new Algorithmic(), cs, ls,ps, width, gap);
    }
    else if (COMMAND == "TEXT")
    {
        Ccp4 myCcp4(ccp4Code, MAT_TYPE,ccp4directory, Fos, Fcs);
        myCcp4.printText(ccp4directory,false);
    }
    else if (COMMAND == "TEXT500")
    {
        Ccp4 myCcp4(ccp4Code, MAT_TYPE, ccp4directory, Fos, Fcs);
        myCcp4.printText(ccp4directory, true);
    }
    else if (COMMAND == "TEXTCOUT")
    {
        Ccp4 myCcp4(ccp4Code, MAT_TYPE, ccp4directory, Fos, Fcs);
        CoutReports::coutText(&myCcp4,true);
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
        else if (COMMAND == "SAMPLES")
        {
            Interpolator* interpMap;
            interpMap = new Thevenaz(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);
            CoutReports::coutSamples(&myCcp4, &myPdb, interpMap, new Algorithmic());
        }
        else
        {
            Interpolator* interp;
            if (COMMAND == "PEAKS" || COMMAND == "EMBELLISH")//TODO don't know why we need thvenaz for peaks...
                interp = new Thevenaz(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);
            else if (INTERPNUM == 0)
                interp = new Nearest(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);
            else
                interp = new Thevenaz(myCcp4.Matrix, myCcp4.W01_NX, myCcp4.W02_NY, myCcp4.W03_NZ);

            if (COMMAND == "PEAKS")
            {
                CoutReports::coutPeaks(&myCcp4, &myPdb, interp, INTERPNUM);
            }
            else if (COMMAND == "EMBELLISH")
            {
                CoutReports::coutEmbellishPdb(&myCcp4, &myPdb, interp, INTERPNUM);
            }
            else if (COMMAND == "DEFORMATION")
            {
                CoutReports::coutDeformation(&myCcp4, &myPdb, interp, new Algorithmic());
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
                    CoutReports::coutSyntheticSlices("", "IAM", interp, cs, ls, ps, width, gap);
                }
                else
                {
                    CoutReports::coutSlices(&myCcp4, &myPdb, interp, cs, ls, ps, width, gap);
                }

                
                
            }

            
                        
        }
                        
    }
    if (diverted)
    {
        std::cout.rdbuf(backup);        // restore cout's original streambuf
        resfile.close();
    }
    
    cout << "Finished with no errros";
}

