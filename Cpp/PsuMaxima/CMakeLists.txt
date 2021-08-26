# CMakeList.txt : CMake project for PsuMaxima, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

project ("PsuMaxima")

# Add source to this project's executable.
add_executable (PsuMaxima "PsuMaxima.cpp" "PsuMaxima.h" "Ccp4.h" "Ccp4.cpp")

# TODO: Add tests and install targets if needed.
