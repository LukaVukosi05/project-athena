"""Adapters for authored assessment modules."""


def module_bank(module):
    """Keep all five components together when registering a lesson."""
    return (
        module.PRACTICE_BANK,
        module.MASTERY_BANK,
        module.REASSESSMENT_BANK,
        module.MISCONCEPTION_REPAIRS,
        module.REPAIR_RULES,
    )
