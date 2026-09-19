from __future__ import annotations
from typing import Any, Mapping
from .safety import integrated_safety_decision, safety_certificate_e842

class TDCResearchV110RC1Adapter:
    """Wrap an existing TDC parent model without rewriting its normative/procedural logic.

    The parent must expose ``decide(state) -> dict`` with an ``action`` key.
    For sequential authorization of ACT, the caller must provide
    ``state["measurement_roots"]`` as three root-local sequences of ``{H,I,L}``
    observations. Root independence is an external trust assumption.

    Fail-closed behavior:
    - upstream E842 is always applied;
    - a parent non-ACT decision is never upgraded;
    - if E842 still permits ACT but measurement roots are absent, the adapter returns PROBE.
    """
    VERSION = "1.10.0-rc1"

    def __init__(self, parent_model):
        self.parent_model = parent_model

    def decide(self, state: Mapping[str, Any]) -> dict[str, Any]:
        parent = self.parent_model.decide(state)
        before = parent['action']
        roots = state.get('measurement_roots')

        if roots is None:
            upstream = safety_certificate_e842(state, before)
            after = upstream['action']
            if after == 'ACT':
                after = 'PROBE'
            out = dict(parent)
            out['action'] = after
            out.setdefault('diagnostics', {})['v1_10_rc1_safety'] = {
                'enabled': True,
                'reason': 'measurement_roots_missing_fail_closed',
                'action_before_safety': before,
                'action_after_safety': after,
                'benefit_used_for_safety_authorization': False,
                'upstream_e842': upstream,
            }
            return out

        safety = integrated_safety_decision(state, before, roots)
        out = dict(parent)
        out['action'] = safety['action']
        out.setdefault('diagnostics', {})['v1_10_rc1_safety'] = {
            'enabled': True,
            'action_before_safety': before,
            'action_after_safety': out['action'],
            'benefit_used_for_safety_authorization': False,
            'details': safety,
        }
        return out
