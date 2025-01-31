import os

from ayon_applications import (
    PreLaunchHook,
    LaunchTypes,
)

from ayon_core.addon import AddonsManager
from ayon_core.tools.utils import qt_app_context


class DiversionPreLaunchHook(PreLaunchHook):
    """Handle workspace reset to commit on remote render jobs."""

    hosts = {"unreal"}
    launch_types = {}
    launch_types = {
        LaunchTypes.local,
        LaunchTypes.remote,
        LaunchTypes.farm_publish,
        LaunchTypes.automated,
    }

    def execute(self):
        if i_publish_job := os.environ.get("AYON_PUBLISH_JOB"):
            if i_publish_job > 0:
                return
        print(f"{self.data = }")
        print(f"{self.launch_context.launch_type = }")

    def reset_to_commit(self, repo: str, branch: str, commit: str):
        pass
