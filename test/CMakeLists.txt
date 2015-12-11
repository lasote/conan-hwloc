PROJECT(MyHello)
cmake_minimum_required(VERSION 3.0)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

find_package(Hwloc)

IF(HWLOC_FOUND)
    include_directories(${HWLOC_INCLUDE_DIRS})
    ADD_EXECUTABLE(main main.c)
    TARGET_LINK_LIBRARIES(main ${HWLOC_LIBRARIES})
ELSE()
    MESSAGE(FATAL_ERROR "HWLOC NOT FOUND!")
ENDIF()