#include <iostream>
#include <fstream>
#include <sys/stat.h>
#include <stdint.h>

// function for swapping endianness
uint32_t swap_endianness(uint32_t value)
{
  uint32_t result = 0;
  result |= (value & 0x000000FF) << 24; // grab last byte and move to first pos
  result |= (value & 0x0000FF00) << 8;
  result |= (value & 0x00FF0000) >> 8;
  result |= (value & 0xFF000000) >> 24;
  return result;
}


union char2float
{
  float f;
  unsigned char c[4];
};

// ifstream -- used for reading input only
// ofstream -- used for writing output only
// fstream  -- for reading and writing to one file
//
// all are defined in fstream.h
//
// normally for file IO you don't use >>, << operators. It can be done, but
// it's a more advanced topic.
//
// to get the size of a file use the C library function stat
// #include<sys/stat.h>
// ...
// struct stat results;
// if (stat("input.bin", &results) == 0))
//    //the size of the file in bytes is in results.st_size
// else
//    //an error occurred


int main(int argc, char** argv)
{

  // process args
  if (argc < 2)
  {
    std::cout << "Give an input file" << "\n";
    return -1;
  }

  //std::string filename = argv[1];
  char* filename = argv[1];
  
  // get file information
  struct stat results;
  if (stat(filename, &results) == 0)
  {
    std::cout << "File size = " << results.st_size << "\n";
  }
  else
  {
    std::cout << "Error getting file size" << "\n";
    return -1;
  }

  std::ifstream floatFile;
  floatFile.open(filename, std::ios::in | std::ios::binary);
  
  if (!floatFile)	
  {
    std::cout << "error opening file" << "\n";
  }

  char  c_buffer[results.st_size];
  float f_buffer[results.st_size/4];

  if (!floatFile.read (c_buffer, results.st_size))
  {
    std::cout << "error reading\n";
  }

  std::cout << "read " << floatFile.gcount() << " bytes \n";

  // finally convert the read bytes into floating point values
  for (int i = 0; i < floatFile.gcount(); i+=4){
    char2float converter;
    for (int j = 0; j < 4; j++)
    {
      converter.c[j] = c_buffer[i+j];
    }
    std::cout << "got: " << converter.f << "\n";
    
  }
  
  return 0;
}
