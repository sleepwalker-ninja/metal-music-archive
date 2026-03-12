"""Sistemdə string chaos yaranmasın, sabit terminologiya olsun"""

from enum import Enum

class TestLayer(Enum):
    """Test layerlərini təmsil edən enum"""
    UNIT = "unit"
    INTEGRATION = "integration"
    API = "api"


class ChangeType(Enum):
    """Sistemdəki dəyişiklik növlərini təmsil edən enum."""
    ADDITION = "addition"
    DELETION = "deletion"
    MODIFICATION = "modification"


class ReasonType(Enum):
    """Dəyişiklik və əməliyyatın arxasındakı əsas səbəbi bildirir"""
    BUG_FIX = "bug_fix"
    FEATURE_ADDITION = "feature_addition"
    REFACTORING = "refactoring"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"

class ConfidenceLevel(Enum):
    """Sistemin və ya modelin qərarına inam dərəcəsini göstərir"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExecutionMode(Enum):
    """Testlərin icra rejimini təmsil edən enum"""
    AUTOMATIC = "automatic"
    MANUAL = "manual"