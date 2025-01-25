import pyblish.api

from ayon_diversion.api import DV_Workspace


class ValidateDiversionWorkspace(pyblish.api.InstancePlugin):
    """Get Workspace from Current Unreal Project Path."""

    order = pyblish.api.ValidatorOrder
    label = "Validate Diversion Workspace"
    hosts = ["unreal"]
    families = ["dv_workspace"]

    def process(self, instance):
        ws: DV_Workspace = instance.data.get("diversion_workspace")
        if ws.has_uncommitted_changes:
            # TODO: repair action
            self.log.error(ws.status)
            raise ValueError("Workspace has uncommitted changes")
