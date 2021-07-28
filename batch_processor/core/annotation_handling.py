from pathlib import Path
import subprocess
from typing import Tuple, List


def generate_volumes_from_annotation_batch(annotation_file: Path, base_mri_file: Path, patient_directory: Path) -> Tuple[List[str], List[str]]:
    """generate volumes for all patients in a directory given a single annotation file

    Args:
        annotation_file (Path): filepath to a FreeSurfer annotation file
        base_mri_file (Path): filepath to the FreeSurfer MRI image that the annotation in `annotation_file` was originally drawn on
        patient_directory (Path): directory to the patient directory

    Returns:
        Tuple[List[str], List[str]]: Results (1 item for each subject), errors (1 item for each subject that ERP did not successfully process)
    """
    
    raise NotImplementedError

def generate_volume_from_annotation(annotation_file: Path, base_mri_file: Path) -> Path:
    """generate a FreeSurfer volume from an annotation file

    Args:
        annotation_file (Path): filepath to a FreeSurfer annotation file
        base_mri_file (Path): filepath to the FreeSurfer MRI image that the annotation in `annotation_file` was originally drawn on

    Returns:
        Path: a path to the newly generated volume
    """
    raise NotImplementedError
    # subprocess.run("annot_2_vol #TODO", capture_output=False) # TODO
    
