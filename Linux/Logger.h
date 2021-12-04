#pragma once

#include <string>
#include <vector>

using namespace std;


class Logger
{//https://stackoverflow.com/questions/1008019/c-singleton-design-pattern
public:
    static Logger& getInstance()
    {
        static Logger    instance; // Guaranteed to be destroyed. Instantiated on first use.
        return instance;
    }
private:
    Logger() {}                    // Constructor? (the {} brackets) are needed here.

    // C++ 03
    // ========
    // Don't forget to declare these two. You want to make sure they are inaccessible(especially from outside), 
    // otherwise, you may accidentally get copies of your singleton appearing.
    Logger(Logger const&);              // Don't Implement
    void operator=(Logger const&); // Don't implement

    string _dir;
    string _log;
            
public:    
    string init(string directory, string cmd, string pdb);
    void log(string msg);    
};