"""Generate the Stage-002 integrity attack matrix from committed fixtures."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.ipel.chain import verify_chain
clean = json.loads((ROOT/'examples/chains/stage002_clean.json').read_text())
checkpoint = clean['checkpoint']
rows=[]
for path in sorted((ROOT/'examples/chains/attacks').glob('*.json')):
    events=json.loads(path.read_text())['events']
    local=verify_chain(events)
    anchored=verify_chain(events, checkpoint)
    rows.append({
        'attack': path.stem,
        'local_integrity_verified': local.integrity_verified,
        'checkpoint_integrity_verified': anchored.integrity_verified,
        'detected_with_checkpoint': not anchored.integrity_verified,
        'finding_codes': sorted({f.code for f in anchored.findings}),
        'claim_truth_verified': anchored.claim_truth_verified,
    })
print(json.dumps(rows, indent=2))
