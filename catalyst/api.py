# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth2Session
from purl import URL

__all__ = ['Session']

ENDPOINT = URL('https://api.pandadoc.com/public/v1/')
OAUTH_AUTHORIZATION_ENDPOINT = URL('https://app.pandadoc.com/oauth2/authorize')
OAUTH_ACCESS_TOKEN_ENDPOINT = URL('https://app.pandadoc.com/oauth2/access_token')

# URL: https://www.pandadoc.com/?state=Y6zMPkOP0Kd8ZhwbizLs23GidXPrPF&code=141eb28ea84f43d1bc9b170ab339d0b6f5f77a1f


"""
{u'access_token': u'a0cc60f407416f3f8cae1d2ac722f2c1774224eb',
 u'expires_at': 1529608481.317,
 u'expires_in': 31535999,
 u'refresh_token': u'afcec38a1ebb272ca56e12b977cc34841ea86c65',
 u'scope': [u'read', u'write', u'read+write'],
 u'token_type': u'Bearer'}
"""

class Session(OAuth2Session):
    """
    Pass in the client_id and token dict to get an authenticated connection.
    For server-side flows, use the pandadocs-tokentool to get the token dict.
    Otherwise, you will need to authorize the user, and
    fetch a token at runtime using the authorization_url and fetch_token methods.

    Here's an example of a token dict::

        token = {
            u'access_token': u'54be934eb3fdf031ccadd2406f2',
            u'expires_at': 1499753835.037497,
            u'expires_in': 31535999,
            u'refresh_token': u'2c1dd5a32d0aff0298c3b2214',
            u'scope': [u'read', u'write', u'read+write'],
            u'token_type': u'Bearer'
        }


    Args:
        client_id (str): the client ID from your application
        token (dict): the token dict with the access token
    """

    def __init__(self, *args, **kwargs):
        """constructor"""
        if 'scope' not in kwargs:
            kwargs['scope'] = ['read', 'write', 'read+write']

        super(Session, self).__init__(*args, **kwargs)

    def authorization_url(self, *args, **kwargs):
        if len(args) == 0 and 'url' not in kwargs:
            args = [OAUTH_AUTHORIZATION_ENDPOINT.as_string()]
        return super(Session, self).authorization_url(*args, **kwargs)

    def fetch_token(self, *args, **kwargs):
        if 'token_url' not in kwargs:
            kwargs['token_url'] = OAUTH_ACCESS_TOKEN_ENDPOINT.as_string()
        return super(Session, self).fetch_token(*args, **kwargs)

    # Templates stuff

    def get_templates(self, page=None):
        """
        Get a list of templates accessible to the currently authorized user.
        The results are paged, so you will only receive the first page by default.

        Args:
            page (int): an optional integer indicating the page you want to retrieve
        """
        url = ENDPOINT.add_path_segment('templates')
        if page is not None:
            url = url.query_param('page', page)
        return self.get(url.as_string())

    def iter_templates_pages(self):
        """Helper generator to iterate over all pages of the list of templates"""
        url = ENDPOINT.add_path_segment('templates').as_string()
        ret = self.get(url)

        yield ret
        while ret.json()['next'] is not None:
            ret = self.get(ret['next'])
            yield ret

    def iter_templates(self):
        """Helper generator to iterate over all templates accessible to the user"""
        for page in self.iter_templates_pages():
            results = page.json()['results']
            for item in results:
                yield item

    def get_template(self, id):
        """
        Get detailed information about a specific template

        Args:
            id (str): the template UUID
        """
        url = ENDPOINT.add_path_segment('templates/{0}/details'.format(id)).as_string()
        return self.get(url)

    # Document stuff

    def create_document(self, data):
        """
        Creat document from a template or file

        Args:
            id (str): the template UUID
            data (dict): data to fill within the document
        """
        url = ENDPOINT.add_path_segment('documents').as_string()
        return self.post(url, json=data)

    def send_document(self, id, message="", silent=True):
        """
        Send a document to a user

        Args:
            id (str):  the document UUID
            message (str):  message to send to the recipient
            silent (boolean): if True, does not send an email; instead puts the document into sent state. This is useful if the document will be signed in an iframe session
        """
        data = {
            'message': message,
            'silent': silent,
        }
        url = ENDPOINT.add_path_segment('documents/{0}/send'.format(id)).as_string()
        return self.post(url, json=data)

    def get_document(self, id):
        """
        Get document details

        Args:
            id (str):  the document UUID
        """
        url = ENDPOINT.add_path_segment('documents/{0}/details'.format(id)).as_string()
        return self.get(url)

    def download_document(self, id):
        """
        Download a document

        Args:
            id (str):  the document UUID
        """
        url = ENDPOINT.add_path_segment('documents/{0}/download'.format(id)).as_string()
        return self.get(url)


    # Session

    def create_session(self, id, email, lifetime=300):
        """
        Create session for a document

        Args:
            id (str):  the document UUID
            email (str): recipient's email address
            lifetime (int): in seconds (default 300s)
        """
        data = {
            'recipient': email,
            'lifetime': lifetime
        }
        url = ENDPOINT.add_path_segment('documents/{0}/session'.format(id)).as_string()
        return self.post(url=url, json=data)

    def get_session(self, data, email):
        """
        Get session details for a document
        """
        document = self.create_document(data)
        document_id = document.json()['uuid']
        self.send_document(document_id)
        session = self.create_session(document_id, email)
        return session
