from pathlib import Path
from ayon_core.addon import AYONAddon, IPluginPaths

from .version import __version__

DIVERSION_ROOT_DIR = Path(__file__).parent.resolve()


class DiversionAddon(AYONAddon, IPluginPaths):
    name = "diversion"
    version = __version__
    host_name = "diversion"

    def initialize(self, studio_settings):
        pass

    def get_plugin_paths(self):
        return {}

    def get_create_plugin_paths(self, host_name):
        create_path = (DIVERSION_ROOT_DIR / "plugins" / "create").as_posix()
        return [create_path]

    def get_publish_plugin_paths(self, host_name):
        self.log.debug(f"{host_name = }")
        publish_path = (DIVERSION_ROOT_DIR / "plugins" / "publish").as_posix()
        return [publish_path]

    def get_launch_hook_paths(self, host_name):
        hooks_path = (DIVERSION_ROOT_DIR / "hooks").as_posix()
        return [hooks_path]
