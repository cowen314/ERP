cmake_minimum_required(VERSION 2.8)
 
project(ERP)
# set(CMAKE_PREFIX_PATH "C:\\ITK_bin\\;C:\\VTK_bin\\")
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})
if (ITKVtkGlue_LOADED)
  find_package(VTK REQUIRED)
  include(${VTK_USE_FILE})
else()
  find_package(ItkVtkGlue REQUIRED)
  include(${ItkVtkGlue_USE_FILE})
  set(Glue ItkVtkGlue)
endif()


# add_executable(ERP MACOSX_BUNDLE ERP.cxx)
add_executable(ERP ERP.cxx)
target_link_libraries(ERP ${Glue}  ${VTK_LIBRARIES} ${ITK_LIBRARIES})
