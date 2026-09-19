import math
from tdc_research_v1_10_rc1.safety import integrated_safety_decision, sequential_multi_certificate, safety_certificate_e842

def roots(H,I,L,n=10):
    return [[{'H':H,'I':I,'L':L} for _ in range(n)] for _ in range(3)]

def base_state(**kw):
    s=dict(severe_harm=0.05,irreversibility=0.05,long_horizon_risk=0.05,risk_uncertainty=0.01,measurement_integrity=1.0,
           systemic_scope=0.05,systemic_propagation=0.05,systemic_persistence=0.05,systemic_cascade=0.05,systemic_lock_in=0.05,
           systemic_accumulation=0.05,systemic_long_horizon=0.05,correctability=0.8)
    s.update(kw); return s

def test_safe_case_recovers_act():
    out=integrated_safety_decision(base_state(), 'ACT', roots(.05,.05,.05))
    assert out['action']=='ACT'

def test_extreme_severity_is_noncompensable():
    out=sequential_multi_certificate(roots(.95,.08,.08),declared_u=.01,integrity=1.0,correctability=.8)
    assert out['action']!='ACT'

def test_delayed_joint_risk_is_blocked():
    out=sequential_multi_certificate(roots(.30,.97,.97),declared_u=.01,integrity=1.0,correctability=.8)
    assert out['action']!='ACT'

def test_one_compromised_root_does_not_authorize_hazard():
    r=roots(.30,.97,.97)
    r[0]=[{'H':.02,'I':.10,'L':.10} for _ in range(10)]
    out=sequential_multi_certificate(r,declared_u=.01,integrity=1.0,correctability=.8)
    assert out['action']!='ACT'

def test_upstream_non_act_cannot_be_upgraded():
    out=sequential_multi_certificate(roots(.01,.01,.01),declared_u=.01,integrity=1.0,correctability=.8,upstream_action='PROBE')
    assert out['action']=='PROBE'

def test_systemic_e842_blocks():
    s=base_state(systemic_scope=.9,systemic_propagation=.9)
    out=safety_certificate_e842(s,'ACT')
    assert out['action']!='ACT'


def test_adapter_missing_measurement_roots_fails_closed():
    from tdc_research_v1_10_rc1.adapter import TDCResearchV110RC1Adapter

    class Parent:
        def decide(self, state):
            return {"action": "ACT", "diagnostics": {}}

    out = TDCResearchV110RC1Adapter(Parent()).decide(base_state())
    assert out["action"] == "PROBE"
    assert out["diagnostics"]["v1_10_rc1_safety"]["reason"] == "measurement_roots_missing_fail_closed"
