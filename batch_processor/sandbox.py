from pathlib import Path
from core.erp import all_patient_dirs

for dir in all_patient_dirs(Path("./")):
    print(dir.absolute())