This program does the following:
	Reads lidar data from las file or csv file
	Filters the 3D points using a threshold on retro intensity (for csv input) or intensity (for las input)
	Cluster the 3D points that belongs to the same sign
	Assign the same sign id to the points that belongs to the same sign
	For the las output, assign the same color to the points that belongs to the same sign
		This color can be used in CloudCompare using the las output to visualize the clustered 3D points using the RGB field and analyse the result
	Outputs a csv file in geo coordinate system (latitudes and longitudes)
	Outputs a las file in geo coordinate system (latitudes and longitudes)
	Outputs a las file in UTM coordinate system

The following parameters can be changed in the code:
	UTM_ZONE: is the utm zone used to convert UTM to Geo (latitudes and longitudes) (defalut value 16 for Atlanta, GA)
	THRESHOLD_INTENSITY: used to filter the point cloud if the input is a las file (default value 40000.0)
	THRESHOLD_RETRO: used to filter the point cloud if the input is a csv file (default value 0.61)

To compile the program you will need to install liblas library and Geographic library then, can be installed using sudo apt-get install liblas-c-dev
    Run the script compile.sh using the following command:
        ./compile.sh
    Or
    Run the following command:
        g++ -std=c++11 -o filter main.cpp -llas -lGeographic     

Usage:
       ./filter <path_to_input_LAS_or_CSV> <path_to_output_folder>

Example:
       ./filter data/20180223/input/HD_20180223_Campus_EB_Run1_LAS1_2.las data/20180223/output/HD_20180223_Campus_EB_Run1/
   or:
       ./filter data/20180223/input/HD_20180223_Campus_EB_Run1.csv data/20180223/output/HD_20180223_Campus_EB_Run1/

