//============================================================================
// Name        : lidar.cpp
// Author      : BADR EL HAFIDI badr@gatech.edu
// Version     : 0.1
// Copyright   : GATECH CE LAB
// Description : read and filter lidar data
//
// Date        : June 2019
// Author      : Esther Ling lingesther@gatech.edu
// Description : 1. Made compatible with the output of c++/normalize/normIntensity (ony for csv input)
//               2. Added status print lines for user
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
#include <math.h>
#include <random>
#include <GeographicLib/Geocentric.hpp>
#include <GeographicLib/LocalCartesian.hpp>
#include <GeographicLib/GeoCoords.hpp>
// #include <opencv2/opencv.hpp>
// #include <opencv2/highgui/highgui.hpp>
// #include <opencv2/core/core.hpp>
// #include "opencv2/imgcodecs.hpp"
// #include "cvui.h"

#define UTM_ZONE 16
#define THRESHOLD_INTENSITY 30000.0
#define THRESHOLD_RETRO 0.55
#define DISTANCE 2
#define NUMBER_OF_POINTS 50

using namespace std;
using namespace GeographicLib;
// using namespace cv;

static void help() {
    cout
        << "\n------------------------------------------------------------------\n"
        << " This program does the following:\n"
        << " \tReads lidar data from las file or csv file\n"
        << " \tFilters the 3D points using a threshold on retro intensity (for csv input) or intensity (for las input)\n"
        << " \tClusters the 3D points that belongs to the same sign\n"
        << " \tAssigns the same sign id to the points that belongs to the same sign\n"
        << " \tFor the las output, assign the same color to the points that belongs to the same sign\n"
        << " \t\tThis color can be used in CloudCompare using the las output to visualize the clustered 3D points using the RGB field and analyse the result\n"
        << " \tOutputs a csv file in geo coordinate system (latitudes and longitudes)\n"
        << " \tOutputs a las file in geo coordinate system (latitudes and longitudes)\n"
        << " \tOutputs a las file in UTM coordinate system\n"
        << " \n"
        << " The following parameters can be changed in the code:\n"
        << " \tUTM_ZONE: is the utm zone used to convert UTM to Geo (latitudes and longitudes) (defalut value 16 for Atlanta, GA)\n"
        << " \tTHRESHOLD_INTENSITY: used to filter the point cloud if the input is a las file (default value 40000.0)\n"
        << " \tTHRESHOLD_RETRO: used to filter the point cloud if the input is a csv file (default value 0.61)\n"
        << " \n"
        << " Usage:\n"
        << "        ./filter <path_to_input_LAS_or_CSV> <path_to_output_folder>\n"
        << " \n"
        << " Example:\n"
        << "        ./filter data/20180223/input/HD_20180223_Campus_EB_Run1_LAS1_2.las data/20180223/output/HD_20180223_Campus_EB_Run1/\n"
        << "    or:\n"
        << "        ./filter data/20180223/input/HD_20180223_Campus_EB_Run1.csv data/20180223/output/HD_20180223_Campus_EB_Run1/\n"
        << "------------------------------------------------------------------\n\n"
        << endl;
}


struct PointCld
{
    int signId;
    int id;
    double x;
    double y;
    double z;
    double retro;
    double normalized_retro;
    double utc;
    double angle;
    double dist;
    bool fromLas;
    int color[3];
    double px;
    double py;
};

void getGeoRepFromUTM(int zone, double easting, double northing, double& lat, double& lon)
{

    // UTM for northern hemisphere
    string coords = to_string(zone) + "n," + to_string(easting) + "," + to_string(northing);
    GeoCoords gc(coords);
    int geoPrecision = 9; // max precision for conversion
    string latlong =  gc.GeoRepresentation(geoPrecision);
    stringstream latlong_ss(latlong);
    string item;
    for(int k=0; getline(latlong_ss, item, ' '); k++)
    {

        if(k==0) lat = stod(item);
        if(k==1) lon = stod(item);
    }
}

void getUTMRepFromGeo(double lat, double lon, int& zone, double& easting, double& northing)
{

    // UTM for northern hemisphere

    stringstream coords_ss;
    coords_ss << fixed << setprecision(10) << lat << " " << lon;
    string coords = coords_ss.str();
    GeoCoords gc(coords);
    int convPrecision = 9; // max precision for conversion
    string utm =  gc.UTMUPSRepresentation(convPrecision);
    stringstream utm_ss(utm);
    string item;

    for(int k=0; getline(utm_ss, item, ' '); k++)
    {
        if(k==0) zone = stod(item.substr(0,item.size()-1));
        if(k==1) easting = stod(item);
        if(k==2) northing = stod(item);
    }

}


void getPointsFromCSV(string filename, map<int, PointCld >& imap)
{
    std::ifstream infile(filename.c_str());
    string cell, line;
    stringstream line_ss;
    int k;
    cout << "Reading csv file .." << endl;
      for(k=0; getline(infile, line); k++)
      {
        if(k>0) // ignore csv header
          {
              line_ss.str(line);
              PointCld point;
              for (int i=0; getline(line_ss, cell, ','); i++)
              {
                  // if(i==0) point.id = stoi(cell);
                  // if(i==1) point.y = stod(cell);
                  // if(i==2) point.x = stod(cell);
                  // if(i==3) point.z = stod(cell);
                  // if(i==6) point.retro = stod(cell);
                  // if(i==7) point.utc = stod(cell);
                      if(i==0) point.id = k;
                      if(i==2) point.x = stod(cell); // LONG
                      if(i==1) point.y = stod(cell); // LAT
                      if(i==3) point.z = stod(cell);
                      if(i==4) point.angle = stod(cell);
                      if(i==5) point.dist = stod(cell);
                      // if(i==6) point.retro = stod(cell); // retro
                      // if(i==7) point.utc = stod(cell);
                      if(i==7) point.retro = stod(cell); // normalized retro
                      if(i==8) point.utc = stod(cell); // UTC

              }
              line_ss.clear();
              point.signId = -1;
              point.fromLas = false;
              imap[point.id] = point;

              if(k%5000 == 0)
              {
                cout << "Line: " << k << endl;
              }
          }
      }
      cout << "Finished reading csv file! " << endl;
    //for (std::map<int, PointCld >::iterator it=imap.begin(); it!=imap.end(); ++it)
    //{
    //    cout << "Key:\t" << it->first << endl;
    //    PointCld point = it->second;
    //    cout << "id:\t"  << point.id << "\t";
    //    cout << "x:\t"  << point.x << "\t";
    //    cout << "y:\t"  << point.y << "\t";
    //    cout << "z:\t"  << point.z << "\t";
    //    cout << "retro:\t"  << point.retro << endl;
    //}

}

void getPointsFromLAS(string filename, map<int, PointCld >& imap)
{
    std::ifstream ifLas(filename.c_str(), ios::in | ios::binary);
    liblas::Reader reader(ifLas);

    liblas::Header const& header = reader.GetHeader();

    for (int k=0; reader.ReadNextPoint(); ++k)
    {
        // get the 3D point
        liblas::Point const& p = reader.GetPoint();
        // create a PointCld and set values
        PointCld point;
        point.fromLas = true;
        point.signId = -1;
        point.id = k;
        // transform points from utm to lat/long
        double lat, lon;
        getGeoRepFromUTM(UTM_ZONE, p.GetX(), p.GetY(), lat, lon);
        point.x = lat;
        point.y = lon;
        point.z = p.GetZ();
        point.retro = p.GetIntensity();
        point.utc = p.GetTime();
        point.angle=p.GetScanAngleRank();
        //point.dist=p.GetDistance();
        // add Point to map
        imap[point.id] = point;
    }
}

void writeOutCSV(string folderName, string filename, map<int, vector <PointCld> >& clusteredMap)
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

    csv << "SignId,Id,X,Y,Z,Retro,angle,distance,UTC\n";
    for (map<int, vector<PointCld> >::iterator it=clusteredMap.begin(); it!=clusteredMap.end(); ++it)
    {

        vector <PointCld> points = it->second;

        for(int i=0; i<points.size(); i++)

        {
            csv << points[i].signId << "," << points[i].id << "," << fixed << setprecision(7) << points[i].x << "," << points[i].y << "," << setprecision(3) << points[i].z
            << "," << setprecision(2) << points[i].retro << "," << setprecision(5) << points[i].angle << ","<< setprecision(3) << points[i].dist << ","<< setprecision(3) << points[i].utc  << "\n";
            //<< points[i].y << "," << setprecision(3)
        }
    }
    csv.close();
}

void writeOutLasGeo(string folderName, string filename, map<int, vector <PointCld> >& clusteredMap)
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
    for (std::map<int, vector <PointCld> >::iterator it=clusteredMap.begin(); it!=clusteredMap.end(); ++it)
    {
        // get the points from the map
        vector <PointCld> points = it->second;
        for(int i=0; i<points.size(); i++)
        {
            // get the point from the vector
            PointCld point = points[i];

            if(it==clusteredMap.begin())
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

    // Set coordinate system to EPSG:4326 using GDAL support
    liblas::SpatialReference srs;
    srs.SetFromUserInput("EPSG:4326");
    header.SetSRS(srs);

    // Create the writer
    std::string outputLAS = folderLAS + filename;
    ofstream ofLas(outputLAS, ios::out | ios::binary);
    liblas::Writer writer(ofLas, header);

    // write out LAS file
    for (map<int, vector <PointCld> >::iterator it=clusteredMap.begin(); it!=clusteredMap.end(); ++it)
    {
        // get the points from the map
        vector <PointCld> points = it->second;
        for(int i=0; i<points.size(); i++)
        {
            // get the point from the vector
            PointCld point = points[i];
            // create liblas point
            liblas::Point pointLas(&header);
            // set some values to the point
            pointLas.SetPointSourceID(point.signId);
            pointLas.SetCoordinates(point.x, point.y, point.z);
            pointLas.SetScanAngleRank(point.angle);
            if(point.fromLas)
            {
                pointLas.SetIntensity( (int) point.retro );
            }
            else
            {
                pointLas.SetIntensity( (int) (point.retro*100000) );
            }
            pointLas.SetTime( point.utc );
            pointLas.SetColor(liblas::Color(point.color[0],point.color[1],point.color[2]));
            // write the point to the las file
            writer.WritePoint(pointLas);
        }
    }

}


void writeOutLasUTM(string folderName, string filename, map<int, vector <PointCld> >& clusteredMap)
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
    for (std::map<int, vector <PointCld> >::iterator it=clusteredMap.begin(); it!=clusteredMap.end(); ++it)
    {
        // get the points from the map
        vector <PointCld> points = it->second;
        for(int i=0; i<points.size(); i++)
        {
            // get the point from the vector
            PointCld point = points[i];

            double easting, northing;
            int zone;
            getUTMRepFromGeo(point.x, point.y, zone, easting, northing);

            if(it==clusteredMap.begin())
            {
                minX = easting; maxX = easting;
                minY = northing; maxY = northing;
                minZ = point.z; maxZ = point.z;
            }
            else
            {
                minX = (easting < minX) ? easting : minX ;
                minY = (northing < minY) ? northing : minY ;
                minZ = (point.z < minZ) ? point.z : minZ ;
                maxX = (easting > maxX) ? easting : maxX ;
                maxY = (northing > maxY) ? northing : maxY ;
                maxZ = (point.z > maxZ) ? point.z : maxZ ;
            }
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

    // Set coordinate system to EPSG:4326 using GDAL support
    liblas::SpatialReference srs;
    srs.SetFromUserInput("EPSG:4326");
    header.SetSRS(srs);
    // Create the writer

    std::string outputLAS = folderLAS + filename;
    ofstream ofLas(outputLAS, ios::out | ios::binary);
    liblas::Writer writer(ofLas, header);

    // write out LAS file
    for (map<int, vector <PointCld> >::iterator it=clusteredMap.begin(); it!=clusteredMap.end(); ++it)
    {
        // get the points from the map
        vector <PointCld> points = it->second;
        for(int i=0; i<points.size(); i++)
        {
            // get the point from the vector
            PointCld point = points[i];
            // create liblas point
            liblas::Point pointLas(&header);
            // set some values to the point
            pointLas.SetPointSourceID(point.signId);
            double easting, northing;
            int zone;
            getUTMRepFromGeo(point.x, point.y, zone, easting, northing);

            pointLas.SetCoordinates(easting, northing, point.z);
            if(point.fromLas)
            {
                pointLas.SetIntensity( (int) point.retro );
            }
            else
            {
                pointLas.SetIntensity( (int) (point.retro*1000) );
            }
            pointLas.SetTime( point.utc );
            pointLas.SetColor(liblas::Color(point.color[0],point.color[1],point.color[2]));
            pointLas.SetScanAngleRank(point.angle);
            // write the point to the las file
            writer.WritePoint(pointLas);
        }
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
        map<int, PointCld > imap;
        string inputFile = argv[1];
        string inputExtension = inputFile.substr(inputFile.size()-3);
        if(inputExtension == "csv")
        {
            getPointsFromCSV(inputFile, imap);

        }
        else if(inputExtension == "las")
        {
            getPointsFromLAS(inputFile, imap);
        }
        else
        {
            cout << "Error: wrong file extension: " << inputExtension << endl;
            help();
        }

        // Filter the points
        cout << "Filtering the points ..." << endl;
        map<int, PointCld > filteredMap; // key = point.id
        for (std::map<int, PointCld >::iterator it=imap.begin(); it!=imap.end(); ++it)
        {
            PointCld point = it->second;
            if(point.fromLas)
            {
                if( point.retro>THRESHOLD_INTENSITY )
                {
                    filteredMap[point.id] = point;
                }
            }
            else
            {   if( point.retro>THRESHOLD_RETRO )
                {
                    filteredMap[point.id] = point;
                }
            }
        }
        int countSigns = 1;

        // generate random color
        std::random_device rd;
        std::mt19937 eng(rd());
        std::uniform_int_distribution<> distr(10, 250);
        int randR = distr(eng);
        int randG = distr(eng);
        int randB = distr(eng);

        map<int, vector <PointCld> > clusteredMap; // key = point.signId

        Geocentric earth(Constants::WGS84_a(), Constants::WGS84_f());

        for (std::map<int, PointCld >::iterator it=filteredMap.begin(); it!=filteredMap.end(); ++it)
        {
            vector <PointCld> points;
            PointCld seed = it->second;
            if(seed.signId == -1)
            {
                filteredMap[it->first].signId = countSigns;
                seed.signId = countSigns;
                seed.color[0] = randR;
                seed.color[1] = randG;
                seed.color[2] = randB;

                points.push_back(seed);

                // set seed point as local coords reference
                LocalCartesian proj(seed.x, seed.y, seed.z, earth);

                for (int i=1; i<30000; i++)
                {
                    //cout<<filteredMap.count(it->first + i)<<"\n";
                    // check if the key exists
                    if(filteredMap.count(it->first + i) == 1)
                    {
                        PointCld point = filteredMap[it->first + i];
                        double xd=-1,yd=-1,zd=-1;
                        proj.Forward(point.x, point.y, point.z, xd, yd, zd);
                        double distance = sqrt( xd*xd + yd*yd + zd*zd );
                        if(distance < DISTANCE)
                        {
                            filteredMap[it->first + i].signId = countSigns;
                            point.signId = countSigns;
                            point.color[0] = randR;
                            point.color[1] = randG;
                            point.color[2] = randB;
                            points.push_back(point);
                        }
                    }
                }
                // save the sign's points in the map
                if( points.size() > NUMBER_OF_POINTS )
                {
                    clusteredMap[countSigns] = points;
                    // increment signId and generate random color
                    countSigns++;
                    randR = distr(eng);
                    randG = distr(eng);
                    randB = distr(eng);
                }
            }
        }

        // write out LAS and CSV files
        cout << "Writing to LAS and CSV file.." << endl;
        string folderName = argv[2];
        //writeOutLasUTM(folderName, "output_las_utm.las",clusteredMap);
        writeOutLasGeo(folderName, "output_las_geo.las",clusteredMap);
        writeOutCSV(folderName, "output_csv.csv",clusteredMap);
    }
    catch (std::exception const& e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}

