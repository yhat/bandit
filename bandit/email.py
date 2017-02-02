from .yhat_json import json_dumps
import mimetypes
import base64
import warnings
from exceptions import UserWarning
import sys
import os

_DEFAULT_BODY = """Your job has completed. This is the default message. You can
customize this message by creating an email object: `from bandit import Email` and `email.body(html or string)`
function and passing it stringified HTML or a plaintext string.""".replace("\n", " ")
_DEFAULT_BODY += "\n\nCheers!\n~Team Bandit"

class Email(object):
    """
    Use the Email objects to programatically send e-mail alerts with Bandit.
    """
    def __init__(self, recipients=[], subject="", body="", write_json=True):
        if isinstance(recipients, str):
            recipients = [recipients]
        elif not isinstance(recipients, list):
            raise Exception("recipients must be a list or string")

        self._recipients = recipients
        self._subject = subject if subject else "Bandit Job"
        self._body = body if body else _DEFAULT_BODY
        self._attachments = [] # attachments
        self.write_json = write_json
        self._write()

    def _to_dict(self):
        "private method for dictifying an Email"
        return {
            "recipients": self._recipients,
            "subject": self._subject,
            "body": self._body,
            "attachments": self._attachments,
            "isHTML": True
        }

    def _write(self):
        """
        Emails get written to a JSON file by default. This is then picked up by
        the bandit job runner and converted into a *real* email.
        """
        if self.write_json==False:
            return self._to_dict()

        data = json_dumps(self._to_dict())
        if os.path.exists('/job/metadata'):
            with open('/job/metadata/email.json', 'wb') as f:
                f.write(data)

    def __str__(self):
        """
        Default stringified message looks like this:


        ======================================================================
        joe.smith@test.com, bob.smith@test.com
        ======================================================================
        > Bandit Job
        ======================================================================
        Your job has completed. This is the default message. You can customize
        this message by calling the `bandit.job.body(html or string)` function
        and passing it stringified HTML or a plaintext string.

        Cheers!
        ~Team Bandit
        ======================================================================
        """
        msg = [
            "="*70,
            ", ".join(self._recipients),
            "="*70,
            "> %s" % self._subject,
            "="*70,
            self._body,
            "="*70,
            "\n".join(["  - " + attachment['name'] for attachment in self._attachments])
        ]
        return "\n".join(msg)

    def subject(self, string):
        """
        Add a subject to your email

        Parameters
        ==========
        string: str
            the subject line of your email
        """
        self._subject = string
        self._write()

    def body(self, html_or_string):
        """
        Add a body to your email

        Parameters
        ==========
        html_or_string: str
            the body of your email. this can be either HTML or plaintext
        """
        self._body = html_or_string
        self._write()

    def add_attachment(self, filepath, filetype=None):
        """
        Add an attachment to your email

        Parameters
        ==========
        filepath: str
            path to the file you'd like to attach
        """

        if filetype is None:
            filetype, _ = mimetypes.guess_type(filepath)

        with open(filepath, 'rb') as f:
            content = f.read()
            n_bytes = sys.getsizeof(content)
            if n_bytes > 1000000:
                sys.stderr.write("Attachment is too large! %s is %d bytes\n" % (filepath, n_bytes))
                return
            attachment = {
                "type": filetype,
                "name": os.path.basename(filepath),
                "content": base64.encodestring(content)
            }
            self._attachments.append(attachment)
            self._write()

    def send(self, to):
        """
        Send an email to someone(s)

        Parameters
        ==========
        recipients: str or list
            str if one person, list if multiple
        """
        if isinstance(to, str):
            warnings.warn("the recipients you passed to the `send` method were formatted as a string. Bandit will split into individual emails using a comma. Please consider using a list instead!", UserWarning)
            to = to.split(',')
        self._recipients = to
        self._write()


# email = Email(write_json=False)
# # email = Email()
# email.body('hi')
# print email
