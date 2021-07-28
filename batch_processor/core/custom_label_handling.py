from pathlib import Path
import subprocess
from typing import Tuple, List
from core.batch_processing import all_patient_dirs


def generate_volumes_from_label_batch(label_file: Path, base_mri_file: Path, patient_directory: Path, new_vol_filename: Path=None, freesurfer_dir: Path="~/freesurfer") -> Tuple[List[str], List[str]]:
    """generate volumes for all patients in a directory given a single label file

    Args:
        label_file (Path): filepath to a FreeSurfer label file
        base_mri_file (Path): filepath to the FreeSurfer MRI image that the label in `label_file` was originally drawn on
        patient_directory (Path): directory to the patient directory

    Returns:
        Tuple[List[str], List[str]]: Results (1 item for each subject), errors (1 item for each subject that ERP did not successfully process)
    """
    if new_vol_filename is None:
        new_vol_filename = label_file.name + ".mgh"
    for patient_dir in all_patient_dirs(patient_directory):
        err = generate_volume_from_label(label_file, base_mri_file, patient_dir / "mri" / new_vol_filename, patient_dir / "mri" / "rawavg.mgh", freesurfer_dir=freesurfer_dir)
        if err:
            exit(err)
    

def generate_volume_from_label(label_file: Path, base_mri_file: Path, output_file: Path, target_mri_file: Path, freesurfer_dir: Path=Path("~/freesurfer")) -> str:
    """generate a FreeSurfer volume from an label file

    Args:
        label_file (Path): filepath to a FreeSurfer label file
        base_mri_file (Path): filepath to the FreeSurfer MRI image that the label in `label_file` was originally drawn on
        output_file (Path): filepath to the write the new volume to
        target_mri_file (Path): filepath to the MRI file to generate this volume for. The label will be remapped onto this volume.

    Returns:
        Path: a path to the newly generated volume
    """
    cmd = [
        str(freesurfer_dir / "bin" / "mri_label2vol"),
        "--label", str(label_file),
        "--o", str(output_file),
        "--regheader", str(base_mri_file),
        "--temp", str(target_mri_file)  # TODO confirm that this works as expected
    ]
    po = subprocess.run(cmd, capture_output=False) # TODO
    if po.returncode > 0:
        return f"Error while generating volume for '{str(target_mri_file)}' from label '{str(label_file)}'"
    else:
        return None
    
