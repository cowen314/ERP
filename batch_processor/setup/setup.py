from pathlib import Path
import os
import shutil
import subprocess
import traceback

"""

ERP Setup

Build this into an executable with PyInstaller, then place it next to the ERP executable and the ERP manager
distribution directory like this:

- setup (executable)
- ERP (executable)
- erpman.d (distribution directory)

Run this executable in a shell to kick off the install process

"""

# Define to install process
ERPMAN_DIR = Path("./ERP")  # TODO put a RELATIVE path to the distribution folder here
ERP_DIR = Path("./ERP")  # TODO put a RELATIVE path to the distribution folder here
TARGET_DIR = Path("/usr/local/bin") / "ERP"  # the install path
# USR_VAR_NAME = "erpman"  # set this to a unique user variable name (distinct to the application)


def copy_dist_to_target(source_path: Path, target_path: Path, single_file: bool) -> bool:
    if source_path.exists():
        print("Found file at %s" % source_path.resolve())
    else:
        print("Unable to find the source/distribution directory, looked at %s" % source_path.resolve())
        return False
    if target_path.exists():
        if len(list(target_path.glob("*"))) > 0:
            if input("Files found in install directory (%s). This will be the case if updating from an older version. "
                     "OK to delete these files? (y/N)" % target_path) == 'y':
                shutil.rmtree(target_path)
            else:
                return False
        else:
            target_path.rmdir()  # remove this dir to avoid error from shutil.copytree
    print("Installing to %s" % target_path)
    if single_file:
        shutil.copy(str(source_path), str(target_path))
    else:
        shutil.copytree(str(source_path), str(target_path))


if __name__=="__main__":
    print("setup")
    print("Be sure to run this installer with admin privileges")
    if input("Ready to start installing? (y/N)") == 'y':
        try:
            erp_move_success = copy_dist_to_target(ERP_DIR, TARGET_DIR, single_file=True)
            erp_man_move_success = copy_dist_to_target(ERPMAN_DIR, TARGET_DIR, single_file=False)
        except Exception as e:
            print("Caught exception:")
            traceback.print_exc()
            erp_man_move_success = False
            erp_move_success = False
        if erp_man_move_success and erp_move_success:
            print("Installation successful!")
        else:
            print("Installation failed!")
        input("Press enter to exit")