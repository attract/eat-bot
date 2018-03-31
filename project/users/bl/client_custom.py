from urllib.parse import parse_qs, urlparse, urlunparse

import httplib2
import oauth2

from core.bl.utils_helper import prn


class ClientCustom(oauth2.Client):
    def request(self, uri, method="GET", body=b'', headers=None,
                redirections=httplib2.DEFAULT_MAX_REDIRECTS, connection_type=None, parameters=None):

        DEFAULT_POST_CONTENT_TYPE = 'application/x-www-form-urlencoded'

        if not isinstance(headers, dict):
            headers = {}

        if not isinstance(parameters, dict):
            parameters = {}

        if method == "POST":
            headers['Content-Type'] = headers.get('Content-Type', DEFAULT_POST_CONTENT_TYPE)

        is_form_encoded = \
            headers.get('Content-Type') == 'application/x-www-form-urlencoded'

        if is_form_encoded and body:
            parameters = parse_qs(body)
        # else:
        #     parameters = None
        req = oauth2.Request.from_consumer_and_token(self.consumer, token=self.token,
                                                     http_method=method, http_url=uri,
                                                     parameters=parameters, body=body,
                                                     is_form_encoded=is_form_encoded)
        req.sign_request(self.method, self.consumer, self.token)

        scheme, netloc, path, params, query, fragment = urlparse(uri)
        realm = urlunparse((scheme, netloc, '', None, None, None))

        if is_form_encoded:
            body = req.to_postdata()
        elif method == "GET":
            uri = req.to_url()
        else:
            headers.update(req.to_header(realm=realm))

        return httplib2.Http.request(self, uri, method=method, body=body,
                                     headers=headers, redirections=redirections,
                                     connection_type=connection_type)
