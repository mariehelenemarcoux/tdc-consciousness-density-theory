from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence
import math
import numpy as np

SEVERITY_THRESHOLD = 0.80
IRREVERSIBLE_THRESHOLD = 0.50
LONG_HARM_THRESHOLD = 0.60
LONG_HORIZON_THRESHOLD = 0.75
DELAYED_JOINT_THRESHOLD = 0.58
N_ROOTS = 3
ROOT_QUORUM = 2
MAX_ROUNDS = 10

T95_ONE_SIDED = {1:6.3138,2:2.9200,3:2.3534,4:2.1318,5:2.0150,6:1.9432,7:1.8946,8:1.8595,9:1.8331}


def clip01(x: float) -> float:
    return float(np.clip(float(x), 0.0, 1.0))


def delayed_score(H: float, I: float, L: float) -> float:
    return float(np.cbrt(np.clip(float(H)*float(I)*float(L), 0.0, 1.0)))


@dataclass(frozen=True)
class Interval:
    mean: float
    lower: float
    upper: float
    n: int


@dataclass(frozen=True)
class RootCertificate:
    status: str
    risk_severity: bool
    risk_irreversible: bool
    risk_long_horizon: bool
    risk_delayed: bool
    safe_severity: bool
    safe_irreversible: bool
    safe_long_horizon: bool
    safe_delayed: bool


def one_sided_interval(history: Sequence[float], declared_u: float, integrity: float) -> Interval:
    values = np.asarray(history, dtype=float)
    n = len(values)
    if n == 0:
        raise ValueError("history must contain at least one observation")
    mean = float(np.mean(values))
    if n < 2:
        return Interval(mean, 0.0, 1.0, n)
    if n > 10:
        values = values[:10]
        n = len(values)
        mean = float(np.mean(values))
    sd = float(np.std(values, ddof=1))
    empirical = T95_ONE_SIDED[n-1] * sd / math.sqrt(n)
    declared = float(declared_u) / math.sqrt(n)
    integrity_penalty = 0.50 * (1.0 - float(integrity))
    halfwidth = max(empirical, declared) + integrity_penalty
    return Interval(mean, clip01(mean-halfwidth), clip01(mean+halfwidth), n)


def classify_root(intervals: Mapping[str, Interval]) -> RootCertificate:
    H, HI, L, D = intervals['H'], intervals['HI'], intervals['L'], intervals['D']
    risk_severity = H.lower >= SEVERITY_THRESHOLD
    risk_irreversible = HI.lower >= IRREVERSIBLE_THRESHOLD
    risk_long = H.lower >= LONG_HARM_THRESHOLD and L.lower >= LONG_HORIZON_THRESHOLD
    risk_delayed = D.lower >= DELAYED_JOINT_THRESHOLD
    risk = risk_severity or risk_irreversible or risk_long or risk_delayed

    safe_severity = H.upper < SEVERITY_THRESHOLD
    safe_irreversible = HI.upper < IRREVERSIBLE_THRESHOLD
    safe_long = H.upper < LONG_HARM_THRESHOLD or L.upper < LONG_HORIZON_THRESHOLD
    safe_delayed = D.upper < DELAYED_JOINT_THRESHOLD
    safe = safe_severity and safe_irreversible and safe_long and safe_delayed
    status = 'RISK' if risk else ('SAFE' if safe else 'UNCERTAIN')
    return RootCertificate(status, risk_severity, risk_irreversible, risk_long, risk_delayed,
                           safe_severity, safe_irreversible, safe_long, safe_delayed)


def safety_certificate_e842(state: Mapping[str, Any], parent_action: str) -> dict[str, Any]:
    """Release-engineering implementation of the frozen E842 fail-closed envelope.

    It can only downgrade parent ACT. It never authorizes ACT when the parent did not.
    """
    H = clip01(state.get('severe_harm', 0.0)); I = clip01(state.get('irreversibility', 0.0)); L = clip01(state.get('long_horizon_risk', 0.0))
    U = clip01(state.get('risk_uncertainty', 0.0)); integrity = clip01(state.get('measurement_integrity', 1.0))
    buf = clip01(2.50*U + 0.50*(1.0-integrity))
    Hp, Ip, Lp = clip01(H+buf), clip01(I+buf), clip01(L+buf)
    keys = ['systemic_scope','systemic_propagation','systemic_persistence','systemic_cascade','systemic_lock_in','systemic_accumulation','systemic_long_horizon']
    vals = {k:clip01(clip01(state.get(k,0.0))+buf) for k in keys}
    sys_score = max(
        math.sqrt(vals['systemic_scope']*vals['systemic_propagation']),
        math.sqrt(vals['systemic_cascade']*vals['systemic_scope']),
        math.sqrt(vals['systemic_lock_in']*vals['systemic_persistence']),
        math.sqrt(vals['systemic_accumulation']*vals['systemic_long_horizon']),
    )
    critical = (Hp >= 0.80) or (Hp*Ip >= 0.50) or (Hp >= 0.60 and Lp >= 0.75)
    systemic = sys_score >= 0.70
    epistemic = integrity >= 0.60 and U <= 0.50
    certified = (not critical) and (not systemic) and epistemic
    action = str(parent_action)
    if action == 'ACT':
        if critical or systemic:
            action = 'TRANSFORM' if clip01(state.get('correctability',0.0)) >= 0.45 else 'ABSTAIN'
        elif not epistemic:
            action = 'PROBE'
    return {
        'action': action, 'safety_certified': certified, 'critical': critical, 'systemic': systemic,
        'epistemically_certified': epistemic, 'risk_buffer': buf, 'H_upper': Hp, 'I_upper': Ip, 'L_upper': Lp,
        'systemic_score': sys_score,
    }


def sequential_multi_certificate(root_rounds: Sequence[Sequence[Mapping[str,float]]], *, declared_u: float,
                                 integrity: float, correctability: float, upstream_action: str='ACT',
                                 max_rounds: int=MAX_ROUNDS) -> dict[str, Any]:
    """Apply the frozen sequential 3-root / 2-of-3 safety verifier.

    `root_rounds` must contain exactly three roots. Each root is a sequence of observations
    with keys H, I, L. Causal independence of roots is an external assumption.
    """
    if upstream_action != 'ACT':
        return {'action':upstream_action,'resolution_round':0,'safe_votes':0,'risk_votes':0,'root_independence_assumed':True}
    if len(root_rounds) != N_ROOTS:
        raise ValueError(f'exactly {N_ROOTS} roots are required')
    available = min(max_rounds, *(len(r) for r in root_rounds))
    if available < 1:
        raise ValueError('each root must contain at least one measurement')
    histories = [{k:[] for k in ('H','L','HI','D')} for _ in range(N_ROOTS)]
    last = None
    for round_id in range(1, available+1):
        for root_id in range(N_ROOTS):
            m = root_rounds[root_id][round_id-1]
            H,I,L = clip01(m['H']),clip01(m['I']),clip01(m['L'])
            histories[root_id]['H'].append(H); histories[root_id]['L'].append(L)
            histories[root_id]['HI'].append(H*I); histories[root_id]['D'].append(delayed_score(H,I,L))
        certs=[]
        for hist in histories:
            intervals={k:one_sided_interval(v,declared_u,integrity) for k,v in hist.items()}
            certs.append(classify_root(intervals))
        safe_votes=sum(c.status=='SAFE' for c in certs); risk_votes=sum(c.status=='RISK' for c in certs)
        last={'resolution_round':round_id,'safe_votes':safe_votes,'risk_votes':risk_votes,
              'severity_votes':sum(c.risk_severity for c in certs),'irreversible_votes':sum(c.risk_irreversible for c in certs),
              'long_votes':sum(c.risk_long_horizon for c in certs),'delayed_votes':sum(c.risk_delayed for c in certs),
              'root_independence_assumed':True}
        if risk_votes >= ROOT_QUORUM:
            return {'action':'TRANSFORM' if clip01(correctability)>=0.45 else 'ABSTAIN', **last}
        if safe_votes >= ROOT_QUORUM:
            return {'action':'ACT', **last}
    return {'action':'PROBE', **last}


def integrated_safety_decision(state: Mapping[str,Any], parent_action: str,
                               root_rounds: Sequence[Sequence[Mapping[str,float]]]) -> dict[str,Any]:
    upstream = safety_certificate_e842(state, parent_action)
    seq = sequential_multi_certificate(root_rounds, declared_u=clip01(state.get('risk_uncertainty',0.0)),
                                       integrity=clip01(state.get('measurement_integrity',1.0)),
                                       correctability=clip01(state.get('correctability',0.0)),
                                       upstream_action=upstream['action'])
    return {'action':seq['action'],'upstream_e842':upstream,'sequential':seq,
            'benefit_used_for_safety_authorization':False}
