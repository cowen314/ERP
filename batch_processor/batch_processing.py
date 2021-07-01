import subprocess
from pathlib import Path
from typing import List

# TODO handle labels

ERP_EXE_NAME = "ERP"


def process_batch(subjects_directory: Path, output_directory: Path, segment_ids: List[int]) -> List[str], List[str]:
    """process a batch of patients all at once

    Args:
        subjects_directory (Path): directory with a bunch of subdirectories, one subdirectory for each subject
        output_directory (Path): directory for the ERP outputs
        segment_ids (List[int]): the segment IDs to generate features for

    Returns:
        List[str], List[str]: Results (1 item for each subject), errors (1 item for each subject that ERP did not successfully process)
    """
    errors = []
    results = []
    for folder in subjects_directory:
        # TODO finish this
        msg, success = process_single(folder, output_directory)
        result = f"Processed {folder}, ERP output:\n\n{msg}"
        print(result)
        results += result
        if not success:
            errors += msg
    print(f"Completed batch with {len(errors)} errors")
    return results, errors


def process_single(input_dir: Path, output_dir: Path, segment_ids: List[int], output_images: bool=False) -> str, bool:
    """process a single patient

    Args:
        input_dir (Path): directory with patient data
        output_dir (Path): directory to put the ERP outputs in

    Returns:
        str, bool: status message, status bool (True = pass, False = fail)
    """
    # for readiability, split things out into a bunch of variables
    # erp_cmd = []
    executable_name = ERP_EXE_NAME
    segments_arg = ",".join(segment_ids)
    output_images_arg = 1 if output_images else 0
    erp_cmd = [
        executable_name,
        segments_arg,
        output_images_arg
    ]
    po = subprocess.run(erp_cmd, capture_output=True, cwd=input_dir)
    if po.returncode > 0:
        return po.stdout.decode('ascii'), False
    return po.stdout.decode('ascii'), True
