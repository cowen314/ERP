from os import error
import subprocess
from pathlib import Path
from typing import List, Tuple

# ERP_EXE_NAME = "ERP"
ERP_EXE_NAME = "echo"  # for use when testing. This'll just print the parameters to stdout. 


def process_batch(subjects_directory: Path, output_directory: Path, segment_ids: List[int], segmentation_volume_rel_path: str) -> Tuple[List[str], List[str]]:
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
        msg, success = process_single(patient_dir / "mri", output_directory, segment_ids, patient_dir / segmentation_volume_rel_path)
        result = f"Processed {patient_dir}, {msg}"
        print(result)
        results += result
        if not success:
            errors += msg
    print(f"Completed batch with {len(errors)} errors")
    return results, errors


def process_single(input_dir: Path, output_dir: Path, segment_ids: List[int], segmentation_volume: Path) -> Tuple[str, bool]:
    """process a single patient

    Args:
        input_dir (Path): directory with patient data
        output_dir (Path): directory to put the ERP outputs in
        segment_ids (List[int]): the segment ids to process with ERP

    Returns:
        str, bool: status message, status bool (True = pass, False = fail)
    """

    errors = []
    for id in segment_ids:
        segment_output_dir = output_dir / input_dir.parent.name / "segment-" / str(id)
        msg, success = call_erp(input_dir, segment_output_dir, id)
        if not success:
            errors.append(f"Segment {id} failed: '{msg}'")
    # FIXME if this tools needs to grow, pass a list of errors out of this function, rather than a formatted string. Keep the formatting and the ERP-call logic separate.
    if len(errors) > 0:
        errors_formatted = '\n\t'.join(errors)
        return f"Some failures occurred while processing: {errors_formatted}"
    return "Processed successfully", True


def call_erp(input_dir: Path, output_dir: Path, segment_id: List[int]) -> Tuple[str, bool]:
    """call the ERP executable via command line, processing a single ROI / segment ID. If the signature of the ERP app changes, this function will probably need to be updated.

    Args:
        input_dir (Path): path to call the ERP app in
        output_dir (Path): location to place the ERP output files in
        segment_id (int): a Freesurfer segment ID

    Returns:
        Tuple[str, bool]: ERP status message; a bool indicating whether ERP ran successfully or not (true = no errors, false = errors)
    """
    # for readiability, split things out into a bunch of variables
    # output_images_arg = '1' if output_images else '0'
    erp_cmd = [
        ERP_EXE_NAME,
        "1",
        str(segment_id)
    ]
    
    ## capture the output, deal with it later
    # po = subprocess.run(erp_cmd, capture_output=True, cwd=input_dir)
    # if po.returncode > 0:
    #     return po.stdout.decode('ascii'), False
    # return po.stdout.decode('ascii'), True

    ## send the output directly to stdout
    po = subprocess.run(erp_cmd, capture_output=False, cwd=input_dir)  # TODO send output to terminal AND capture?
    if po.returncode > 0:
        return f"Error while processing '{str(input_dir.resolve())}'", False
    else:
        # the ERP tool worked as expected, move outputs
        move_all_files_with_pattern(input_dir, output_dir, "*_features.csv")
        return f"Processed '{str(input_dir.resolve())}' successfully", True


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

