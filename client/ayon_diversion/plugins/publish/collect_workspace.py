from pathlib import Path

import pyblish.api

from ayon_diversion.api import DV_Workspace


class CollectDiversionWorkspace(pyblish.api.InstancePlugin):
    """Get Workspace from Current Unreal Project Path."""

    order = pyblish.api.CollectorOrder
    label = "Collect Diversion Workspace"
    hosts = ["unreal"]
    families = ["dv_workspace"]

    def process(self, instance):
        ue_project_root = Path(instance.context.data["currentFile"]).parent
        ws = DV_Workspace(ue_project_root)
        instance.data["diversion_workspace"] = ws
        self.log.info(ws.status)
