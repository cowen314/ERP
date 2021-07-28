import argparse
from os import error
from batch_processor.core.batch_processing import process_batch, process_single
from batch_processor.core.annotation_handling import generate_volumes_from_annotation_batch

parser = argparse.ArgumentParser(description="A tool for extracting features from batches of patients.")
parser.add_argument("segment_ids", help="FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'.")

# mode_group = parser.add_mutually_exclusive_group()
# mode_group.add_argument("segmentation_volume_file", help="Path to FreeSurfer segmentation volume")
# mode_group.add_argument("annotation_file", help="Path to annotation file")

annotation_group = parser.add_argument_group()
annotation_group.add_argument("annotation_file", help="Path to an annotation file")
annotation_group.add_argument("base_image", help="Path to the FreeSurfer image (mgz) that annotation was drawn on")

auto_seg_group = parser.add_argument_group()
auto_seg_group.add_argument("segmentation_volume_file", help="Path to FreeSurfer segmentation volume")

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
# TODO only run the annotation batch processing if the user specifies
results, errors = generate_volumes_from_annotation_batch()
if len(errors) > 0:
    exit(f"{len(errors)} occurred while generating annotation files.")
results, errors = process_batch()
