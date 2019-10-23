#This file shows how to link to a PUMI
#installation using CMake
#it represents a simple 'CMakeLists.txt'
#file for a new project

cmake_minimum_required(VERSION 3.0.0)

project(UGRIDtoPUMI VERSION 1.0.0 LANGUAGES CXX)
option(HAVE_SIMMETRIX "If Pumi was built with Simmetrix support" OFF)
option(ENABLE_ZOLTAN "If Pumi was built with Zoltan support" OFF)

# Starting here are the critical lines:

# Allow the user to indicate where they installed SCOREC
# via "-DSCOREC_PREFIX=/home/somewhere" when calling `cmake`
set(SCOREC_PREFIX "" CACHE STRING "Directory where SCOREC is installed")

# If SCOREC_PREFIX was specified, only link to that directory,
# i.e. don't link to another installation in /usr/lib by mistake
if (SCOREC_PREFIX)
  find_package(SCOREC 2.2.0 REQUIRED CONFIG PATHS ${SCOREC_PREFIX} NO_DEFAULT_PATH)
else()
# IF SCOREC_PREFIX was not specified, look in typical system directories,
# and also in CMAKE_PREFIX_PATH (environment variable)
  find_package(
      SCOREC #package name, has to be SCOREC
      2.2.0  #version. can be omitted, and will match any installed version
             #greater than or equal to this one, as long as the major number
             #is the same
      REQUIRED #indicate that SCOREC is really needed to compile
      CONFIG   #skip the 'MODULE' search system, save some time and confusion
      )

endif()

MESSAGE( STATUS "CMAKE_BINARY_DIR:     " ${CMAKE_BINARY_DIR})
MESSAGE( STATUS "Pumi configuration file location: " ${SCOREC_CONFIG})
MESSAGE( STATUS "installation prefix: " ${CMAKE_INSTALL_PREFIX})

# Figure out of Pumi was built with Simmetrix support
get_target_property(SCOREC_LIBS SCOREC::core INTERFACE_LINK_LIBRARIES)
MESSAGE(STATUS ${SCOREC_LIBS})
if(SCOREC_LIBS MATCHES "gmi_sim")
  MESSAGE(STATUS "Found gmi_sim")
  set (HAVE_SIMMETRIX ON)
else()
  MESSAGE(STATUS "gmi_sim not found")
endif()


# Figure out of Pumi was built with Zoltan support
if(SCOREC_LIBS MATCHES "apf_zoltan")
  MESSAGE(STATUS "Found apf_zoltan")
  set (ENABLE_ZOLTAN ON)
else()
  MESSAGE(STATUS "apf_zoltan not found")
endif()

include_directories("${PROJECT_BINARY_DIR}")

# set RPATH for binaries
# use, i.e. don't skip the full RPATH for the build tree
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)

# when building, don't use the install RPATH already
# (but later on when installing)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

# add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# the RPATH to be used when installing, but only if it's not a system directory
LIST(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/lib" isSystemDir)
IF("${isSystemDir}" STREQUAL "-1")
  SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
ENDIF("${isSystemDir}" STREQUAL "-1")

add_executable(ugrid_test ugrid_test.cpp)

target_link_libraries(ugrid_test PRIVATE SCOREC::core)

install (TARGETS ugrid_test DESTINATION bin)