//============================================================================
// Author      : Esther Ling lingesther@gatech.edu
// Date        : June 2019
// Description : Reads las file and converts to csv
//============================================================================

#include <liblas/liblas.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <stdio.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>

using namespace std;

static void help() {
    cout
        << "\n------------------------------------------------------------------\n"
        << " This program does the following actions:\n"
        << "\tReads a las file and converts it into csv\n"
        << " Usage:\n"
        << "        ./las2csv <path_to_input_las> <path_to_output_folder>\n"
        << " \n"
        << " Example:\n"
        << "        ./las2csv ../../../Data/i75_2018/V_20180804_I75_nb_run1/V_20180804_I75_nb_run1 (0).las ../../../Data/i75_2018/V_20180804_I75_nb_run1/\n"
        << "------------------------------------------------------------------\n\n"
        << endl;
}

struct Point
{
    int signId;
    int id;
    double x;
    double y;
    double z;
    double angle;
    double distance;
    double retro;
    double normalized_retro;
    double utc;
    bool fromLas;
};

void las2csv(const string& filename, const string& folderCSV)
{
	// open las file for reading
    std::ifstream ifLas(filename.c_str(), ios::in | ios::binary);
    liblas::Reader reader(ifLas);

    liblas::Header const& header = reader.GetHeader();

	// open csv file for writing
	std::string outputCSV = folderCSV + filename;
	ofstream csv;
	csv.open(outputCSV.c_str());
	csv << "Id,X,Y,Z,Angle,Distance,Retro,UTC,\n";

    for (int k=0; reader.ReadNextPoint(); ++k)
    {
        // get the 3D point
        liblas::Point const& p = reader.GetPoint();
        // create a Point and set values
        Point point;
        point.fromLas = true;
        point.signId = -1;
        point.id = k;
        point.x = p.GetX();
        point.y = p.GetY();
        point.z = p.GetZ();
        point.retro = p.GetIntensity();
        point.utc = p.GetTime();

        // write to csv file
		csv << point.id << "," << fixed << setprecision(7) << point.x << "," << point.y << "," << setprecision(3) << point.z
		<< "," << setprecision(5) << point.angle << "," << setprecision(3) << point.distance
		<<setprecision(5)<<","<<  point.retro << "," << setprecision(5) << point.utc << "\n";

		if(k%1000 == 0)
		{
			cout << "row: " << k << endl;
		}

    }

	csv.close();

}

int main(int argc, char** argv) {
    if (argc != 3)
    {
        help();
        return 1;
    }

    try
    {
        string inputFile = argv[1];
        string outputFolder = argv[2];
        string inputExtension = inputFile.substr(inputFile.size()-3);

        if(inputExtension == "las")
        {
        	// create folder
		    // check if the folder exists and make one if not
		    struct stat sb;
		    if (!(stat(outputFolder.c_str(), &sb) == 0 && S_ISDIR(sb.st_mode)))
		    {
		        const int dir_err = mkdir(outputFolder.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
		        if (dir_err == -1)
		        {
		            std::cout << "Error creating directory: " << outputFolder << std::endl;
		        }
		    }

			// make a subfolder for CSV
			string folderCSV = outputFolder + "csv/";
			struct stat sbCSV;
			if (!(stat(folderCSV.c_str(), &sbCSV) == 0 && S_ISDIR(sbCSV.st_mode)))
			{
			    const int dir_err = mkdir(folderCSV.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
			    if (dir_err == -1)
			    {
			        std::cout << "Error creating directory: " << folderCSV << std::endl;
			    }
			}

			// conversion
            las2csv(inputFile, folderCSV);
            std::cout << "Done!" << std::endl;
        }
        else
        {
            cout << "Error: wrong file extension: " << inputExtension << endl;
            help();
            return 1;
        }

    }
    catch (std::exception const& e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
    }

	return 0;
}
