//============================================================================
// Name        : lidar.cpp
// Author      : BADR EL HAFIDI badr@gatech.edu
// Version     : 0.1
// Copyright   : GATECH CE LAB
// Description : read and filter lidar data
//
// Date        : June 2019
// Author      : Esther Ling lingesther@gatech.edu
// Description : 1. Removed maximum of 999,999 lines
//               2. Fixed bug: normalized retro and retro columns were swapped in the output csv file
//============================================================================

#include <liblas/liblas.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>

using namespace std;

static void help() {
    cout
        << "\n------------------------------------------------------------------\n"
        << " This program does the following actions:\n"
        << "\tReads Lidar data from CSV file in geo coordinate system (latitudes and longitudes)\n"
        << "\tNormalize retro intensity using beam distance and incidence angle\n"
        << "\tOutputs a csv file in geo coordinate system (latitudes and longitudes)\n"
        << " \tOutputs a las file in geo coordinate system (latitudes and longitudes)\n"
        << " \n"
        << " Usage:\n"
        << "        ./normIntensity <path_to_input_CSV> <path_to_output_folder>\n"
        << " \n"
        << " Example:\n"
        << "        ./normIntensity data/20180223/input/HD_20180223_Campus_EB_Run1.csv data/20180223/normalizedData/H_EB/\n"
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

void getPointsFromCSV(string filename, map<int, Point >& imap)
{
    std::ifstream infile(filename.c_str());
    string cell, line;
    stringstream line_ss;
    for(int k=0; getline(infile, line); k++)
    {
        // if(k>0 && k<1000000) // ignore csv header
        if(k>0) // ignore csv header
        {
            line_ss.str(line);
            Point point;
            for (int i=0; getline(line_ss, cell, ','); i++)
            {
                if(i==0) point.id = stoi(cell);
                if(i==1) point.x = stod(cell);
                if(i==2) point.y = stod(cell);
                if(i==3) point.z = stod(cell);
                if(i==4) point.angle = stod(cell);
                if(i==5) point.distance = stod(cell);
                if(i==6) point.retro = stod(cell);
                if(i==7) point.utc = stod(cell);
            }
            line_ss.clear();
            point.signId = -1;
            point.fromLas = false;
            imap[point.id] = point;
        }
        if(k%1000 == 0) // print progress
        {
            cout << "line: " << k << endl;
        }
    }
    //for (std::map<int, Point >::iterator it=imap.begin(); it!=imap.end(); ++it)
    //{
    //    cout << "Key:\t" << it->first << endl;
    //    Point point = it->second;
    //    cout << "id:\t"  << point.id << "\t";
    //    cout << "x:\t"  << point.x << "\t";
    //    cout << "y:\t"  << point.y << "\t";
    //    cout << "z:\t"  << point.z << "\t";
    //    cout << "retro:\t"  << point.retro << endl;
    //}
}

// void getPointsFromLAS(string filename, map<int, Point >& imap)
// {
//     std::ifstream ifLas(filename.c_str(), ios::in | ios::binary);
//     liblas::Reader reader(ifLas);
//
//     liblas::Header const& header = reader.GetHeader();
//
//     for (int k=0; reader.ReadNextPoint(); ++k)
//     {
//         // get the 3D point
//         liblas::Point const& p = reader.GetPoint();
//         // create a Point and set values
//         Point point;
//         point.fromLas = true;
//         point.signId = -1;
//         point.id = k;
//         point.x = p.GetX();
//         point.y = p.GetY();
//         point.z = p.GetZ();
//         point.retro = p.GetIntensity();
//         point.utc = p.GetTime();
//         // add Point to map
//         imap[point.id] = point;
//     }
// }

void writeOutCSV(string folderName, string filename, map<int, Point >& filteredMap)
{
    // check if the folder exists and make one if not
    struct stat sb;
    if (!(stat(folderName.c_str(), &sb) == 0 && S_ISDIR(sb.st_mode)))
    {
        const int dir_err = mkdir(folderName.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        if (dir_err == -1)
        {
            std::cout << "Error creating directory: " << folderName << std::endl;
        }
    }

    // make a subfolder for CSV
    string folderCSV = folderName + "csv/";
    struct stat sbCSV;
    if (!(stat(folderCSV.c_str(), &sbCSV) == 0 && S_ISDIR(sbCSV.st_mode)))
    {
        const int dir_err = mkdir(folderCSV.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        if (dir_err == -1)
        {
            std::cout << "Error creating directory: " << folderCSV << std::endl;
        }
    }
    // write out CSV file
    std::string outputCSV = folderCSV + filename;
    ofstream csv;
    csv.open(outputCSV.c_str());
    // csv << "Id,X,Y,Z,Angle,Distance,Retro,Normalized Retro,UTC,\n";
    csv << "Id,X,Y,Z,Angle,Distance,Normalized Retro,Retro,UTC,\n";
    for (map<int, Point>::iterator it=filteredMap.begin(); it!=filteredMap.end(); ++it)
    {
        Point point = it->second;
        csv << point.id << "," << fixed << setprecision(7) << point.x << "," << point.y << "," << setprecision(3) << point.z
        << "," << setprecision(5) << point.angle << "," << setprecision(3) << point.distance << ","
        <<point.normalized_retro<<setprecision(5)<<","<<  point.retro << "," << setprecision(5) << point.utc << "\n";
    }
    csv.close();
}

void writeOutLAS(string folderName, string filename, map<int, Point >& filteredMap)
{
    // check if the folder exists and make one if not
    struct stat sb;
    if (!(stat(folderName.c_str(), &sb) == 0 && S_ISDIR(sb.st_mode)))
    {
        const int dir_err = mkdir(folderName.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        if (dir_err == -1)
        {
            std::cout << "Error creating directory: " << folderName << std::endl;
        }
    }

    // make a subfolder for LAS
    string folderLAS = folderName + "las/";
    struct stat sbLAS;
    if (!(stat(folderLAS.c_str(), &sbLAS) == 0 && S_ISDIR(sbLAS.st_mode)))
    {
        const int dir_err = mkdir(folderLAS.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        if (dir_err == -1)
        {
            std::cout << "Error creating directory: " << folderLAS << std::endl;
        }
    }

    // Get bounds
    double minX, minY, minZ, maxX, maxY, maxZ;
    for (std::map<int, Point >::iterator it=filteredMap.begin(); it!=filteredMap.end(); ++it)
    {
        // get the point from the map
        Point point = it->second;

        if(it==filteredMap.begin())
        {
            minX = point.x; maxX = point.x;
            minY = point.y; maxY = point.y;
            minZ = point.z; maxZ = point.z;
        }
        else
        {
            minX = (point.x < minX) ? point.x : minX ;
            minY = (point.y < minY) ? point.y : minY ;
            minZ = (point.z < minZ) ? point.z : minZ ;
            maxX = (point.x > maxX) ? point.x : maxX ;
            maxY = (point.y > maxY) ? point.y : maxY ;
            maxZ = (point.z > maxZ) ? point.z : maxZ ;
        }
    }

    // Define the LAS header, default creates ePointFormat3
    liblas::Header header;
    // Set bounds
    header.SetMin(minX, minY, minZ);
    header.SetMax(maxX, maxY, maxZ);
    header.SetOffset(minX, minY, minZ);

    // Set scale for X Y Z precision
    //header.SetScale(0.0000001,0.0000001,0.001);
    header.SetScale(0.001,0.001,0.001);

    // // Set coordinate system to EPSG:4326 using GDAL support
    // liblas::SpatialReference srs;
    // srs.SetFromUserInput("EPSG:4326");
    // header.SetSRS(srs);
    // Create the writer

    std::string outputLAS = folderLAS + filename;
    ofstream ofLas(outputLAS, ios::out | ios::binary);
    liblas::Writer writer(ofLas, header);

    // write out LAS file
    for (map<int, Point >::iterator it=filteredMap.begin(); it!=filteredMap.end(); ++it)
    {
        // get the point from the map
        Point point = it->second;
        // create liblas point
        liblas::Point pointLas(&header);
        // set some values to the point
        pointLas.SetPointSourceID(point.id);
        pointLas.SetCoordinates(point.x, point.y, point.z);
        if(point.fromLas)
        {
            pointLas.SetIntensity( (int) point.normalized_retro );
        }
        else
        {
            pointLas.SetIntensity( (int) (point.normalized_retro*1000) );
        }
        pointLas.SetTime( point.utc );
        // write the point to the las file
        writer.WritePoint(pointLas);
    }

}

int main(int argc, char** argv) {
    if (argc != 3)
    {
        help();
        return 1;
    }

    try
    {
        // get the 3D points from the CSV or the LAS file
        map<int, Point > imap;
        string inputFile = argv[1];
        string outputFolder = argv[2];
        string inputExtension = inputFile.substr(inputFile.size()-3);

        if(inputExtension == "csv")
        {
            getPointsFromCSV(inputFile, imap);
        }
        else
        {
            cout << "Error: wrong file extension: " << inputExtension << endl;
            help();
            return 1;
        }

        // normalize the intensity or retro intensity using the beam distance and incidence angle
        double g=0;
        double f=0;
        for (std::map<int, Point >::iterator it=imap.begin(); it!=imap.end(); ++it)
        {
            double distance = it->second.distance;
            double angleRad = it->second.angle;
            double angle = angleRad * ((180.0/3.141592653589793238463));

            // compute the beam distance model function
            if(it->second.distance>15)
                g=1.0939*pow(distance,-0.04224);
            else
                g=0.0042*distance + 0.9357;

            // compute the incidence angle model function
            f = (0.0015 - 0.0001*angle*angle + 0.0003*angle)*cos(angleRad) - 0.0001*angle*angle - 0.0003*angle + 0.9985;

            it->second.normalized_retro = g*f;
        }

        // write out LAS and CSV files
        writeOutLAS(outputFolder, "output_las.las",imap);
        writeOutCSV(outputFolder, "output_csv.csv",imap);
    }
    catch (std::exception const& e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
    }

	return 0;
}
