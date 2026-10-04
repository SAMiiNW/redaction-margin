import json, re, time
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus

R = Path(__file__).parents[1]
env = (R.parents[3] / 'accounts.env').read_text()
address = json.loads((R / 'deployment.json').read_text())['contractAddress']
def account(number):
    key = re.search(rf'^ACCOUNT_{number}_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', env, re.M).group(1).strip()
    return create_account(account_private_key=key)
def client(number): return create_client(chain=studionet, account=account(number))
def write(number, name, args):
    c = client(number); tx = c.write_contract(address=address, function_name=name, args=args); print(name + '_tx=' + str(tx), flush=True)
    receipt = c.wait_for_transaction_receipt(transaction_hash=tx, status=TransactionStatus.FINALIZED, retries=180, interval=5000, full_transaction=True)
    leader = (receipt.get('consensus_data', {}).get('leader_receipt') or [{}])[0]
    assert receipt.get('result_name') == 'MAJORITY_AGREE' and leader.get('execution_result') == 'SUCCESS'
    return str(tx)

stamp = str(int(time.time())); record_id = 'DISCLOSURE-' + stamp
full = 'https://raw.githubusercontent.com/SAMiiNW/redaction-margin/ac0c63867eef9f008d83b7ca58ab3005aa73acba/evidence/full-record.md'
public = 'https://cdn.jsdelivr.net/gh/SAMiiNW/redaction-margin@ac0c63867eef9f008d83b7ca58ab3005aa73acba/evidence/public-release.md'
txs = {}
txs['register'] = write(1, 'register_record', [record_id, account(2).address, 'Permit desk public release', full, ['Service desk hours','Applicant contact and internal case number','Appeal deadline','Accessibility assistance'], ['PERSONAL_DATA']])
txs['audit'] = write(2, 'audit_release', [record_id, public])
state = client(1).read_contract(address=address, function_name='get_record', args=[record_id])
assert state['state'] == 'MINIMAL' and state['omitted_indexes'] == [1] and state['unsupported_indexes'] == [] and state['exposed_indexes'] == [] and state['reason_pairs'] == [[1, 0]]
proof = {'recordId':record_id,'transactions':txs,'state':state,'walletDisclosure':'Both wallets and both evidence documents are operator-controlled technical fixtures.'}
(R / 'evidence' / 'live-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2), flush=True)
