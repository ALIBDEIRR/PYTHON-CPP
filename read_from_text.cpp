#include<iostream>

#include <fstream>
#include <string>
#include <sstream>
#include <vector>



double ratioo;
double numberStep;
double X;
double Y;
double LOOP;
double noiseamplitude;
double percentt;
double seuil;
double iteration;
double pas;
double seuil_r;
bool filt_Y;
double display;
double noise;   



// Function to read parameters from a .txt file
void readParametersFromTxt(const std::string& txtFilePath) {
    std::ifstream inputFile(txtFilePath);
    if (!inputFile.is_open()) {
        std::cerr << "Error opening .txt file: " << txtFilePath << std::endl;
        return;
    }

    std::string line;
    while (std::getline(inputFile, line)) {
        std::istringstream iss(line);
        std::string key;
        double value;

        if (iss >> key >> value) {
            // Match key and assign corresponding values
            if (key == "ratioo") ratioo = value;
            else if (key == "numberStep") numberStep = value;
            else if (key == "X") X = value;
            else if (key == "Y") Y = value;
            else if (key == "LOOP") LOOP = value;
            else if (key == "noiseamplitude") noiseamplitude = value;
            else if (key == "percentt") percentt = value;
            else if (key == "seuil") seuil = value;
            else if (key == "iteration") iteration = value;
            else if (key == "pas") pas = value;
            else if (key == "seuil_r") seuil_r = value;
            else if (key == "filt_Y") filt_Y = static_cast<bool>(value);
            else if (key == "display") display = value; 
            else if (key == "noise") noise = value;     
    }
}

