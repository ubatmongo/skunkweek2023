"""verify release branch project configuration

Usage:
    thread_unroller.py (--thread THREAD_URL) [--pdf] [--verbose]

Options:
    --thread THREAD_URL    Project id created in Evergreen
    --pdf                  Content will be saved as a PDF
    --verbose              Debug level for the logger
"""


import os
import pathlib
import logging
from logging import StreamHandler

from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined, CatchAll

from typing import List, Dict, Any
from docopt import docopt

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

from reportlab.lib.colors import blue
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfgen.canvas import Canvas


logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(logging.INFO)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(init=True, repr=True, eq=True)
class SlackMessage:
    type: str
    text: str
    user: str
    ts: str
    user: str
    thread_ts: str


def _unroll(arguments: Dict[str, Any]):
    thread_url: str = arguments["--thread"]
    is_pdf: bool = arguments["--pdf"]
    logger.info({
        "message": "Going to unroll a Slack thread",
        "thread": thread_url,
        "is_pdf": is_pdf
    })

    splitted_url = thread_url.split("/")
    slack_channel_id: str = splitted_url[-2]
    thread_ts: str = splitted_url[-1][1:]
    thread_ts = "{}.{}".format(thread_ts[0:len(thread_ts)-6], thread_ts[len(thread_ts)-6:])

    logger.debug({
        "message": "Slack conversation details",
        "channel_id": slack_channel_id,
        "thread_timestamp": thread_ts
    })

    slack_auth_token = os.getenv("SLACK_AUTH_TOKEN")
    slack_web_client = WebClient(token=slack_auth_token)

    thread_details: SlackResponse = slack_web_client.conversations_replies(
        channel=slack_channel_id,
        ts=thread_ts,
        include_all_metadata=True,
        inclusive=True
    )

    if thread_details.status_code >= 400:
        logger.error({
            "message": "Failed to fetch the thread from Slack",
        })
        return

    slack_messages = thread_details.get("messages")
    users_map: Dict[str, Any] = {}
    message_list: List[SlackMessage] = []

    for message in slack_messages:
        logger.debug({
            "message": "Message received from Slack",
            "user_message": message
        })
        new_message: SlackMessage = SlackMessage.from_dict(message)
        if new_message.user and new_message.user not in users_map:
            new_user: SlackResponse = slack_web_client.users_profile_get(user=new_message.user)
            users_map[new_message.user] = new_user.get("profile")

        message_list.append(new_message)

    out_file_path: str = "{}/{}".format(pathlib.Path.home(), "Desktop")
    out_file_name: str = thread_ts
    if is_pdf:
        out_file: Canvas = Canvas(f"{out_file_path}/{out_file_name}.pdf", pagesize=A4)
        width, height = A4

        paragraph_style = ParagraphStyle(
            name='Normal',
            fontName='Times-Roman',
            fontSize=12,
            backColor='#F1F1F1',
            borderColor='#00000F',
            borderWidth=1,
            borderPadding=(10, 10, 10, 10),
            leading=10,
            alignment=0
        )

        paragraphs: List[Paragraph] = []
        for idx, message in enumerate(message_list):
            formatted_message = f"""
            <b>{users_map[message.user]["real_name"]}</b>:
            <p>{message.text}</p>
            """
            # paragraphs.append(Paragraph(formatted_message, style = paragraph_style))
            # out_file.build(Paragraph(formatted_message, style = paragraph_style))
            paragraph = Paragraph(formatted_message, style=paragraph_style)
            pwidth, pheight = paragraph.wrapOn(out_file, width - 10, 100)
            logger.debug({
                "message": "Height and width of the paragraph",
                "p-width": pwidth,
                "p-height": pheight
            })
            paragraph.drawOn(out_file, width - 450, height - (pheight + 50) * (idx + 1))

        out_file.save()

    else:
        with open(f"{out_file_path}/{out_file_name}.txt", "w") as out_file:
            for message in message_list:
                out_file.write(f"{users_map[message.user]['real_name']}:\n")
                out_file.write(f"{message.text}\n\n")


if __name__ == "__main__":
    logger.info({
        "message": "Unrolling a Slack thread"
    })

    args: Dict[str, Any] = docopt(__doc__)
    if args["--verbose"]:
        logger.setLevel(logging.DEBUG)

    _unroll(args)
