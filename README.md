# ERP
Epilepsy Radiomics Processing.
## Get Started

### Tools

#### CMake [![versioncmake](https://img.shields.io/badge/CMake-3.15.3-red.svg?style=flat&logo=CMake)](https://cmake.org/)
  1. Download and install CMake from the [CMake website](https://cmake.org/)
#### Git  
  1. Download and install Git, if you don't already have it.
#### Visual Studio Community [![versionvs](https://img.shields.io/badge/Visual%20Studio-16.2-blue.svg?style=flat&logo=visual-studio-code)](https://visualstudio.microsoft.com/vs/community/)
  1. Download Visual Studio (or your desired text editor) just make sure that it can compile C++ files.
#### ITK [![versionitk](https://img.shields.io/badge/ITK-5.0.1-brightgreen.svg?style=flat&logo=data:image/png;base64,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)](https://itk.org/)
  The Insight Toolkit (ITK) must be installed and compiled in order to be able to build the project 
  1. Download ITK from the [ITK website](https://itk.org)
  2. Use CMake to configure ITK [See note on MGH/MHZ files below](#MGH/MHZ-files) 
  3. Open the .sln file generated in Visual Studio (see below)

  

### MGH/MHZ files
In order to use the files that come directly from Freesurfer in MGH or MHZ format is is necessary to have Git installed in the computer at the time of the ITK build.
Also, the Module_MGHIO must be selected. Otherwise, the program might cause some problems when running. 


### Detailed build instructions

These instuctions were written specifically for an Ubuntu machine, but the process should be similar on other platforms.

1. Download and install CMake
    1. `apt-get install cmake`
1. Download, configure, build, and install VTK
    1. [Download the VTK source code](https://vtk.org/download/)
    1. `cmake -S vtk-src -B vtk-bin` to configure VTK (where `vtk-src` is the directory that downloaded VTK source code was placed in, and `vtk-bin` is an arbitrary directory)
        1. this step failed for me the first time I ran it because an OpenGL implementation needed to be on the system. [This post](https://stackoverflow.com/questions/31170869/cmake-could-not-find-opengl-in-ubuntu) was helpful.
    1. `cmake --build vtk-bin` to build VTK 
1. Download, configure, build, and install ITK
    1. [Download the ITK source code](https://itk.org/download/)
    1. `cmake -D Module_MGHIO:BOOL=ON -D Module_ITKVtkGlue:BOOL=ON -S itk-src/ -B itk-bin/` to configure VTK (where `itk-src` is the directory that downloaded VTK source code was placed in, and `itk-bin` is an arbitrary directory)
        1. Note that this step configures ITK with MGHIO support (which is needed to read in the Freesurfer MGH/MGZ files) and VTK Glue support  
1. Clone, configure, and build ERP
    1. `git clone https://github.com/cowen314/ERP.git`
    1. `cmake -S ERP -B erp-bin`
    1. `cmake --build erp-bin`
