from apps.dashboard.navigation import SIDEBAR


def navigation(request):
    return {
        "sidebar": SIDEBAR,
    }
