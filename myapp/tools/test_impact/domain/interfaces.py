"""
Sistemin abstraksiya layeri.
Hər modul bu interface-lərə qarşı yazılır — implementation-a deyil.
Sonra JSON store-u SQLite ilə, ya coverage collector-u başqası ilə əvəz etmək üçün
yalnız bu interface-i implement edən yeni sinif yazmaq kifayətdir.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from .models import (
    ChangedFile,
    ExecutionPlan,
    ExecutionResult,
    ImpactSelectionResult,
    RuntimeTrace,
    TestCase,
)


# ---------------------------------------------------------------------------
# 1. MƏLUMAT TOPLAMA (Collectors)
# ---------------------------------------------------------------------------

class TestCatalogProvider(ABC):
    """
    Proyektdəki bütün test case-ləri tapır.
    Default implementation: pytest --collect-only ilə işləyir.
    """

    @abstractmethod
    def collect(self, root: str) -> list[TestCase]:
        """
        Verilmiş qovluqdan bütün test case-ləri toplayır.

        Args:
            root: Test axtarışının başladığı qovluq yolu.

        Returns:
            Tapılan bütün TestCase-lərin siyahısı.
        """
        ...


class TraceProvider(ABC):
    """
    Hər test üçün runtime əhatə izini toplayır.
    Default implementation: pytest-cov / coverage.py ilə işləyir.
    """

    @abstractmethod
    def collect(self, test: TestCase) -> RuntimeTrace:
        """
        Bir test case-i işə salıb onun əhatə izini qaytarır.

        Args:
            test: İzi toplanacaq test case.

        Returns:
            Test-in icra etdiyi bütün fayl+sətir nöqtələri.
        """
        ...

    @abstractmethod
    def collect_all(self, tests: list[TestCase]) -> list[RuntimeTrace]:
        """
        Bir neçə test üçün eyni anda iz toplayır.

        Args:
            tests: İzi toplanacaq test case-lərin siyahısı.

        Returns:
            Hər test üçün bir RuntimeTrace.
        """
        ...


class DiffProvider(ABC):
    """
    VCS-dən (Git) dəyişiklik məlumatını oxuyur.
    Default implementation: git diff ilə işləyir.
    """

    @abstractmethod
    def get_changed_files(self, base: str, head: str = "HEAD") -> list[ChangedFile]:
        """
        İki commit/branch arasındakı dəyişmiş faylları qaytarır.

        Args:
            base: Müqayisə bazası (branch adı və ya commit SHA).
            head: Müqayisə hədəfi. Default: HEAD.

        Returns:
            Dəyişmiş faylların siyahısı.
        """
        ...


class DependencyProvider(ABC):
    """
    Proyektdəki modul asılılıq qrafını qurur.
    V2 üçün — static import analizi əsasında.
    """

    @abstractmethod
    def get_dependents(self, file_path: str) -> list[str]:
        """
        Verilmiş faylı import edən bütün faylları qaytarır.

        Args:
            file_path: Asılılıqları axtarılacaq faylın yolu.

        Returns:
            Bu faylı birbaşa import edən faylların yolları.
        """
        ...

    @abstractmethod
    def get_transitive_dependents(self, file_path: str) -> list[str]:
        """
        Verilmiş faylı dolayı yolla import edən bütün faylları qaytarır.

        Args:
            file_path: Asılılıqları axtarılacaq faylın yolu.

        Returns:
            Bu faylı birbaşa və ya dolayı import edən bütün faylların yolları.
        """
        ...


# ---------------------------------------------------------------------------
# 2. SAXLAMA (Storage)
# ---------------------------------------------------------------------------

class ArtifactStore(ABC):
    """
    TIA engine-in artifact-larını (inventory, coverage map, report) saxlayır və oxuyur.
    Default implementation: JSON faylları ilə işləyir (storage/json_store.py).
    Alternativ: SQLite, Redis, və s.
    """

    @abstractmethod
    def save_inventory(self, tests: list[TestCase]) -> None:
        """Test inventarını saxlayır."""
        ...

    @abstractmethod
    def load_inventory(self) -> list[TestCase]:
        """Saxlanmış test inventarını oxuyur."""
        ...

    @abstractmethod
    def save_traces(self, traces: list[RuntimeTrace]) -> None:
        """Runtime əhatə izlərini saxlayır."""
        ...

    @abstractmethod
    def load_traces(self) -> list[RuntimeTrace]:
        """Saxlanmış əhatə izlərini oxuyur."""
        ...

    @abstractmethod
    def save_report(self, results: list[ExecutionResult]) -> None:
        """İcra nəticələri hesabatını saxlayır."""
        ...

    @abstractmethod
    def load_report(self) -> list[ExecutionResult]:
        """Saxlanmış hesabatı oxuyur."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Bütün artifact-ları silir."""
        ...


# ---------------------------------------------------------------------------
# 3. SEÇİM VƏ PLANLAŞDIRMA (Selection & Planning)
# ---------------------------------------------------------------------------

class SelectionStrategy(ABC):
    """
    Dəyişikliklərdən təsirlənən testləri seçir.
    Default implementation: coverage map əsasında (selection/engine.py).
    Alternativ: LLM-based, heuristic-only, və s.
    """

    @abstractmethod
    def select(
        self,
        changed_files: list[ChangedFile],
        traces: list[RuntimeTrace],
        all_tests: list[TestCase],
    ) -> list[ImpactSelectionResult]:
        """
        Dəyişmiş fayllara görə təsirlənən testləri seçir.

        Args:
            changed_files: VCS-dən alınan dəyişmiş faylların siyahısı.
            traces:         Hər test üçün runtime əhatə izləri.
            all_tests:      Proyektdəki bütün test case-lər.

        Returns:
            Seçilmiş testlər və seçim əsaslandırmaları.
        """
        ...

class ExecutionPlanner(ABC):
    """
    Seçilmiş testlərdən icra planı qurur.
    Prioritetləşdirmə, batching, paralel icra qərarları burada verilir.
    """

    @abstractmethod
    def build_plan(
        self,
        selected: list[ImpactSelectionResult],
        changed_files: list[ChangedFile],
    ) -> ExecutionPlan:
        """
        Seçilmiş testlərdən icra planı qurur.

        Args:
            selected:      Seçilmiş testlər və əsaslandırmaları.
            changed_files: Planın hazırlandığı dəyişiklik konteksti.

        Returns:
            İcraya hazır ExecutionPlan.
        """
        ...