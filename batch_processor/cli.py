import argparse
from core.custom_label_handling import generate_volumes_from_label_batch
from os import error
from core.erp import process_batch, process_single
from core.custom_label_handling import generate_volumes_from_label_batch

def generate(args):
    segments = args.segment_ids.split(',')

    for i in range(len(segments)):
        try:
            segments[i] = int(segments[i])
        except ValueError:
            exit(f"Could not convert segment ID '{segments[i]}' into an integer")
    for id in segments:
        status, passed = process_single(args.input_dir, args.input_dir, id)
        if passed:
            print(f"Segment ID {id} processed successfully. Status: {status}")
        else:
            print(f"Unable to process segment ID {id}. Status: {status}")

'''
Generate features for several patients with a single command

Inputs:
- A directory with the MRIs and segmentations of many patients (standard FreeSurfer format)
- A list of segment IDs to generate features for **OR** a label file, along with the MRI that the label was originally drawn on

Output:
- CSVs with features
'''

parser = argparse.ArgumentParser(description="A tool for extracting features from batches of patients.")

subparsers = parser.add_subparsers()
generate_parser = subparsers.add_parser("generate", help="Generates features for any number of segment IDs")
generate_parser.add_argument("segment_ids", help="FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'.")
parser.add_argument("input_directory", help="A directory with patient data (rawavg.mgh and aseg.mgh).")
generate_parser.set_defaults(func=generate)
''' 
this section contains old stuff that'll probably go

# mode_group = parser.add_mutually_exclusive_group()
# mode_group.add_argument("segmentation_volume_file", help="Path to FreeSurfer segmentation volume")
# mode_group.add_argument("label", help="Path to label file")

# label_group = parser.add_argument_group()
# label_group.add_argument("--label", help="Path to a label file")
# label_group.add_argument("--base_image", help="Path to the FreeSurfer image (mgz) that label was drawn on")

# auto_seg_group = parser.add_argument_group()
# auto_seg_group.add_argument("--segmentation_volume_file", help="Path to FreeSurfer segmentation volume")

# parser.add_argument("patient_directory", help="The base directory in which patient data is stored. All patients found in this directory will be processed.")
# parser.add_argument("output_directory", help="A directory to place ERP outputs into.")
'''

args = parser.parse_args()
args.func(args)

# TODO only run the label batch processing if the user specifies
# errors = []
# results, errors = generate_volumes_from_label_batch(args.label, args.base_image, args.patient_directory, args.label.name + ".mgh")
# if len(errors) > 0:
#     exit(f"{len(errors)} occurred while generating label files.")
# results, errors = process_batch(args.label, args.output_directory, segments)
