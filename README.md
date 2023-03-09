# Skunkwork 2023

## Verify Evergreen Config of Release Branch

The bullet point 4 at [Creating A Release Branch And Deploying To QA
](https://wiki.corp.mongodb.com/display/MMS/Cloud+Release+Management#CloudReleaseManagement-CloudDeveloperProductivityAssignments) asks us to valiadate 
a few config items. 
This utility helps to validate configs.

- Source code: _verify_branch_cut_config_
- run 
  - debug mode: `python3 <path>/verify_branch_cut_config/verify_branch_config.py --project mms-v20230301 --verbose
  `
  - normal mode: `python3 <path>/verify_branch_cut_config/verify_branch_config.py --project mms-v20230301`

## Unroll a Slack Thread

We often discuss stuff on Slack that should go in a PD/Scope/Spec document.
This tool will help us keep a copy of that.

- Source code: _slack_thread_unroll_
- run:
  - PDF: `python3 <path>/slack_thread_unroll/thread_unroller.py --thread https://mdb-sandboxenterprise.slack.com/archives/C04SUBZ2X27/p1678222095655119 --pdf --verbose 
  - txt: `python3 <path>/slack_thread_unroll/thread_unroller.py --thread https://mdb-sandboxenterprise.slack.com/archives/C04SUBZ2X27/p1678222095655119 

```json
{'message': 'Unrolling a Slack thread'}
{'message': 'Going to unroll a Slack thread', 'thread': 'https://mdb-sandboxenterprise.slack.com/archives/C04SUBZ2X27/p1678222095655119', 'is_pdf': False}
{'message': 'Slack conversation details', 'channel_id': 'C04SUBZ2X27', 'thread_timestamp': '1678222095.655119'}
{'message': 'Message received from Slack', 'user_message': {'client_msg_id': '4a496119-a879-4ebf-8da6-309051290dd4', 'type': 'message', 'text': 'This is a message', 'user': 'U04SD4ZLSJ3', 'ts': '1678222095.655119', 'blocks': [{'type': 'rich_text', 'block_id': 'eHb', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'This is a message'}]}]}], 'team': 'T01F60CPBRU', 'thread_ts': '1678222095.655119', 'reply_count': 4, 'reply_users_count': 1, 'latest_reply': '1678222179.277849', 'reply_users': ['U04SD4ZLSJ3'], 'is_locked': False, 'subscribed': False}}
{'message': 'Message received from Slack', 'user_message': {'client_msg_id': '6eb28f66-4e3e-4bcb-9f00-9abb70fcf2e6', 'type': 'message', 'text': 'message in the thread', 'user': 'U04SD4ZLSJ3', 'ts': '1678222105.245449', 'blocks': [{'type': 'rich_text', 'block_id': 'QQe', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'message in the thread'}]}]}], 'team': 'T01F60CPBRU', 'thread_ts': '1678222095.655119', 'parent_user_id': 'U04SD4ZLSJ3'}}
{'message': 'Message received from Slack', 'user_message': {'type': 'message', 'text': 'image and text', 'files': [{'id': 'F04SUFVM9RQ', 'created': 1678222116, 'timestamp': 1678222116, 'name': 'Screenshot 2023-02-28 at 5.10.46 PM.png', 'title': 'Screenshot 2023-02-28 at 5.10.46 PM.png', 'mimetype': 'image/png', 'filetype': 'png', 'pretty_type': 'PNG', 'user': 'U04SD4ZLSJ3', 'user_team': 'E01EJJR6SQ2', 'editable': False, 'size': 443503, 'mode': 'hosted', 'is_external': False, 'external_type': '', 'is_public': True, 'public_url_shared': False, 'display_as_bot': False, 'username': '', 'url_private': 'https://files.slack.com/files-pri/T01EJJR6SQ2-F04SUFVM9RQ/screenshot_2023-02-28_at_5.10.46_pm.png', 'url_private_download': 'https://files.slack.com/files-pri/T01EJJR6SQ2-F04SUFVM9RQ/download/screenshot_2023-02-28_at_5.10.46_pm.png', 'media_display_type': 'unknown', 'thumb_64': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_64.png', 'thumb_80': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_80.png', 'thumb_360': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_360.png', 'thumb_360_w': 360, 'thumb_360_h': 234, 'thumb_480': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_480.png', 'thumb_480_w': 480, 'thumb_480_h': 312, 'thumb_160': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_160.png', 'thumb_720': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_720.png', 'thumb_720_w': 720, 'thumb_720_h': 468, 'thumb_800': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_800.png', 'thumb_800_w': 800, 'thumb_800_h': 520, 'thumb_960': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_960.png', 'thumb_960_w': 960, 'thumb_960_h': 623, 'thumb_1024': 'https://files.slack.com/files-tmb/T01EJJR6SQ2-F04SUFVM9RQ-984203b64c/screenshot_2023-02-28_at_5.10.46_pm_1024.png', 'thumb_1024_w': 1024, 'thumb_1024_h': 665, 'original_w': 3024, 'original_h': 1964, 'thumb_tiny': 'AwAfADCP7E//ADxP6UfYpP8Angf0rVNLigDKWyYjmIj8KQ2Tg8REj14rWxRigDI+xv8A88T+lL9jf/ngfzFa2KMUANNOpMUtABRRRQAUUUUAf//Z', 'permalink': 'https://mongodb-sandbox.enterprise.slack.com/files/U04SD4ZLSJ3/F04SUFVM9RQ/screenshot_2023-02-28_at_5.10.46_pm.png', 'permalink_public': 'https://slack-files.com/T01EJJR6SQ2-F04SUFVM9RQ-acbb2282c1', 'is_starred': False, 'has_rich_preview': False, 'file_access': 'visible'}], 'upload': False, 'user': 'U04SD4ZLSJ3', 'display_as_bot': False, 'ts': '1678222123.809339', 'blocks': [{'type': 'rich_text', 'block_id': 'EjGR', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'image and text'}]}]}], 'client_msg_id': 'f83520d2-83c9-4f79-8561-0e1f018637ef', 'thread_ts': '1678222095.655119', 'parent_user_id': 'U04SD4ZLSJ3'}}
{'message': 'Message received from Slack', 'user_message': {'client_msg_id': 'ccbf4317-67c3-4bf9-a04d-af849884eb87', 'type': 'message', 'text': '```this is formatted stuff```', 'user': 'U04SD4ZLSJ3', 'ts': '1678222138.900689', 'blocks': [{'type': 'rich_text', 'block_id': '5GKV', 'elements': [{'type': 'rich_text_preformatted', 'elements': [{'type': 'text', 'text': 'this is formatted stuff'}], 'border': 0}]}], 'team': 'T01F60CPBRU', 'thread_ts': '1678222095.655119', 'parent_user_id': 'U04SD4ZLSJ3'}}
{'message': 'Message received from Slack', 'user_message': {'client_msg_id': '47bc4c44-ae49-47ee-8435-b9bab587066c', 'type': 'message', 'text': "if this doesn't work then....", 'user': 'U04SD4ZLSJ3', 'ts': '1678222179.277849', 'blocks': [{'type': 'rich_text', 'block_id': 'PZPM1', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': "if this doesn't work then...."}]}]}], 'team': 'T01F60CPBRU', 'thread_ts': '1678222095.655119', 'parent_user_id': 'U04SD4ZLSJ3'}}
```

## Compute time regression of tasks from Evergreen data

Looks over historic Evergreen data for tasks, grouped by (task, variant) over a specified 
period of time and reports if 
- max time has regressed more than 10% over min time
- any task has regressed more than 10% over min time

- Source code: _evergreen_task_regression_
- run:
  - `python3 <path>/evergreen_task_regression/task_regression.py --project mms --tasks COMPILE_BAZEL,COMPILE_CLIENT_BAZEL,COMPILE_SERVER --variants code_health --period 30 --weekly --verbose 
 
