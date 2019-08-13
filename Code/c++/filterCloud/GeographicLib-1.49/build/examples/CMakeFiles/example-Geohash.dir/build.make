# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/esther/Downloads/GeographicLib-1.49

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/esther/Downloads/GeographicLib-1.49/build

# Include any dependencies generated for this target.
include examples/CMakeFiles/example-Geohash.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/example-Geohash.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/example-Geohash.dir/flags.make

examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o: examples/CMakeFiles/example-Geohash.dir/flags.make
examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o: ../examples/example-Geohash.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/esther/Downloads/GeographicLib-1.49/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o -c /home/esther/Downloads/GeographicLib-1.49/examples/example-Geohash.cpp

examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/example-Geohash.dir/example-Geohash.cpp.i"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/esther/Downloads/GeographicLib-1.49/examples/example-Geohash.cpp > CMakeFiles/example-Geohash.dir/example-Geohash.cpp.i

examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/example-Geohash.dir/example-Geohash.cpp.s"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/esther/Downloads/GeographicLib-1.49/examples/example-Geohash.cpp -o CMakeFiles/example-Geohash.dir/example-Geohash.cpp.s

examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.requires:

.PHONY : examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.requires

examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.provides: examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.requires
	$(MAKE) -f examples/CMakeFiles/example-Geohash.dir/build.make examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.provides.build
.PHONY : examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.provides

examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.provides.build: examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o


# Object files for target example-Geohash
example__Geohash_OBJECTS = \
"CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o"

# External object files for target example-Geohash
example__Geohash_EXTERNAL_OBJECTS =

examples/example-Geohash: examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o
examples/example-Geohash: examples/CMakeFiles/example-Geohash.dir/build.make
examples/example-Geohash: src/libGeographic.so.17.1.2
examples/example-Geohash: examples/CMakeFiles/example-Geohash.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/esther/Downloads/GeographicLib-1.49/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable example-Geohash"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/example-Geohash.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/example-Geohash.dir/build: examples/example-Geohash

.PHONY : examples/CMakeFiles/example-Geohash.dir/build

examples/CMakeFiles/example-Geohash.dir/requires: examples/CMakeFiles/example-Geohash.dir/example-Geohash.cpp.o.requires

.PHONY : examples/CMakeFiles/example-Geohash.dir/requires

examples/CMakeFiles/example-Geohash.dir/clean:
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && $(CMAKE_COMMAND) -P CMakeFiles/example-Geohash.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/example-Geohash.dir/clean

examples/CMakeFiles/example-Geohash.dir/depend:
	cd /home/esther/Downloads/GeographicLib-1.49/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/esther/Downloads/GeographicLib-1.49 /home/esther/Downloads/GeographicLib-1.49/examples /home/esther/Downloads/GeographicLib-1.49/build /home/esther/Downloads/GeographicLib-1.49/build/examples /home/esther/Downloads/GeographicLib-1.49/build/examples/CMakeFiles/example-Geohash.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/example-Geohash.dir/depend

