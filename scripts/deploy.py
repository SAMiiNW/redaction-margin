import hashlib, json, re
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus

R = Path(__file__).parents[1]
env = (R.parents[3] / 'accounts.env').read_text()
key = re.search(r'^ACCOUNT_1_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', env, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=key))
code = (R / 'contracts' / 'contract.py').read_text()
tx = client.deploy_contract(code=code, args=[])
print('deploy_tx=' + str(tx), flush=True)
receipt = client.wait_for_transaction_receipt(transaction_hash=tx, status=TransactionStatus.FINALIZED, retries=180, interval=5000, full_transaction=True)
leader = (receipt.get('consensus_data', {}).get('leader_receipt') or [{}])[0]
address = receipt.get('data', {}).get('contract_address') or receipt.get('to_address')
assert receipt.get('result_name') == 'MAJORITY_AGREE' and leader.get('execution_result') == 'SUCCESS'
out = {'network':'StudioNet','account':'SAMiiNW','contractAddress':address,'deploymentTransaction':str(tx),'deploymentConsensus':receipt.get('result_name'),'deploymentExecution':leader.get('execution_result'),'sourceSha256':hashlib.sha256(code.encode()).hexdigest(),'repository':'https://github.com/SAMiiNW/redaction-margin'}
(R / 'deployment.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2), flush=True)
