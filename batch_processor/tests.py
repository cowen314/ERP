from .batch_processing import process_batch, process_single
from pathlib import Path

process_single(
    Path("../../erp-data/bert-20210604T031952Z-001/bert/mri"),
    Path("../../erp-data/batch-process-outputs"),
    [53, 10]
)
# process_batch(Path()) # try this once we have a few more patients to run this on