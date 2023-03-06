"""verify release branch project configuration

Usage:
    verify_branch_config.py (--project PROJECT) [--verbose]

Options:
    --project PROJECT    Project id created in Evergreen
    --verbose            Debug level for the logger
"""
import os
import logging
from logging import StreamHandler
import re
from typing import Dict, Any
from docopt import docopt
from evergreen.api import EvergreenApi, EvgAuth
from evergreen import Project


logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(logging.INFO)


def _verify_branch_config(arguments: Dict[str, Any]):
    is_valid_branch_config = True
    project = arguments["--project"] if "--project" in arguments else arguments["-p"]
    logger.info({
        "message": "Verifying release branch project",
        "project": project
    })

    evergreen_user = os.getenv("EVERGREEN_USER")
    evergreen_password = os.getenv("EVERGREEN_PASSWORD")

    evergreen_api = EvergreenApi.get_api(EvgAuth(evergreen_user, evergreen_password))
    logger.debug({
        "message": "Created Evergreen client",
        "evergreen_api": evergreen_api,
    })

    evg_project: Project = evergreen_api.project_by_id(project)
    evg_project_json = evg_project.json
    logger.debug({
        "message": "Found evergreen project",
        "project": project,
        "evergreen_project": evg_project_json
    })

    branch_pattern = r'v(202(\d{1})(\d{2})(\d{2}))'
    matched_branch = re.search(branch_pattern, evg_project.branch_name)
    if not matched_branch:
        is_valid_branch_config = False
        logger.error({
            "message": "Branch name doesn't match valid pattern",
            "valid_pattern": "v20YYMMDD",
            "project": project,
            "branch_name": evg_project.branch_name
        })

    is_pr_testing_enabled = evg_project_json.get("pr_testing_enabled", False)
    if not is_pr_testing_enabled:
        is_valid_branch_config = False
        logger.error({
            "message": "Automatic PR testing is not enabled",
            "project": project,
            "branch_name": evg_project.branch_name,
            "pr_testing_enabled": is_pr_testing_enabled
        })

    evg_project_variables = {}
    if "variables" in evg_project_json and "vars" in evg_project.json["variables"]:
        evg_project_variables = evg_project.json["variables"]["vars"]
    logger.debug({
        "message": "Evergreen project variables",
        "project": project,
        "variables": evg_project_variables
    })

    cloud_qa_url = "https://cloud-qa.mongodb.com"
    e2e_url = evg_project_variables.get("e2e_url", None)
    if e2e_url != cloud_qa_url:
        is_valid_branch_config = False
        logger.error({
            "message": "e2e_url variable doesn't point to cloud-qa environment",
            "project": project,
            "branch_name": evg_project.branch_name,
            "e2e_url": e2e_url
        })

    if is_valid_branch_config:
        logger.info({
            "message": "The config on the release branch are valid",
            "project": project
        })
    else:
        logger.warning({
            "message": "The config on the release branch are INVALID",
            "project": project
        })


if __name__ == "__main__":
    logger.info({
        "message": "Attempting to verify release branch config"
    })

    args: Dict[str, Any] = docopt(__doc__)
    if args["--verbose"]:
        logger.setLevel(logging.DEBUG)

    logger.info({
        "message": "release branch to be verified",
        "arguments": args
    })
    _verify_branch_config(args)