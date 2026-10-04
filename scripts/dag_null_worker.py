"""One dummy-letter schedule. Print the JSON and nothing else."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.dagapeyeff_nulls import worker_report

print(json.dumps(worker_report(int(sys.argv[1]))))
