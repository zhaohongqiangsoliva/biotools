import contextlib
from contextlib import nullcontext
import os,sys,time
import requests
from pathlib import Path


def open_or_zip(path) :
    """Return a context that may be used for reading the contents from the path.

    If path is a directory returns the contents as an in memory zip file.
    """

    if not path:
        return nullcontext()

    path = Path(path)
    if path.is_dir():
        return zip_dir(path)
    else:
        return path.open("rb")


def submit_workflow_to_server(
        url,
            wdl: str,
            wdl_json: str,
            options_json: str,
            dependencies_zip: str,

    http_utils=None) :
        """Submits workflow and related files to cromwell server"""

        none_context = contextlib.nullcontext()
        # Give to file handler if file is None
        # "With" below will open multiple files, since the options_json and dependencies_zip
        # files are optional the "with" statement has conditionals that opens the files
        # only if they are not NONE. To do this none_context is used to pass to the file
        # handler, which avoids errors if optional files are NONE.
        with open(wdl, "rb") as wdl_file ,open_or_zip(dependencies_zip) as dependencies_file:
            submission_params = {
                "workflowSource": wdl_file,
                "workflowInputs": wdl_json,
            }
            if options_json is not None:
                submission_params["workflowOptions"] = options_json
            if dependencies_zip is not None:
               submission_params["workflowDependencies"] = dependencies_file

            requests_out = requests.post(
                url,
                files=submission_params,
                timeout=5,
                verify=False
            )
            return (requests_out.text)


if __name__ == '__main__':

    submit_workflow_to_server(
                        "http://192.168.77.45:8088/api/workflows/v1"
                            "/disk/project/imputation/warp19/Imputation_v1.1.10.zip",
                          "/disk/project/imputation/warp19/input_2.json",
                          "/disk/project/imputation/warp19/options.json",
                          "/disk/project/imputation/warp19/Imputation_v1.1.10.zip")