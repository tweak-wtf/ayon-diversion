import json
import tempfile
from pathlib import Path

from ayon_core.pipeline import publish


class ExtractDiversionWorkspace(publish.Extractor):
    """Store workspace info into a json file to be integrated later."""

    order = publish.Extractor.order
    label = "Extract Diversion Workspace"
    families = ["dv_workspace"]
    targets = ["local"]

    def process(self, instance):
        ws = instance.data.get("diversion_workspace")
        if not ws:
            raise ValueError("No workspace found in instance data.")

        ws_data = {
            "name": ws.name,
            "ref_id": ws.ref_id,
            "repo_name": ws.repo_name,
            "repo_ref_id": ws.repo_ref_id,
            "branch_name": ws.branch_name,
            "branch_ref_id": ws.branch_ref_id,
            "commit": ws.commit,
        }

        file_name = f"{ws.name}.json"
        staging_dir = Path(tempfile.mkdtemp())
        ws_data_path = staging_dir / file_name
        with open(ws_data_path, "w") as fp:
            json.dump(ws_data, fp)

        repre_data = {
            "name": "dv_workspace",
            "ext": "json",
            "files": file_name,
            "stagingDir": staging_dir,
        }

        instance.data["representations"].append(repre_data)
