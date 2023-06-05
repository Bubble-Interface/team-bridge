import logging
import os
import json

from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler

from flask import Flask, request

from db.db_interaction import (
    save_acronym,
    get_acronym_description,
    list_acronyms
)

# TODO: change from acronyms to terms or smth similar
# TODO: add missing knowledge actions (submit/request)
# TODO: add shortcut (create knowledge from the message)
# TODO: monitor conversations and reply in thread with term explanation

basedir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = App(logger=logger)
handler = SlackRequestHandler(app)


@app.event("app_home_opened")
def handle_command(say):
    say("Hey there!")

@app.view("add_acronym_view")
def handle_submission(ack, body, client, view, logger, say):
    # TODO: send private message to everyone in the chat
    # about additional info request for that knowledge
    
    acronym = view["state"]["values"]["acronym"]["title"]
    acronym = acronym.get("value")
    acronym_description = view["state"]["values"]["description_input"]["description"]
    acronym_description = acronym_description.get("value")
    user = body["user"]["id"]
    # Validate the inputs
    errors = {}
    if acronym is None:
        errors["acronym"] = "Please enter an acronym"
    if acronym_description is None:
        errors["description_input"] = "Please enter an acronym description"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    # Acknowledge the view_submission request and close the modal
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission

    # Message to send user
    msg = ""
    try:
        # Save to DB
        save_acronym(acronym=acronym, description=acronym_description)
        msg = f"Your submission of {acronym} was successful"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    try:
        say(channel=user, text=msg)
    except SlackApiError as e:
        logger.exception(f"Failed to post a message {e}")


# TODO: notify in the app members of the channel
@app.command("/remember")
def open_modal(ack, body, client):
    # Acknowledge the command request
    ack()
    with open("templates/add_knowledge.json") as add_knowledge_template:
        add_knowledge_view = json.load(add_knowledge_template)
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=add_knowledge_view
    )


@app.command("/what")
def what_command(ack, respond, command):
    ack()
    text = command['text'].split()
    acronym = text[0]
    acronym_description = get_acronym_description(acronym=acronym)
    respond(acronym_description)

# TODO: list as bullet points: acronym: description
@app.command("/list")
def list_command(ack, respond, command):
    ack()
    acronym_list = list_acronyms()
    acronyms = '; '.join(acronym_list)
    respond(f"List of saved acronyms: {acronyms}")

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


if __name__ == "__main__":
    flask_app.run(debug=True, port=3000)


# pip install -r requirements.txt

# # -- OAuth flow -- #
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,chat:write

# FLASK_APP=oauth_app.py FLASK_ENV=development flask run -p 3000
