
#include <iostream>
#include <fstream>
#include <string>


#include "Logger.h"

string Logger::init(string directory, string cmd, string pdb)
{
	_dir = directory;		
	_log = pdb + "_" + cmd + ".log";
	size_t pos = cmd.find("FILE");

	std::ofstream logfile;
	logfile.open((_dir + _log).c_str()); 
	logfile << "-------- OPENING LOG FILE ------\n";
	logfile.close();

	if (pos != std::string::npos)
	{
		return cmd.substr(0, cmd.length() - 4);
	}
	else
	{
		return cmd;
	}

}

void Logger::log(string msg)
{
	std::ofstream logfile;
	logfile.open((_dir + _log).c_str(), std::ios_base::app); // append instead of overwrite
	logfile << msg << "\n";
	logfile.close();
}