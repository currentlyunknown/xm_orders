from admin_tools.dashboard import Dashboard as AdminToolsDashboard
from admin_tools.dashboard import modules
from admin_tools.utils import get_admin_site_name
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

waffle_module = modules.ModelList("Waffle feature toggler", models=["waffle.*"])

redirects_module = modules.ModelList(
    "Redirects module", models=["django.contrib.redirects.*"]
)


class DashboardBase(AdminToolsDashboard):
    def add_perm_mods(self, mods):
        # Most modules disappear by themselves if no permissions exist,
        # but we still want to limit some further.
        self.children.extend([m for m, b in mods if b])


class Dashboard(DashboardBase):
    """
    Custom index dashboard for main XM Orders admins.
    """

    title = "XM Orders Site Admin"

    def init_with_context(self, context):
        super(Dashboard, self).init_with_context(context)
        request = context["request"]
        site_name = get_admin_site_name(context)

        accounts_module = modules.ModelList(
            "Accounts",
            models=[
                "accounts.models.CustomUser",
                "django.contrib.auth.models.Group",
            ],
        )

        # CMS module appears for some reason even if user has no permission:
        is_admin = request.user.is_superuser

        self.children.append(
            modules.LinkList(
                "Welcome!",
                layout="inline",
                draggable=True,
                deletable=False,
                collapsible=True,
                pre_content=("Welcome to the XM Orders main admin dashboard"),
                children=[
                    ("Return to site", "/"),
                    ("Change password", reverse(f"{site_name}:password_change")),
                    ("Log out", reverse(f"{site_name}:logout")),
                ],
            )
        )

        self.add_perm_mods(
            [
                (accounts_module, True),
                (
                    modules.RecentActions(_("Recent Actions"), 5),
                    True,
                ),
                (waffle_module, is_admin),
                (redirects_module, is_admin),
            ]
        )
