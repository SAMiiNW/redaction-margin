import base64, hashlib, json
from pathlib import Path
from genlayer_py import create_client
from genlayer_py.chains import studionet

R = Path(__file__).parents[1]
d = json.loads((R / 'deployment.json').read_text())
tx = create_client(chain=studionet).get_transaction(transaction_hash=d['deploymentTransaction'])
deployed = base64.b64decode(tx['data']['contract_code'], validate=True)
local = (R / 'contracts' / 'contract.py').read_text().encode()
leader = (tx.get('consensus_data', {}).get('leader_receipt') or [{}])[0]
out = {'contract':d['contractAddress'],'deploymentTransaction':d['deploymentTransaction'],'status':tx.get('status_name'),'consensus':tx.get('result_name'),'execution':leader.get('execution_result'),'sourceSha256':hashlib.sha256(deployed).hexdigest(),'sourceMatches':deployed == local}
assert out['status'] == 'FINALIZED' and out['consensus'] == 'MAJORITY_AGREE' and out['execution'] == 'SUCCESS' and out['sourceMatches']
(R / 'evidence' / 'deployment-verification.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
