// PsuMaxima.cpp : Defines the entry point for the application.
//

#include "PsuMaxima.h"
#include "Ccp4.h"

using namespace std;

int main()
{
	cout << "Hello CMake." << endl;
	Ccp4 *c4 = new Ccp4();
	cout << "Resolution is " << c4->Resolution();

	return 0;
}
