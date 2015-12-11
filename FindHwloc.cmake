# Copyright (c)      2014 Thomas Heller
# Copyright (c) 2007-2012 Hartmut Kaiser
# Copyright (c) 2010-2011 Matt Anderson
# Copyright (c) 2011      Bryce Lelbach
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
# Modified by Luis Martinez de Bartolome (Conan.io)


MESSAGE(STATUS "********* Conan FindHwloc wrapper! **********")

find_path(HWLOC_INCLUDE_DIR NAMES hwloc.h PATHS ${CONAN_INCLUDE_DIRS_HWLOC})
find_library(HWLOC_LIBRARY NAMES ${CONAN_LIBS_HWLOC} PATHS ${CONAN_LIB_DIRS_HWLOC})

set(HWLOC_INCLUDE_DIRS ${HWLOC_INCLUDE_DIR})
set(HWLOC_LIBRARIES ${HWLOC_LIBRARY})
set(HWLOC_FOUND 1)

mark_as_advanced(HWLOC_ROOT HWLOC_LIBRARY HWLOC_INCLUDE_DIR)
