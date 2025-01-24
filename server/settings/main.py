from ayon_server.settings import (
    BaseSettingsModel,
    SettingsField,
)


class DiversionSettings(BaseSettingsModel):
    """Nuke addon settings."""

    enabled: bool = SettingsField(
        default=False,
        title="Enabled",
    )


DEFAULT_VALUES = {}
