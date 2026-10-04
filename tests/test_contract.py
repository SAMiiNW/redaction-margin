import ast
from pathlib import Path

SOURCE = (Path(__file__).parents[1] / 'contracts' / 'contract.py').read_text()
TREE = ast.parse(SOURCE)
def load(name):
    node = next(x for x in TREE.body if isinstance(x, ast.FunctionDef) and x.name == name)
    scope = {}; exec(compile(ast.Module(body=[node], type_ignores=[]), '<contract>', 'exec'), scope); return scope[name]

def test_release_state_prioritizes_exposure():
    state = load('release_state')
    assert state([], []) == 'MINIMAL'
    assert state([2], []) == 'OVERREDACTED'
    assert state([2], [1]) == 'LEAKING'

def test_consensus_binds_every_stored_finding():
    assert 'prompt_comparative' in SOURCE
    for field in ('omitted, unsupported, exposed, reason_pairs, full_digest, and public_digest must match exactly', 'every omission requires a disposition'):
        assert field in SOURCE
    assert 'Every index is zero-based' in SOURCE

def test_lifecycle_and_source_guards_are_present():
    for method in ('register_record', 'audit_release', 'get_record'): assert f'def {method}' in SOURCE
    assert "origin == record.full_origin" in SOURCE
    assert "record.state != 'REGISTERED'" in SOURCE
    assert 'checker.as_hex == gl.message.sender_address.as_hex' in SOURCE
