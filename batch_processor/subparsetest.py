import argparse

def generate(args):
    print("123")

parser = argparse.ArgumentParser(description="A tool for extracting features from batches of patients.")

subparsers = parser.add_subparsers()

# parser.add_argument("segment_ids", help="FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'.")

generate_parser = subparsers.add_parser("generate", help="Generates features for a list of segment IDs")
generate_parser.add_argument("ids", help="FreeSurfer segment IDs to process. Provide as a comma separated list e.g. '10,17,53,49'.")
generate_parser.set_defaults(func=generate)
# test_parser = subparsers.add_parser("test")
# test_parser.add_argument("test134", help="123?")

args = parser.parse_args()

args.func(args)
pass # figure out how to call a function based on the selected subparser