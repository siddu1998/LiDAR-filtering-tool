# Install script for directory: /home/esther/Downloads/GeographicLib-1.49/matlab

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/matlab/geographiclib" TYPE FILE FILES
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/Contents.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/cassini_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/cassini_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/defaultellipsoid.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/ecc2flat.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/eqdazim_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/eqdazim_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/flat2ecc.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/gedistance.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/gedoc.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geocent_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geocent_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geodarea.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geoddistance.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geoddoc.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geodreckon.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geographiclib_test.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geoid_height.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/geoid_load.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/gereckon.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/gnomonic_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/gnomonic_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/loccart_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/loccart_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/mgrs_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/mgrs_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/polarst_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/polarst_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/projdoc.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/tranmerc_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/tranmerc_inv.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/utmups_fwd.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/utmups_inv.m"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/matlab/geographiclib/private" TYPE FILE FILES
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/A1m1f.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/A2m1f.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/A3coeff.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/A3f.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/AngDiff.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/AngNormalize.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/AngRound.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/C1f.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/C1pf.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/C2f.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/C3coeff.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/C3f.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/C4coeff.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/C4f.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/G4coeff.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/GeoRotation.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/LatFix.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/SinCosSeries.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/atan2dx.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/cbrtx.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/copysignx.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/cvmgt.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/eatanhe.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/geoid_file.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/geoid_load_file.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/norm2.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/sincosdx.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/sumx.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/swap.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/tauf.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib/private/taupf.m"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/matlab/geographiclib-legacy" TYPE FILE FILES
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/Contents.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/geocentricforward.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/geocentricreverse.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/geodesicdirect.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/geodesicinverse.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/geodesicline.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/geoidheight.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/localcartesianforward.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/localcartesianreverse.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/mgrsforward.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/mgrsreverse.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/polygonarea.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/utmupsforward.m"
    "/home/esther/Downloads/GeographicLib-1.49/matlab/geographiclib-legacy/utmupsreverse.m"
    )
endif()

