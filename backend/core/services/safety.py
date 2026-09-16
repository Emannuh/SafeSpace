"""
SafeSpace safety service (Day 5).

Wraps the existing deterministic RiskRule engine for use in the AI pipeline.
Deterministic safety classification always runs BEFORE the AI step.
The AI layer CANNOT downgrade a safety classification.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.models import RiskRule

# Risk severity ordering — higher = more severe
_SEVERITY: dict[str, int] = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "IMMEDIATE": 4,
}


@dataclass
class SafetyResult:
    risk_level: str   # LOW | MEDIUM | HIGH | IMMEDIATE
    action: str       # NORMAL_FLOW | SHOW_SUPPORT | SHOW_HIGH_RISK_SUPPORT | SHOW_IMMEDIATE_SAFETY
    matched_rule: str | None

    @property
    def blocks_ai_answering(self) -> bool:
        """IMMEDIATE risk bypasses the normal AI explanation flow."""
        return self.risk_level == "IMMEDIATE"

    @property
    def severity(self) -> int:
        return _SEVERITY.get(self.risk_level, 0)


_DEFAULT = SafetyResult(risk_level="LOW", action="NORMAL_FLOW", matched_rule=None)


def classify_safety(message: str) -> SafetyResult:
    """
    Run all active RiskRules against the message (case-insensitive).

    Returns the most severe matching result, or the LOW default.
    This result is FINAL — the AI layer must not alter it.
    """
    if not message or not message.strip():
        return _DEFAULT

    active_rules = RiskRule.objects.filter(active=True).order_by("-priority", "name")

    best: SafetyResult = _DEFAULT
    for rule in active_rules:
        if rule.matches(message):
            candidate = SafetyResult(
                risk_level=rule.risk_level,
                action=rule.action,
                matched_rule=rule.name,
            )
            if candidate.severity > best.severity:
                best = candidate

    return best
