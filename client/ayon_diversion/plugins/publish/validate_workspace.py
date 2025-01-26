import pyblish.api

from ayon_core.pipeline.publish import RepairAction, PublishValidationError

from ayon_diversion.api import DV_Workspace
from ayon_diversion.ui_tools.repair_actions import UncommittedChangesRepairer


class ValidateDiversionWorkspace(pyblish.api.InstancePlugin):
    """Get Workspace from Current Unreal Project Path."""

    order = pyblish.api.ValidatorOrder
    label = "Validate Diversion Workspace"
    hosts = ["unreal"]
    families = ["dv_workspace"]
    actions = [RepairAction]

    def process(self, instance):
        ws: DV_Workspace = instance.data.get("diversion_workspace")
        if ws.has_uncommitted_changes:
            self.log.error(ws.uncommitted_changes)
            raise PublishValidationError("Workspace has uncommitted changes")

    @classmethod
    def repair(cls, instance):
        UncommittedChangesRepairer(
            workspace=instance.data["diversion_workspace"],
        ).exec_()
