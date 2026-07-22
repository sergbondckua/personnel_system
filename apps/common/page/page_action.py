from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PageAction:
    """
    Дія сторінки.
    """

    title: str

    url: str

    icon: str | None = None

    style: str = "outline-secondary"
