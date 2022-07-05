# ERP
Epilepsy Radiomics Processing.

## General Info

This tool extracts features from MRI images. The images must be in the MGH/MGZ (Freesurfer) format.

## Using the tool

* The ERP tool only needs the path to a folder containing a segmentation file and an MRI. If no other arguments are provided, ERP will generate features for the left hippocampus (segment ID 17), right hippocampus (53), left thalamus (10), and right thalamus (49).
* Optionally, a segment ID may be provided as the second argument. In this case, features will be extracted from the segment ID provided as opposed to the 4 regions listed above.
* Optionally, a segment ID and the name of an alternate segmentation file can be provided (as the second and third arguments, respectively). In this case, features will be extracted from the segment ID provided AND the alternate segmentation volume will be used instead of aseg.mgh.
* If there are more than 3 arguments, everything from the last bullet will happen, and processed image files will be written to disk.

### Examples

1. `./ERP ../erp-data/bert/` will extract features from `../erp-data/bert/rawavg.mgh` using `../erp-data/bert/aseg.mgh`. Features will be extracted from 4 regions; the left hippocampus (segment ID 17), right hippocampus (53), left thalamus (10), and right thalamus (49).
1. `./ERP ../erp-data/bert/ 17` will extract features from `../erp-data/bert/rawavg.mgh` using `../erp-data/bert/aseg.mgh`. Features will extracted from the from region specified (in this case segment ID 17, the left hippocampus).
1. `./ERP ../erp-data/bert/ 1 roi.mgh` will extract features from `../erp-data/bert/rawavg.mgh` using `../erp-data/bert/roi.mgh` instead of `../erp-data/bert/aseg.mgh`. Features will be extracted from segment ID 1.
1. `./ERP ../erp-data/bert/ 1 roi.mgh files` will do everything above, and processed image files will be written to disk.

## ERP Build Instructions

These instuctions were written specifically for an Linux (Ubuntu) machine, but the process should be similar on other platforms.

1. Download and install git
    1. `apt install git`
1. Download and install CMake
    1. `apt install cmake`
1. Download, configure, and build VTK
    1. [Download the VTK source code](https://vtk.org/download/)
    1. Run `cmake -S vtk-src -B vtk-bin` to configure VTK (where `vtk-src` is the directory that downloaded VTK source code was placed in, and `vtk-bin` is an arbitrary directory to place VTK makefiles and binaries in)
        1. As of 2021 04 21, an OpenGL implementation might need to be present on the system. [This post](https://stackoverflow.com/questions/31170869/cmake-could-not-find-opengl-in-ubuntu) may be helpful.
        2. If cmake complains about compiler support, `sudo apt install build-essential` may help
    1. Run `cmake --build vtk-bin` to build VTK 
1. Download, configure, and build ITK
    1. [Download the ITK source code](https://itk.org/download/)
    1. Run `cmake -D Module_MGHIO:BOOL=ON -D Module_ITKVtkGlue:BOOL=ON -D VTK_DIR:PATH=/home/cowen/vtk-bin/ -S itk-src/ -B itk-bin/` to configure VTK (where `itk-src` is the directory that downloaded VTK source code was placed in, and `itk-bin` is an arbitrary directory to place ITK makefiles and binaries in)
        1. Note that this step configures ITK with MGHIO support (which is needed to read in the Freesurfer MGH/MGZ files) and VTK Glue support  
        1. `VTK_DIR:PATH=/home/cowen/vtk-bin/` tells ITK where to look for VTK. VTK is required because the ITKVTKGlue module depends on it. Change `/home/cowen/vtk-bin/` to wherever `vtk-bin` is (from the prior step).
    1. Run `cmake --build itk-bin` to build ITK 
1. Clone, configure, and build ERP
    1. Run `git clone https://github.com/cowen314/ERP.git` to clone the repo
    1. Run `cmake -D ITK_DIR:PATH=/home/cowen/itk-bin -S ERP -B erp-bin/` to configure the ERP tool. `/home/cowen/itk-bin` should be wherever `itk-bin` is (from "*Download, configure, and build ITK*"). 
    1. Run `cmake --build erp-bin` to build the ERP tool. 
1. Run ERP. See "Using the tool" for more information.

## ERP Manager

ERP Manager (erpman) is a tool that wraps around ERP to provide additional functionality.

## Distribution

ERP and ERP manager can distributed + installed together with the help of a Python script (`setup.py`).

### Building the Distribution From Scratch

1. Clone the repository (e.g. `git clone git@github.com:cowen314/ERP.git`)
2. Create a new virtual environment with `python -m venv venv`
3. Activate the virtual environment with `source ./venv/bin/activate`
4. Install all required python packages with `pip -r requirements.txt`
5. Switch to erpman directory with `cd batch_processor`
6. Build the setup script with `pyinstaller --onefile setup/setup.py`
7. Build erpman with `pyinstaller --onefile --name erpman cli.py`
8. Build ERP (using the steps above)
9. Put the ERP executable in the dist directory alongside erpman and the setup executable
10. Distribute entire dist directory. To install, run the setup executable.

To officially release a new version, compress the contents of the dist directory (ERP, erpman, and setup; `cd dist` then `tar -czvf erpman-x.y.z.tar.gz *`), then upload to a new GitHub release.

## Common Problems

### Exec format error

#### Description

`cannot execute binary file: Exec format error` when trying to run the executable

#### Possible solution

Make sure the executable was built on a similar platform as the one you're running it on. As of 2022 06 23, Ubuntu 18.04 is the recommended distribution for building and running these applications.
