from pathlib import Path
from ayon_core.addon import AYONAddon

from .version import __version__

DIVERSION_ROOT_DIR = Path(__file__).parent.resolve()


class DiversionAddon(AYONAddon):
    name = "diversion"
    version = __version__
    host_name = "diversion"
