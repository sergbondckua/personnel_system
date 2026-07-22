from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apps.common.page import PageAction


@dataclass(slots=True)
class PageContext:
    """
    Контекст сторінки.
    """

    title: str
    subtitle: str | None = None
    actions: list[PageAction] = field(default_factory=list)
    navigation: Any | None = None
    filter_form: Any | None = None
