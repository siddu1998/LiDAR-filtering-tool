# Install script for directory: /home/esther/Downloads/GeographicLib-1.49/include/GeographicLib

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/GeographicLib" TYPE FILE FILES
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Accumulator.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/AlbersEqualArea.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/AzimuthalEquidistant.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/CassiniSoldner.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/CircularEngine.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Constants.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/DMS.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Ellipsoid.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/EllipticFunction.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/GARS.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/GeoCoords.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Geocentric.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Geodesic.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/GeodesicExact.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/GeodesicLine.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/GeodesicLineExact.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Geohash.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Geoid.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Georef.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Gnomonic.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/GravityCircle.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/GravityModel.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/LambertConformalConic.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/LocalCartesian.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/MGRS.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/MagneticCircle.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/MagneticModel.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Math.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/NearestNeighbor.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/NormalGravity.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/OSGB.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/PolarStereographic.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/PolygonArea.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Rhumb.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/SphericalEngine.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/SphericalHarmonic.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/SphericalHarmonic1.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/SphericalHarmonic2.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/TransverseMercator.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/TransverseMercatorExact.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/UTMUPS.hpp"
    "/home/esther/Downloads/GeographicLib-1.49/include/GeographicLib/Utility.hpp"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/GeographicLib" TYPE FILE FILES "/home/esther/Downloads/GeographicLib-1.49/build/include/GeographicLib/Config.h")
endif()

