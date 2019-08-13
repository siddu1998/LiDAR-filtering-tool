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
include examples/CMakeFiles/example-Ellipsoid.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/example-Ellipsoid.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/example-Ellipsoid.dir/flags.make

examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o: examples/CMakeFiles/example-Ellipsoid.dir/flags.make
examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o: ../examples/example-Ellipsoid.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/esther/Downloads/GeographicLib-1.49/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o -c /home/esther/Downloads/GeographicLib-1.49/examples/example-Ellipsoid.cpp

examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.i"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/esther/Downloads/GeographicLib-1.49/examples/example-Ellipsoid.cpp > CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.i

examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.s"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/esther/Downloads/GeographicLib-1.49/examples/example-Ellipsoid.cpp -o CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.s

examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.requires:

.PHONY : examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.requires

examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.provides: examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.requires
	$(MAKE) -f examples/CMakeFiles/example-Ellipsoid.dir/build.make examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.provides.build
.PHONY : examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.provides

examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.provides.build: examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o


# Object files for target example-Ellipsoid
example__Ellipsoid_OBJECTS = \
"CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o"

# External object files for target example-Ellipsoid
example__Ellipsoid_EXTERNAL_OBJECTS =

examples/example-Ellipsoid: examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o
examples/example-Ellipsoid: examples/CMakeFiles/example-Ellipsoid.dir/build.make
examples/example-Ellipsoid: src/libGeographic.so.17.1.2
examples/example-Ellipsoid: examples/CMakeFiles/example-Ellipsoid.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/esther/Downloads/GeographicLib-1.49/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable example-Ellipsoid"
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/example-Ellipsoid.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/example-Ellipsoid.dir/build: examples/example-Ellipsoid

.PHONY : examples/CMakeFiles/example-Ellipsoid.dir/build

examples/CMakeFiles/example-Ellipsoid.dir/requires: examples/CMakeFiles/example-Ellipsoid.dir/example-Ellipsoid.cpp.o.requires

.PHONY : examples/CMakeFiles/example-Ellipsoid.dir/requires

examples/CMakeFiles/example-Ellipsoid.dir/clean:
	cd /home/esther/Downloads/GeographicLib-1.49/build/examples && $(CMAKE_COMMAND) -P CMakeFiles/example-Ellipsoid.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/example-Ellipsoid.dir/clean

examples/CMakeFiles/example-Ellipsoid.dir/depend:
	cd /home/esther/Downloads/GeographicLib-1.49/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/esther/Downloads/GeographicLib-1.49 /home/esther/Downloads/GeographicLib-1.49/examples /home/esther/Downloads/GeographicLib-1.49/build /home/esther/Downloads/GeographicLib-1.49/build/examples /home/esther/Downloads/GeographicLib-1.49/build/examples/CMakeFiles/example-Ellipsoid.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/example-Ellipsoid.dir/depend

