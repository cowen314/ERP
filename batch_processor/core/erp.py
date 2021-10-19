from os import error
import subprocess
from pathlib import Path
from typing import List, Union, Tuple
from sys import platform
from rich import print


class ERP:
    def __init__(self, erp_exe_name:Union[List[str], str]="ERP"):
        self._erp_exe_name = erp_exe_name

    def _erp_executable(self, input_dir: Path, segment_id: int, output_dir: Path=None, segmentation_file: str= "aseg.mgh", write_images: bool=False) -> Tuple[str, bool]:
        """call the ERP executable via command line, processing a single ROI / segment ID

        This is meant to be a Python "binding" around the ERP tool.
        If the signature of the ERP app changes, this function will probably need to be updated.

        Args:
            input_dir (Path): path to call the ERP app in
            segment_id (int): a Freesurfer segment ID
            output_dir (optional, Path): location to place the ERP output files in. By default, leave them wherever ERP puts them.
            segmentation_file (optional, str): name of an alternate segmentation file (should be in `input_dir`). By default,
            write_images (optional, bool): whether the tool should write images to disk. Can be helpful for debugging.

        Returns:
            Tuple[str, bool]: ERP status message; a bool indicating whether ERP ran successfully or not (true = no errors, false = errors)
        """

        # prepare ERP parameters
        if type(self._erp_exe_name) is list:
            erp_cmd = list(self._erp_exe_name)  # make a value copy of list
        elif type(self._erp_exe_name) is str:
            erp_cmd = [self._erp_exe_name]
        else:
            raise TypeError("EXE name must be a list or a string")
        slash = '\\' if platform.startswith('win32') or platform.startswith('cygwin') else '/'
        erp_cmd.append(str(input_dir.resolve())+slash)  # ERP does not handle paths well, need to make sure path ends with slash
        erp_cmd.append(str(segment_id))
        erp_cmd.append(segmentation_file)
        if write_images:
            erp_cmd.append("images")

        # send the output directly to stdout so that user can view feedback live
        try:
            po = subprocess.run(erp_cmd, cwd=input_dir)  # TODO capture output, reformat, then pass back up to be displayed live?
        except FileNotFoundError:
            print("Unable to run ERP without shell option, trying again with shell option")
            po = subprocess.run(erp_cmd, shell=True, cwd=input_dir)
        if po.returncode > 0:
            return f"Error while processing '{str(input_dir.resolve())}', with segment ID {segment_id} and segmentation" \
                   f" file '{segmentation_file}'", False
        else:
            # the ERP tool worked as expected
            if output_dir:
                move_all_files_with_pattern(input_dir, output_dir, "*_features.csv")
            return f"Processed '{str(input_dir.resolve())}', with segment ID {segment_id} and segmentation" \
                   f" file '{segmentation_file}' successfully", True

    def process_single(self, input_dir: Path, output_dir: Path, segment_ids: List[int], segmentation_volume: str="aseg.mgh") -> Tuple[List[str], bool]:
        """process a single patient

        Args:
            input_dir (Path): directory with patient data
            output_dir (Path): directory to put the ERP outputs in
            segment_ids (List[int]): the segment ids to process with ERP

        Returns:
            Tuple[List[str], bool]: [list of messages, a bool indicating whether ERP ran successfully or not (true = no
             errors, false = errors)]
        """

        messages = []
        success_overall = True
        for id in segment_ids:
            segment_output_dir = output_dir / input_dir.parent.name / f"segment-{str(id)}"
            msg, success = self._erp_executable(input_dir, id, segment_output_dir, segmentation_volume)
            messages.append(msg)
            if not success:
                success_overall = False
        return messages, success_overall

    def process_batch(self, subjects_directory: Path, output_directory: Path, segment_ids: List[int], segmentation_volume_rel_path: str) -> Tuple[List[str], List[str]]:
        """process a batch of patients all at once

        Args:
            subjects_directory (Path): directory with a bunch of subdirectories, one subdirectory for each subject
            output_directory (Path): directory for the ERP outputs
            segment_ids (List[int]): the segment IDs to generate features for
            segmentation_volume_rel_path (str): a relative path to the segmentation volume (relative to the base directory for each patient)

        Returns:
            List[str], List[str]: Results (1 item for each subject), errors (1 item for each subject that ERP did not successfully process)
        """
        errors = []
        results = []
        for patient_dir in all_patient_dirs(subjects_directory):  # TODO test generator
            msg, success = self.process_single(patient_dir / "mri", output_directory, segment_ids, patient_dir / segmentation_volume_rel_path)
            result = f"Processed {patient_dir}, {msg}"
            print(result)
            results += result
            if not success:
                errors += msg
        print(f"Completed batch with {len(errors)} errors")
        return results, errors


def move_all_files_with_pattern(original_dir: Path, new_dir: Path, pattern: str) -> List[Path]:
    if not new_dir.exists():
        new_dir.mkdir(parents=True)
    output_files = original_dir.glob(pattern)
    output_files_moved = []
    for ofile in output_files:
        output_files_moved.append(ofile.rename(new_dir / ofile.name))
    return output_files_moved


# TODO write a generator that returns a sequence of folders in the patient directory
def all_patient_dirs(base: Path):
    for item in base.glob("*"):
        if item.is_dir:
            yield item

