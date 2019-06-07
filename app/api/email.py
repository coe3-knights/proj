from app import models
from threading import Thread
from flask import current_app, render_template,jsonify
from flask_mail import Message
from app import mail



def sendAsyncEmail(app, msg):
   with app.app_context():
        mail.send(msg)


def sendEmail(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body  

        if attachments:
            for attachment in attachments:
                msg.attach(*attachment)
        
        if sync:
            mail.send(msg)
              
        else:
            Thread(target=sendAsyncEmail,
                args=(current_app._get_current_object(), msg)).start()
    except:
        return None  

def sendPaswordRequest(user):
    token = user.getPasswordResetToken()
    sendEmail('[Knights Project Manager] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('reset_password.html',
                                     user=user, token=token))
