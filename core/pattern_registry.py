# Pattern registry system

pattern_registry = []

def register_pattern(func):
    """
    Register a pattern detector
    """
    pattern_registry.append(func)
    return func


def get_patterns():
    """
    Return all registered patterns
    """
    return pattern_registry