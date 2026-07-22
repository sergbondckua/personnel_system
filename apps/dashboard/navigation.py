from dataclasses import dataclass, field


@dataclass(slots=True)
class MenuItem:
    title: str
    icon: str
    url: str | None = None
    children: list["MenuItem"] = field(default_factory=list)


SIDEBAR = [
    MenuItem(
        title="Головна",
        icon="🏠",
        url="dashboard:index",
    ),
    # MenuItem(
    #     title="Особовий склад",
    #     icon="👤",
    #     children=[
    #         MenuItem(
    #             title="Військовослужбовці",
    #             icon="",
    #             url="personnel:list",
    #         ),
    #         MenuItem(
    #             title="Призначення",
    #             icon="",
    #             url="assignments:list",
    #         ),
    #     ],
    # ),
    # MenuItem(
    #     title="Організація",
    #     icon="🏢",
    #     children=[
    #         MenuItem(
    #             title="Організації",
    #             icon="",
    #             url="organization:organizations",
    #         ),
    #         MenuItem(
    #             title="Підрозділи",
    #             icon="",
    #             url="organization:units",
    #         ),
    #         MenuItem(
    #             title="Штатні посади",
    #             icon="",
    #             url="organization:staff",
    #         ),
    #     ],
    # ),
    MenuItem(
        title="Відпустки",
        icon="📅",
        children=[
            # MenuItem(
            #     title="Список",
            #     icon="",
            #     url="vacations:list",
            # ),
            MenuItem(
                title="Графік",
                icon="",
                url="vacations:schedule",
            ),
        ],
    ),
    # MenuItem(
    #     title="Довідники",
    #     icon="📖",
    #     url="references:index",
    # ),
]
