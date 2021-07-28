import argparse
from batch_processor.core.custom_label_handling import generate_volumes_from_label_batch
from os import error
from core.batch_processing import process_batch, process_single
from core.custom_label_handling import generate_volumes_from_label_batch

parser = argparse.ArgumentParser(description="A tool for extracting features from batches of patients.")
parser.add_argument("segment_ids", help="FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'.")

# mode_group = parser.add_mutually_exclusive_group()
# mode_group.add_argument("segmentation_volume_file", help="Path to FreeSurfer segmentation volume")
# mode_group.add_argument("label", help="Path to label file")

label_group = parser.add_argument_group()
label_group.add_argument("--label", help="Path to a label file")
label_group.add_argument("--base_image", help="Path to the FreeSurfer image (mgz) that label was drawn on")

auto_seg_group = parser.add_argument_group()
auto_seg_group.add_argument("--segmentation_volume_file", help="Path to FreeSurfer segmentation volume")

parser.add_argument("patient_directory", help="The base directory in which patient data is stored. All patients found in this directory will be processed.")
parser.add_argument("output_directory", help="A directory to place ERP outputs into.")
args = parser.parse_args()

segments = args.segment_ids.split(',')

for i in range(len(segments)):
    try:
        segments[i] = int(segments[i])
    except ValueError:
        exit(f"Could not convert segment ID '{segments[i]}' into an integer")

errors = []
# TODO only run the label batch processing if the user specifies
results, errors = generate_volumes_from_label_batch(args.label, args.base_image, args.patient_directory, args.label.name + ".mgh")
if len(errors) > 0:
    exit(f"{len(errors)} occurred while generating label files.")
results, errors = process_batch(args.label, )
