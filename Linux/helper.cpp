#include "helper.h"


using namespace std;


vector<string> helper::stringToVector(string input, string delim)
{
	string newin = input;
	vector<string> vals;
	int pos = newin.find(delim);
	while (pos > -1) 
	{
		string val = newin.substr(0, pos);
		if (val != "")
			vals.push_back(val);
		newin = newin.substr(pos + 1);
		pos = newin.find(delim);
	}

	vals.push_back(newin);
	return vals;
}