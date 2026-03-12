"""Sistemdə string chaos yaranmasın, sabit terminologiya olsun"""

from enum import Enum


class TestLayer(Enum):
    """Test layerlərini təmsil edən enum."""
    UNIT = "unit"
    INTEGRATION = "integration"
    API = "api"


class ChangeType(Enum):
    """Dəyişmiş faylın növünü bildirir."""
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    RENAMED = "renamed"


class SelectionReason(Enum):
    """Testin niyə seçildiyini bildirir."""
    DIRECT_COVERAGE = "direct_coverage"
    """Dəyişən sətir birbaşa bu test tərəfindən əhatə olunur."""

    INDIRECT_COVERAGE = "indirect_coverage"
    """Dəyişən sətir dolayı yolla (import/çağırış zənciri) əhatə olunur."""

    HEURISTIC = "heuristic"
    """Əhatə məlumatı yoxdur; evristik qaydaya görə seçilib."""

    ALWAYS_RUN = "always_run"
    """Hər zaman işlədilməli olan test (məs. smoke, conftest dəyişikliyi)."""


class ExecutionStatus(Enum):
    """Bir testin icra nəticəsi."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"