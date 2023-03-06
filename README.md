# Skunkwork 2023

## Verify Evergreen Config of Release Branch

The bullet point 4 at [Creating A Release Branch And Deploying To QA
](https://wiki.corp.mongodb.com/display/MMS/Cloud+Release+Management#CloudReleaseManagement-CloudDeveloperProductivityAssignments) asks us to valiadate 
a few config items. 
This utility helps to validate configs.

- Source code: verify_branch_cut_config
- run 
  - debug mode: `python3 <path>/skunkweek2023/verify_branch_cut_config/verify_branch_config.py --project mms-v20230301 --verbose
  `
  - normal mode: `python3 <path>/skunkweek2023/verify_branch_cut_config/verify_branch_config.py --project mms-v20230301`


