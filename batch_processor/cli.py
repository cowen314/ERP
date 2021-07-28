import argparse
from batch_processor.core.batch_processing import process_batch, process_single

parser = argparse.ArgumentParser()
parser.add_argument("segment_ids", help="FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'.")
parser.add_argument("patient_directory", help="The base directory in which patient data is stored. All patients found in this directory will be processed.")
parser.add_argument("output_directory", help="A directory to place ERP outputs into.")
args = parser.parse_args()

segments = args.segment_ids.split(',')

for i in range(len(segments)):
    try:
        segments[i] = int(segments[i])
    except ValueError:
        exit(f"Could not convert segment ID '{segments[i]}' into an integer")

process_batch()
