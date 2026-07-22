from __future__ import annotations

from dataclasses import dataclass, field

from apps.organization.models import OrgUnit
from apps.organization.tree_person import OrgTreePerson


@dataclass(slots=True)
class OrgTreeNode:
    """
    Вузол дерева організаційної структури.
    """

    unit: OrgUnit

    level: int = 0

    people: list[OrgTreePerson] = field(default_factory=list)

    children: list["OrgTreeNode"] = field(default_factory=list)