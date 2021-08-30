from pathlib import Path
from typing import List, Tuple

truth = Path("/home/cowen/projects/erp-data/bert-standard-processed/rawavg_auto_features.csv")
test = Path("/home/cowen/projects/erp-data/bert-lhip-test-2021-08-29/rawavg_features.csv")
out_f = Path("/home/cowen/projects/erp-data/lhip-solo-process-vs-group-process-comparison.csv")
# truth_start_line = 86
# truth_end_line = 127
# test_start_line = 2
# test_end_line = 43

truth_start_line = 2
truth_end_line = 43
test_start_line = 2
test_end_line = 43

def split_and_clean(csv_text: str, start_line: int, stop_line: int) -> List[Tuple[str]]:
    lines = csv_text.split("\n")
    cleaned = []
    lines = lines[start_line-1:stop_line]
    for line in lines:
        name_value = line.split(',')
        cleaned.append((name_value[0].strip(), name_value[1].strip()))
    return cleaned


truth_data = split_and_clean(truth.read_text(), truth_start_line, truth_end_line)
test_data = split_and_clean(test.read_text(), test_start_line, test_end_line)
comparison = ""
for i in range(truth_end_line - truth_start_line + 1):
    try:
        error = 100*(abs(float(truth_data[i][1]) - float(test_data[i][1])) / abs(float(truth_data[i][1])))
    except ZeroDivisionError:
        error = f"{abs(float(truth_data[i][1]) - float(test_data[i][1]))} / {float(truth_data[i][1])}"
    comparison+=(f"% error for '{truth_data[i][0]}': {error}\n")

print(comparison)
with open(out_f, "w") as fh:
    fh.write(comparison)
