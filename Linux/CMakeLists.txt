cmake_minimum_required(VERSION 3.0.0)
project(PsuMaxima VERSION 0.1.0)

include(CTest)
enable_testing()

add_executable(PsuMaxima main.cpp Ccp4.h Ccp4.cpp PdbFile.h PdbFile.cpp Atom.h Atom.cpp MatrixThreeThree.h MatrixThreeThree.cpp VectorThree.h VectorThree.cpp helper.h helper.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
