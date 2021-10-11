from pathlib import Path
from core.erp import process_batch, process_single, move_all_files_with_pattern

'''Make sure that a single pass works. Change paths as needed.'''
output, passed = process_single(
    Path("/home/cowen/projects/erp-data/bert-20210604T031952Z-001/bert/mri"),
    Path("/home/cowen/projects/erp-data/batch-process-outputs"),
    [53, 10]
)
print(output)
print(passed)

'''Make sure that files move around properly'''
move_all_files_with_pattern(Path("/home/cowen/Desktop/bert-outputs-test"), Path("/home/cowen/Desktop/new-dir"), "*_features.csv")

# process_batch(Path()) # try this once we have a few more patients to run this on
