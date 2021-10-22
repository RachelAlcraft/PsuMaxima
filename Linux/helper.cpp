#include<sstream>
#include <iostream>
#include<iomanip>

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

string helper::getNumberStringGaps(double number, int dp, int length)
{// we need fixed string intervals for pdb files in ent format	
	number = round(number*1000)/1000;
	int missingLength = length;	
	if (dp > 0)
	{
		missingLength -= dp;
		missingLength -= 1;//for the point
	}
	if (number >= 0)
	{
		if (number < 10)
			missingLength -= 1;
		else if (number < 100)
			missingLength -= 2;
		else if (number < 1000)
			missingLength -= 3;
		else if (number < 10000)
			missingLength -= 4;
		else //if (number < 100000)
			missingLength -= 5;
	}
	else
	{
		if (number > -10)
			missingLength -= 2;
		else if (number > -100)
			missingLength -= 3;
		else if (number < 1000)
			missingLength -= 4;
		else if (number < 10000)
			missingLength -= 5;
		else// if (number < 100000)
			missingLength -= 6;
	}
	string gaps = "";

	for (unsigned int i=0; i < missingLength; ++i)
		gaps += " ";
	return gaps;
}
string helper::getWordStringGaps(string word, int length)
{// we need fixed string intervals for pdb files in ent format		
	int missingLength = length-word.length();	
	string gaps = "";	
	for (unsigned int i=0; i < missingLength; ++i)
		gaps += " ";
	return gaps;
}