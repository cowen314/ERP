import argparse
from datetime import datetime

from core.custom_label_handling import generate_volumes_from_label_batch
from os import error
from core.erp import ERP
from core.custom_label_handling import generate_volumes_from_label_batch
from pathlib import Path
from rich import print
from rich.traceback import install

install(show_locals=True)


def _erp_process_single(erp: ERP, args):
    segments = args.segment_ids.split(',')

    for i in range(len(segments)):
        try:
            segments[i] = int(segments[i])
        except ValueError:
            exit(
                f"Could not convert segment ID '{segments[i]}' into an integer"
            )

    statuses, passed = erp.process_single(
        Path(args.input_directory),
        Path(args.input_directory),
        segments,
        segmentation_volume=args.segmentation_volume)

    status_str = "\n > ".join(statuses)
    if passed:
        print(f"Operation succeeded\n > {status_str}")
    else:
        print(f"Operation failed\n > {status_str}")


def _erp_process_multiple(erp: ERP, args):
    segments = args.segment_ids.split(',')

    for i in range(len(segments)):
        try:
            segments[i] = int(segments[i])
        except ValueError:
            exit(
                f"Could not convert segment ID '{segments[i]}' into an integer"
            )

    output_directory: Path = Path(
        args.freesurfer_patient_directory) / "erpman-outputs"
    output_directory.mkdir(mode=0o666, exist_ok=True)
    batch_directory = output_directory / datetime.now().strftime(
        "%Y%m%d-%H%M%S")
    batch_directory.mkdir(mode=0o666, exist_ok=False)
    statuses, errors = erp.process_batch(
        Path(args.freesurfer_patient_directory),
        batch_directory,
        segments,
        segmentation_volume_rel_path=args.segmentation_volume)

    status_str = "\n > ".join(statuses)
    if len(errors) == 0:
        print(f"Operation succeeded\n > {status_str}")
    else:
        print(f"Operation failed\n > {status_str}")


parser = argparse.ArgumentParser(
    description="A tool for extracting features from batches of patients.")
parser.add_argument("--executable-name",
                    dest="executable_name",
                    help="The name of the ERP executable.",
                    default="ERP")

subparsers = parser.add_subparsers()
generate_parser = subparsers.add_parser(
    "process-single",
    help="Generates features for any number of segment IDs on a single patient"
)
generate_parser.add_argument(
    "input_directory",
    help="A directory with patient data (rawavg.mgh and a segmentation volume)."
)
generate_parser.add_argument(
    "segment_ids",
    help=
    "FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'."
)
# generate_parser.add_argument("--output-directory", dest="output_directory", help="A directory to move feature CSVs to after ERP completes.")
generate_parser.add_argument(
    "--segmentation-volume",
    dest="segmentation_volume",
    help="Name of the segmentation volume to use ('aseg.mgh' by default).",
    default='aseg.mgh')
generate_parser.set_defaults(func=_erp_process_single)

generate_parser = subparsers.add_parser(
    "process-multiple",
    help="Generates features for any number of segment IDs on multiple patients"
)
generate_parser.add_argument(
    "freesurfer_patient_directory",
    help=
    "A directory with patient data (which contains several subfolders; each subfolder should contain an /mri folder with a rawavg.mgh and a segmentation volume)."
)
generate_parser.add_argument(
    "segment_ids",
    help=
    "FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'."
)
# generate_parser.add_argument("--output-directory", dest="output_directory", help="A directory to move feature CSVs to after ERP completes.")
generate_parser.add_argument(
    "--segmentation-volume",
    dest="segmentation_volume",
    help="Name of the segmentation volume to use ('aseg.mgh' by default).",
    default='aseg.mgh')
generate_parser.set_defaults(func=_erp_process_multiple)
'''
TODO Generate features for several patients with a single command

Inputs:
- A directory with the MRIs and segmentations of many patients (standard FreeSurfer format)
- A list of segment IDs to generate features for **OR** a label file, along with the MRI that the label was originally drawn on

Output:
- CSVs with features
'''
''' 
this section contains old stuff that'll probably get deleted

# mode_group = parser.add_mutually_exclusive_group()
# mode_group.add_argument("segmentation_volume_file", help="Path to FreeSurfer segmentation volume")
# mode_group.add_argument("label", help="Path to label file")

# label_group = parser.add_argument_group()
# label_group.add_argument("--label", help="Path to a label file")
# label_group.add_argument("--base_image", help="Path to the FreeSurfer image (mgh) that label was drawn on")

# auto_seg_group = parser.add_argument_group()
# auto_seg_group.add_argument("--segmentation_volume_file", help="Path to FreeSurfer segmentation volume")

# parser.add_argument("patient_directory", help="The base directory in which patient data is stored. All patients found in this directory will be processed.")
# parser.add_argument("output_directory", help="A directory to place ERP outputs into.")
'''

args = parser.parse_args()
erp = ERP(erp_exe_name=args.executable_name.split(' '))
if hasattr(args, "func"):
    print(args.segmentation_volume)
    args.func(erp, args)
else:
    print(
        "A subcommand must be specified. Run this tool with '--help' to display help."
    )

# TODO process batch
# TODO generate a segmentation volume from a label file, then use that

# TODO only run the label batch processing if the user specifies
# errors = []
# results, errors = generate_volumes_from_label_batch(args.label, args.base_image, args.patient_directory, args.label.name + ".mgh")
# if len(errors) > 0:
#     exit(f"{len(errors)} occurred while generating label files.")
# results, errors = process_batch(args.label, args.output_directory, segments)
