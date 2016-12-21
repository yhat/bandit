import json
import os

def metadata(json_blob):
    _write_metadata(json_blob)

def add_metadata_key(key, value):
    """
    Add key value pair to your metdata.

    Parameters
    ==========
    key: str
        name of the value you'd like to save
    value: object
        value of what you'd like to save

    Examples
    ========
    >>> add_metadata_key("r2", 0.82)
    >>> add_metadata_key("foo", "bar")
    """
    metadata = _get_metadata()
    metadata[key] = value
    _write_metadata(json.dumps(metadata))

def _write_metadata(metdata_json):
    try:
        json_blob = json.loads(metdata_json)
    except Exception as e:
        raise Exception("json_blob is invalid json: %s" % str(e))

    if not os.path.exists('metadata/metadata.json'):
        print(json_blob)
        return

    with open('metadata/metadata.json', 'wb') as f:
        json.dump(json_blob, f)

def _get_metadata():
    if not os.path.exists('metadata/metadata.json'):
        return {}

    with open('metadata/metadata.json', 'rb') as f:
        return json.load(f)

def set_status(status):
    if status not in ['failed', 'success']:
        raise Exception("Invalid status: %" % status)
    os.environ['BANDIT_JOB_STATUS'] = status

_DEFAULT_BODY = """Your job has completed. This is the default message. You can
customize this message by calling the `bandit.job.body(html or string)`
function and passing it stringified HTML or a plaintext string.""".replace("\n", " ")
_DEFAULT_BODY += "\n\nCheers!\n~Team Bandit"

class Email(object):
    """
    Use the Email objects to programatically send e-mail alerts with Bandit.
    """
    def __init__(self, subject="", body="", attachments=[], write_json=True):
        self._subject = subject if subject else "Bandit Job"
        self._body = body if body else _DEFAULT_BODY
        self._attachments = attachments
        self.write_json = write_json

    def _to_dict(self):
        "private method for dictifying an Email"
        return {
            "subject": self._subject,
            "body": self._body,
            "attachments": self._attachments
        }

    def _write(self):
        """
        Emails get written to a JSON file by default. This is then picked up by
        the bandit job runner and converted into a *real* email.
        """
        if self.write_json==False:
            return

        with open('email.json', 'wb') as f:
            json.dump(self._to_dict(), f)

    def __str__(self):
        """
        Default stringified message looks like this:

        > Bandit Job
        Your job has completed. This is the default message. You can customize
        this message by calling the `bandit.job.body(html or string)` function
        and passing it stringified HTML or a plaintext string.

        Cheers!
        ~Team Bandit
        """
        msg = [
            "="*80,
            "> %s" % self._subject,
            self._body,
            "="*80,
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

    def attachment(self, attachment):
        """
        Add an attachment to your email

        Parameters
        ==========
        attachment: instance of StringIO
            attachment for your email. this needs to be a StringIO object. you can
            format most file types as a StringIO filetype (for example a png)
        """
        self._attachments.append(attachment)

# email = Email(write_json=False)
# # email = Email()
# email.body('hi')
# print email
