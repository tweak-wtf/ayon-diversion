from ayon_server.settings import (
    BaseSettingsModel,
    SettingsField,
)

from ayon_server.settings.enum import secrets_enum


class DiversionSettings(BaseSettingsModel):
    """Nuke addon settings."""

    enabled: bool = SettingsField(
        default=False,
        title="Enabled",
    )

    api_key: str = SettingsField(
        default="",
        enum_resolver=secrets_enum,
        title="API Key",
    )


DEFAULT_VALUES = {}
