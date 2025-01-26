from qtpy import uic
from qtpy import QtCore, QtWidgets

from ayon_core.tools.utils import ErrorMessageBox

from ayon_diversion.api import DV_Workspace
from ayon_diversion.addon import DIVERSION_ROOT_DIR


class UncommittedChangesRepairer(ErrorMessageBox):
    def __init__(self, workspace: DV_Workspace):
        self.title = "Uncommitted Changes"
        self.parent = QtWidgets.QApplication.activeWindow()
        self.workspace = workspace
        super().__init__(self.title, self.parent)

    def _create_content(self, content_layout) -> None:
        msg = """
You have pending files in your changelist.
Please revert or commit your changes before publishing again.

You can use the below tool or any other method provided by Diversion to do so.
"""
        label = QtWidgets.QLabel(msg)
        content_layout.addWidget(label)

        ui_file = (
            DIVERSION_ROOT_DIR / "ui_tools" / "resources" / "uncommitted_changes.ui"
        ).resolve()
        new_widget = uic.loadUi(ui_file.as_posix(), QtWidgets.QWidget())

        if added_files := self.workspace.uncommitted_changes["added"]:
            for added_file in added_files:
                new_widget.vl_added.addWidget(QtWidgets.QLabel(added_file))
        else:
            new_widget.wdg_added.hide()

        if modified_files := self.workspace.uncommitted_changes["modified"]:
            for modified_file in modified_files:
                new_widget.vl_modified.addWidget(QtWidgets.QLabel(modified_file))
        else:
            new_widget.wdg_modified.hide()

        if deleted_files := self.workspace.uncommitted_changes["deleted"]:
            for deleted_file in deleted_files:
                new_widget.vl_deleted.addWidget(QtWidgets.QLabel(deleted_file))
        else:
            new_widget.wdg_deleted.hide()

        commit_msg = "[AYON PRE PUBLISH] I'm a user message"
        new_widget.btn_commit.clicked.connect(
            lambda _, msg=commit_msg: self.workspace.commit_changes(msg)
        )
        new_widget.btn_reset.clicked.connect(self.workspace.reset_changes)

        content_layout.addWidget(new_widget)
