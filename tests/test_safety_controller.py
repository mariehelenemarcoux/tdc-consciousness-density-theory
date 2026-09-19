from tdc_agent_research.safety import delayed_score, safety_certificate_e842, sequential_multi_certificate

def test_delayed_score_bounds():
    assert delayed_score(0,1,1)==0
    assert 0 <= delayed_score(.5,.5,.5) <= 1

def test_e842_never_upgrades_non_act():
    state={"severe_harm":0,"irreversibility":0,"long_horizon_risk":0,"risk_uncertainty":0,"measurement_integrity":1,"correctability":1}
    assert safety_certificate_e842(state,"PROBE")["action"]=="PROBE"

def test_sequential_requires_three_roots():
    try:
        sequential_multi_certificate([[{"H":0,"I":0,"L":0}]],declared_u=.1,integrity=1,correctability=1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
