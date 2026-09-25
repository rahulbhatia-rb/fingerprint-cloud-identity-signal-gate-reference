import json, sys
from pathlib import Path

def evaluate(s, p):
    reasons=[]
    if s['identity_confidence'] < p['min_identity_confidence']: reasons.append('identity confidence below policy')
    if s['signal_age_ms'] > p['max_signal_age_ms']: reasons.append('identity signal is stale')
    if s['fraud_error_rate'] > p['max_fraud_error_rate']: reasons.append('fraud decision error rate elevated')
    if not s['replicas_healthy']: reasons.append('identity service capacity unhealthy')
    return {'allow_sensitive_action':not reasons,'reasons':reasons}

def run(p):
    d=json.loads(Path(p).read_text()); return evaluate(d['signals'],d['policy'])
if __name__=='__main__':
    if sys.argv[1:]==['--self-test']:
        assert evaluate({'identity_confidence':.99,'signal_age_ms':20,'fraud_error_rate':.001,'replicas_healthy':True},{'min_identity_confidence':.9,'max_signal_age_ms':100,'max_fraud_error_rate':.01})['allow_sensitive_action'];print('identity gate: passed')
    else: print(json.dumps(run(sys.argv[1]),indent=2))
