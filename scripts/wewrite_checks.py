"""Local artifact checks. Semantic accuracy and actual verification remain editorial work."""
import json
import re
from pathlib import Path
import yaml
from wewrite.paths import home
from wewrite.runs import load_run, run_dir
from wewrite.sources import load_sources


def check(run_id=None):
    state = load_run(run_id)
    base = home().resolve()
    directory = run_dir(state['run_id'])
    def artifact(name):
        path = (base / state['artifacts'][name]).resolve()
        if not path.is_relative_to(base):
            raise ValueError('Artifact outside project state')
        return path
    brief = yaml.safe_load(artifact('brief').read_text())
    if brief.get('topic') != state['topic']['title']:
        raise ValueError('Brief must preserve the user-specified topic')
    if state['permissions']['publish'] or state['mode'] != 'draft' or state['visual']['mode'] != 'none':
        raise ValueError('This workflow requires draft / visual none / no publish permission')
    sources = load_sources(state['run_id'])['sources']
    ids = {s['id'] for s in sources}
    notes_path = directory / 'source-verifications.yaml'
    notes = yaml.safe_load(notes_path.read_text()) if notes_path.exists() else {}
    for source in sources:
        if source['status'] == 'verified' and not notes.get(source['id']):
            raise ValueError('Verified source is missing a verification record')
    claims = yaml.safe_load(artifact('claims').read_text()).get('claims', [])
    if not claims:
        raise ValueError('At least one claim is required')
    for claim in claims:
        if claim.get('type') not in {'fact', 'project_claim', 'inference', 'prediction', 'hypothetical'}:
            raise ValueError('Unknown claim type')
        if not claim.get('source_ids') or not set(claim['source_ids']).issubset(ids):
            raise ValueError('Claim references missing source IDs')
        if not claim.get('limitations'):
            raise ValueError('Claim must record evidence scope / limitations')
    for name in ['draft', 'article']:
        text = artifact(name).read_text()
        if not text.strip() or not re.search(r'\[配图：[^\]\n]+\]', text):
            raise ValueError('Article needs a concrete Chinese image placeholder')
        if re.search(r'!\[[^\]]*\]\(|<img\b', text, re.I):
            raise ValueError('Body images are placeholders only')
    report = json.loads(artifact('review_report').read_text())
    editorial = state.get('editorial', {})
    if report.get('decision') != 'pass' or report.get('publishable') is not True or editorial.get('decision') != 'pass' or editorial.get('publishable') is not True:
        raise ValueError('Editorial assessment has not passed')
    return {'ok': True, 'run_id': state['run_id'], 'sources': len(sources), 'claims': len(claims), 'scope': 'artifact consistency only; not factual verification or publication permission'}
