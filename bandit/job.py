import json
import os
import sys

class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

class Metadata(Map):
    """
    Metadata that can be stored for your job.
    """
    def __setitem__(self, key, value):
        try:
            json.dumps(key)
            json.dumps(value)
        except Exception as e:
            raise Exception(e)
        super(Metadata, self).__setitem__(key, value)
        self._write_metadata(self)

    def __delitem__(self, key):
        super(Metadata, self).__delitem__(key)
        self._write_metadata(self)

    def _write_metadata(self, data):
        try:
            json.dumps(data)
        except Exception as e:
            raise Exception("data is not json serializable: %s" % str(e))

        if not os.path.exists('metadata/metadata.json'):
            sys.stderr.write(json.dumps(data, indent=2) + '\n')
            return

        with open('metadata/metadata.json', 'wb') as f:
            json.dump(data, f)

    def _get_metadata(self):
        if not os.path.exists('metadata/metadata.json'):
            return {}

        with open('metadata/metadata.json', 'rb') as f:
            return json.load(f)


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
