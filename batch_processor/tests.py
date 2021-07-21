from pathlib import Path
from core.batch_processing import process_batch, process_single

output, passed = process_single(
    Path("/home/cowen/projects/erp-data/bert-20210604T031952Z-001/bert/mri"),
    Path("/home/cowen/projects/erp-data/batch-process-outputs"),
    [53, 10]
)
# process_batch(Path()) # try this once we have a few more patients to run this on
print(output)
print(passed)