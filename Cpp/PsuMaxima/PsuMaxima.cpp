// PsuMaxima.cpp : Defines the entry point for the application.
//

#include "PsuMaxima.h"
#include "Ccp4.h"

using namespace std;

int main(int argc, char* argv[])
{//From the cmmand line we pass in
	//1COMMAND can be CREATE or SLICE
	//IF CREATE then
		//2.pdbfile, 3.ccp4 file, 4.diff file, 5.new pdb name, 6.peaks name, 7.report name
	//IF SLICE then
		//2.CCP4 file, 3.diff file, 4.(x,y,z) 5.(x,y,z) 6.(x,y,z) (central, linear, planar)
	


	string runCommand = "CREATE";	
	if (argc > 1)
	{
		runCommand = argv[1];
	}
	if (runCommand == "CREATE")
	{
		string pdbFileName = "C:/Dev/Github/PsuMaxima/Cpp/PsuMaxima/TestFiles/pdb6eex.ent";
		string ccp4FileName = "C:/Dev/Github/PsuMaxima/Cpp/PsuMaxima/TestFiles/6eex.ccp4";
		string diffFileName = "C:/Dev/Github/PsuMaxima/Cpp/PsuMaxima/TestFiles/6eex_diff.ccp4";
		string newPdbFileName = "C:/Dev/Github/PsuMaxima/Cpp/PsuMaxima/TestFiles/pdb6eex.new";
		string peaksFileName = "C:/Dev/Github/PsuMaxima/Cpp/PsuMaxima/TestFiles/peaks6eex.csv";
		string reportFileName = "C:/Dev/Github/PsuMaxima/Cpp/PsuMaxima/TestFiles/report6eex.csv";
	
		if (argc > 5)
		{		
			string pdbFileNameX(argv[2]);
			string ccp4FileNameX(argv[3]);
			string diffFileNameX(argv[4]);
			string newPdbFileNameX(argv[5]);
			string peaksFileNameX(argv[6]);
			string reportFileNameX(argv[7]);

			pdbFileName = pdbFileNameX;
			ccp4FileName = ccp4FileNameX;
			diffFileName = diffFileNameX;
			newPdbFileName = newPdbFileNameX;
			peaksFileName = peaksFileNameX;
			reportFileName = reportFileNameX;
		}

		Ccp4* c4 = new Ccp4(ccp4FileName, diffFileName);
		cout << "Resolution is " << c4->Resolution() << endl;
		cout << "Success?" << c4->Loaded() << endl;


		
		cout << pdbFileName << "," << ccp4FileName << "," << reportFileName << endl;
	}
	else
	{
		cout << "Incorrect arguments entered," << " , , " << endl;
	}

	return 0;
}
