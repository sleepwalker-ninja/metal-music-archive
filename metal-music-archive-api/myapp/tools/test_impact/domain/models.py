""" Sistemin “dilini” müəyyən edir. Bütün modullar eyni model-lərlə danışmalıdır """

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime

from .enums import (
    TestLayer,
    ChangeType,
    ReasonType,
    ConfidenceLevel,
    ExecutionMode
)

# ---------------------------------------------------------
# 1. KOD DƏYİŞİKLİYİ MODELLƏRİ (VCS / Git səviyyəsi)
# ---------------------------------------------------------

class ChangedHunk(BaseModel):
    """Fayl daxilindəki konkret dəyişmiş sətirlər bloku."""
    start_line: int = Field(..., description="Dəyişiklik blokunun başladığı sətir nömrəsi")
    end_line: int = Field(..., description="Dəyişiklik blokunun bitdiyi sətir nömrəsi")
    contetnt: str = Field(..., description="Dəyişmiş sətirlər bloku (opsional)")


class ChangedFile(BaseModel):
    """Dəyişmiş fayl haqqında məlumat."""
    file_path: str = Field(..., description="Dəyişmiş faylın yolu")
    change_type: ChangeType
    hunks: List[ChangedHunk] = Field(default_factory=list, description="Fayl daxilindəki dəyişiklik blokları")


# ---------------------------------------------------------
# 2. TEST VƏ TRACE MODELLƏRİ (Analiz səviyyəsi)
# ---------------------------------------------------------

class TestCase(BaseModel):
    """Sistemdəki bir ədəd testin tərifi."""
    # Model config: obyektin dəyərlərini sonradan dəyişməyə icazə vermir (Immutable edir)
    model_config = ConfigDict(frozen=True)
    