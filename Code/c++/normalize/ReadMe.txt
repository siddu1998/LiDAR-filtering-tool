This program does the following actions:
   Reads Lidar data from CSV file in geo  UTM coordinates (zone 16 by default)
   Normalize retro intensity using beam distance and incidence angle
   Outputs a csv file in geo coordinate system (latitudes and longitudes)
	Outputs a las file in geo coordinate system (latitudes and longitudes)

To compile the program you will need to install liblas library then
    Run the script compile.sh using the following command:
        ./compile.sh
    Or
    Run the following command:
        g++ -std=c++11 -o normIntensity main.cpp -llas

Usage:
       ./normIntensity <path_to_input_CSV> <path_to_output_folder>

Example:
       ./normIntensity data/20180223/input/HD_20180223_Campus_EB_Run1.csv data/20180223/normalizedData/H_EB/

reference chengbo ai thesis page 69 to 71.
