# Configure GeographicLib
#
# Set
#  GeographicLib_FOUND = GEOGRAPHICLIB_FOUND = 1
#  GeographicLib_INCLUDE_DIRS = /usr/local/include
#  GeographicLib_SHARED_LIBRARIES = GeographicLib        (or empty)
#  GeographicLib_STATIC_LIBRARIES = GeographicLib_STATIC (or empty)
#  GeographicLib_SHARED_DEFINITIONS = GEOGRAPHICLIB_SHARED_LIB=1
#  GeographicLib_STATIC_DEFINITIONS = GEOGRAPHICLIB_SHARED_LIB=0
#  GeographicLib_LIBRARY_DIRS = /usr/local/lib
#  GeographicLib_BINARY_DIRS = /usr/local/bin
#  GeographicLib_VERSION = 1.34 (for example)
#  GEOGRAPHICLIB_DATA = /usr/local/share/GeographicLib (for example)
#  Depending on GeographicLib_USE_STATIC_LIBS
#    GeographicLib_LIBRARIES = ${GeographicLib_SHARED_LIBRARIES}, if OFF
#    GeographicLib_LIBRARIES = ${GeographicLib_STATIC_LIBRARIES}, if ON
#    GeographicLib_DEFINITIONS = ${GeographicLib_SHARED_DEFINITIONS}, if OFF
#    GeographicLib_DEFINITIONS = ${GeographicLib_STATIC_DEFINITIONS}, if ON
#  If only one of the libraries is provided, then
#    GeographicLib_USE_STATIC_LIBS is ignored.
#
# For cmake 2.8.11 or later, there's no need to include
#   include_directories (${GeographicLib_INCLUDE_DIRS})
#   add_definitions (${GeographicLib_DEFINITIONS})
#
# The following variables are only relevant if the library has been
# compiled with a default precision different from double:
#  GEOGRAPHICLIB_PRECISION = the precision of the library (usually 2)
#  GeographicLib_HIGHPREC_LIBRARIES = the libraries need for high precision

message (STATUS "Reading ${CMAKE_CURRENT_LIST_FILE}")
# GeographicLib_VERSION is set by version file
message (STATUS
  "GeographicLib configuration, version ${GeographicLib_VERSION}")

# Tell the user project where to find our headers and libraries
get_filename_component (_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
if (IS_ABSOLUTE "../../..")
  # This is an uninstalled package (still in the build tree)
  set (_ROOT "../../..")
  set (GeographicLib_INCLUDE_DIRS "")
  set (GeographicLib_LIBRARY_DIRS "${_ROOT}/src")
  set (GeographicLib_BINARY_DIRS "${_ROOT}/tools")
else ()
  # This is an installed package; figure out the paths relative to the
  # current directory.
  get_filename_component (_ROOT "${_DIR}/../../.." ABSOLUTE)
  set (GeographicLib_INCLUDE_DIRS "${_ROOT}/include")
  set (GeographicLib_LIBRARY_DIRS "${_ROOT}/lib")
  set (GeographicLib_BINARY_DIRS "${_ROOT}/bin")
endif ()
set (GEOGRAPHICLIB_DATA "/usr/local/share/GeographicLib")
set (GEOGRAPHICLIB_PRECISION 2)
set (GeographicLib_HIGHPREC_LIBRARIES "")

set (GeographicLib_SHARED_LIBRARIES GeographicLib)
set (GeographicLib_STATIC_LIBRARIES )
set (GeographicLib_SHARED_DEFINITIONS -DGEOGRAPHICLIB_SHARED_LIB=1)
set (GeographicLib_STATIC_DEFINITIONS )
# Read in the exported definition of the library
include ("${_DIR}/geographiclib-targets.cmake")
include ("${_DIR}/geographiclib-namespace-targets.cmake")

unset (_ROOT)
unset (_DIR)

if ((NOT GeographicLib_SHARED_LIBRARIES) OR
    (GeographicLib_USE_STATIC_LIBS AND GeographicLib_STATIC_LIBRARIES))
  set (GeographicLib_LIBRARIES ${GeographicLib_STATIC_LIBRARIES})
  set (GeographicLib_DEFINITIONS ${GeographicLib_STATIC_DEFINITIONS})
  message (STATUS "  \${GeographicLib_LIBRARIES} set to static library")
else ()
  set (GeographicLib_LIBRARIES ${GeographicLib_SHARED_LIBRARIES})
  set (GeographicLib_DEFINITIONS ${GeographicLib_SHARED_DEFINITIONS})
  message (STATUS "  \${GeographicLib_LIBRARIES} set to shared library")
endif ()

set (GeographicLib_NETGeographicLib_LIBRARIES )

# Check for the components requested.  This only supports components
# STATIC, SHARED, and NETGeographicLib by checking the value of
# GeographicLib_${comp}_LIBRARIES.  No need to check if the component
# is required or not--the version file took care of that.
# GeographicLib_${comp}_FOUND is set appropriately for each component.
if (GeographicLib_FIND_COMPONENTS)
  foreach (comp ${GeographicLib_FIND_COMPONENTS})
    if (GeographicLib_${comp}_LIBRARIES)
      set (GeographicLib_${comp}_FOUND 1)
      message (STATUS "GeographicLib component ${comp} found")
    else ()
      set (GeographicLib_${comp}_FOUND 0)
      message (WARNING "GeographicLib component ${comp} not found")
    endif ()
  endforeach ()
endif ()

# GeographicLib_FOUND is set to 1 automatically
set (GEOGRAPHICLIB_FOUND 1)     # for backwards compatibility
