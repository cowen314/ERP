from pathlib import Path
import os
import shutil
import subprocess
import traceback
import sys
import argparse
from rich.traceback import install
install(show_locals=True)

"""

ERP Setup

Build this into an executable with PyInstaller, then place it next to the ERP executable and the ERP manager
distribution directory like this:

- setup (executable)
- ERP (executable)
- erpman (executable)

Run this executable in a shell to kick off the install process

"""

parser = argparse.ArgumentParser(description="Setup for erpman")
parser.add_argument("-f", "--force", help="Force the setup to run silently", action="store_true")
args = parser.parse_args()


if getattr(sys, 'frozen', False):  # if in the context of a PyInstaller bundled application
    EXE_DIR = Path(sys.executable).parent
else:
    EXE_DIR = Path(__file__).parent

# Define install source and targets
# ERPMAN_SOURCE_DIRPATH = Path(EXE_DIR) / "erpman"
ERPMAN_EXE_FILEPATH = Path(EXE_DIR) / "erpman"
ERP_EXE_SOURCE_FILEPATH = Path(EXE_DIR) / "ERP"
# INSTALL_DIRECTORY = Path("/usr/local/bin") / "ERP"  # commenting this out for now becauase I'd need to add it to path
INSTALL_DIRECTORY = Path("/usr/local/bin")
# INSTALL_DIRECTORY = Path("C:/Users/cowen/Desktop/Temp")


def check_for_expected_response(prompt_message: str, expected_response: str=None, active: bool=True) -> bool:
    """If active, solicit user input. Return True if the user provides the expected response."""
    if active:
        response = input(prompt_message)
        if expected_response:
            return response == expected_response
        else:
            return True
    else:
        return True


def clear_destination_directory(destination_dir: Path) -> bool:
    if destination_dir.exists():
        if len(list(destination_dir.glob("*"))) > 0:
            if input(f"Files found in install directory ({destination_dir}). This will be the case if updating from an"
                     f"older version. OK to delete these files? (y/N)") == 'y':
                shutil.rmtree(destination_dir)
            else:
                return False
        else:
            destination_dir.rmdir()  # remove this dir to avoid error from shutil.copytree
    return True


def copy_dir_to_target(source_directory: Path, destination_directory: Path) -> bool:
    """

    Args:
        source_directory: a folder to copy
        destination_directory: the parent directory to copy source_directory into

    Returns: True if copy was successful, False otherwise

    """
    if source_directory.exists() and source_directory.is_dir():
        print("Found directory at %s" % source_directory.resolve())
    else:
        print("Unable to find required folder, looked at %s" % source_directory.resolve())
        return False
    print("Copying to %s" % destination_directory)
    shutil.copytree(str(source_directory), str(destination_directory / source_directory.name))
    return True  # if no errors, assume that the copy was a success


def copy_file_to_target(source_file: Path, destination_directory: Path, mode=0o555, prompts: bool=True) -> bool:
    """

    Args:
        source_file: a file to copy
        destination_directory: the directory to copy source_file into

    Returns: True if copy was successful, False otherwise

    """
    if source_file.exists() and source_file.is_file():
        print("Found file at %s" % source_file.resolve())
    else:
        print("Unable to find required file, looked at %s" % source_file.resolve())
        return False
    if not destination_directory.exists():
        destination_directory.mkdir(parents=True, mode=0o777)
    destination_filepath = destination_directory / source_file.name
    if destination_filepath.exists():
        if destination_filepath.is_file():
            if check_for_expected_response(f"Found file at ({destination_filepath}). This is likely hanging around from a previous install. OK to "
                     f"delete this file? (y/N)", expected_response='y', active=args.force):
                destination_filepath.unlink()
            else:
                return False
        else:
            if check_for_expected_response(f"Found a directory where a file was expected ({destination_filepath}). OK to delete this directory? "
                     f"(y/N)", expected_response='y', active=args.force):
                shutil.rmtree(destination_filepath)
            else:
                return False
    print("Copying to file at path %s" % destination_filepath)
    shutil.copyfile(str(source_file), str(destination_filepath))
    destination_filepath.chmod(mode)
    return True  # if no errors, assume that the copy was a success


if __name__=="__main__":
    print("ERP + erpman setup")
    print("Be sure to run this installer with admin privileges")
    if check_for_expected_response("Ready to start installing? (y/N)", expected_response='y', active=args.force):
        # clear_success = False
        erp_man_move_success = False
        erp_move_success = False
        try:
            # clear_success = clear_destination_directory(INSTALL_DIRECTORY)
            erp_move_success = copy_file_to_target(ERP_EXE_SOURCE_FILEPATH, INSTALL_DIRECTORY)
            if erp_move_success:
                # erp_man_move_success = copy_dir_to_target(ERPMAN_SOURCE_DIRPATH, INSTALL_DIRECTORY)
                erp_man_move_success = copy_file_to_target(ERPMAN_EXE_FILEPATH, INSTALL_DIRECTORY)
        except Exception as e:
            print("Caught exception:")
            traceback.print_exc()
        if erp_man_move_success and erp_move_success:
            print("Installation successful!")
        else:
            print("Installation failed!")
        check_for_expected_response("Press enter to exit", expected_response='y', active=args.force)
