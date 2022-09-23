from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from jira import JIRA


jira = JIRA(
    basic_auth=('<email>', '<token>'),
    server="https://<company>.atlassian.net"
)

app = Flask(__name__)
 
@app.route("/wa")
def wa_hello():
    return "Hello, World!"
 
@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    """Respond to incoming calls with a simple text message."""
    
    msg = request.form.get('Body').lower() # Reading the message from the whatsapp
 
    print("msg-->",msg)
    resp = MessagingResponse()
    reply=resp.message()
    # Create reply
    if msg == "hi":
       reply.body("hello!")
 
    
    issue_dict = {
        'project': {'key': 'INT'},
        'summary': 'Testing support bot',
        'description': 'Please ignore',
        'issuetype': {'name': 'Bug'},
    }
    new_issue = jira.create_issue(
        project='INT', 
        summary='New issue from support-bot',
         description='Look into this one', 
         issuetype={'name': 'Task'})
    
    reply.body(f"Se creó el ticket de soporte: {new_issue.key}. Gracias!")

    return str(resp)
 
if __name__ == "__main__":	
    app.run(debug=True)