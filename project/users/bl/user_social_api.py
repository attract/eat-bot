import json

import oauth2
import requests
from django.conf import settings

from core.bl.utils_helper import prn
from photos.models import Photo
from users.bl.client_custom import ClientCustom


class UserSocialApi(object):
    user = None
    social_accounts = {settings.FACEBOOK_PROVIDER:None,
                   settings.TWITTER_PROVIDER:None,
                   settings.PINTEREST_PROVIDER:None,
                   }
    with_debug = True

    def __init__(self, user):
        self.user = user
        self.user_social = {}
        user_social = self.user.user_social.filter(is_active=True).all()
        for one_social in user_social:
            self.social_accounts[one_social.provider] = one_social

    def share_photo_facebook(self, photo):
        prn('Sharing facebook photo')
        # API DOCS https://developers.facebook.com/docs/graph-api/using-graph-api/
        #          https: // developers.facebook.com / docs / graph - api / photo - uploads
        user_social = self.social_accounts[settings.FACEBOOK_PROVIDER]
        if not user_social:
            prn('Error! User have no facebook account')
            return False

        user_id = user_social.uid
        access_token = user_social.get_token()
        # SHARE_URL EXAMPLE = 'https://graph.facebook.com/{user-id}/feed?message={message}&access_token={access-token}'
        # user_id = 2017486768528419
        # access_token = 'EAAC8rPvk6FMBAC0rkboSCPrAinDIQDgQf6beIRrxjmLKIhlnb2zOjjt2GMuHmwdKLGvojs0nqWEZC0NUN64ZC7rmSuUvkmv4vM9rS31WdizxmWjKZC0OUYD4h7YEzmZAVzAJ47wFSpRqidIOgSSXbvjGVFFv1Rv7RxeZAwclFYfauyGy6semmGZCY5fPENkcSwV7VuZCMZCkAbf0Pr1JEaCdY40zNfnjhSE72XmZBPg9XiAZDZD'

        # TODO PHOTO POST TEXT
        message = ''
        # photo = Photo.objects.filter(id=40).first()
        if photo.description:
            message += photo.description
        else:
            message += 'Look at my pet!'
        image_url = "%s%s%s" % (settings.SITE_URL, settings.MEDIA_URL, photo.image)
        # adding to feed
        # api_url = '%s%s/feed?' % (settings.FACEBOOK_API_URL, user_id)

        # adding to photos
        api_url = '%s%s/photos?' % (settings.FACEBOOK_API_URL, user_id)

        if self.with_debug:
            api_url += "&debug=all"

        # POST MESSAGE
        # response = requests.post(api_url, data={'message': message,
        #                                         'link': image_url,
        #                                         'access_token': access_token,
        #                                         'fields': 'created_time,from,id,message,permalink_url'}, json=None,)

        # POST PHOTO
        response = requests.post(api_url, data={'caption': message,
                                                'url': image_url,
                                                'access_token': access_token,
                                                'fields': 'created_time,id,permalink_url'}, json=None,)
        api_data = response.json()
        if response.status_code != 200:
            prn('Error')
        else:
            prn('No Error')

    def share_photo_twitter(self, photo_todo):
        prn('Sharing twitter photo')
        # TWITTER API to tweet https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-update

        # TODO PHOTO TEXT, need my account to delete created tweets
        message = 'Petrater.'
        api_url = 'https://api.twitter.com/1.1/statuses/update.json?status=%s' % message
        user_social = self.social_accounts[settings.TWITTER_PROVIDER]
        if not user_social:
            prn('Error! User have no twitter account')
            return False

        token = user_social.get_token()
        token_secret = user_social.get_token(need_secret=True)
        options = {'method': 'POST'}
        api_data = self.send_query_oauth2(settings.TWITTER_PROVIDER, api_url, token,
                                          token_secret, options)
        if 'error' in api_data:
            prn(api_data['error'])
        else:
            prn('Photo is tweeted')

    def share_photo_pinterest(self, photo_todo):
        prn('Sharing pinterest photo')
        # PINTEREST API to post board https://developers.pinterest.com/docs/api/boards/

        user_social = self.social_accounts[settings.PINTEREST_PROVIDER]
        if not user_social:
            prn('Error! User have no twitter account')
            return False

        # TODO PHOTO TEXT, need to check permission Scope: "write_public"
        # now error is code 3 = Authorization failed.
        name = 'petrater_name'
        description = 'petrater_description'
        token = user_social.get_token()

        api_url = 'https://api.pinterest.com/v1/boards/?access_token=%s' % token

        # 'https://api.pinterest.com/v1/me/?access_token=AXhhzU8fJ--rJNqewxPnz49GL-h1FQaM3NK05uhEmRoNmqA5xAAAAAA'
        options = {'method': 'POST',
                   'post_parameters': {'access_token': token,
                                       'name': name,
                                       'description': description}}

        prn(api_url)
        api_data = UserSocialApi.send_query_oauth2(settings.PINTEREST_PROVIDER, api_url,
                                                   options=options)
        if 'data' in api_data and api_data['data']:
            prn("Board is created")
        else:
            prn('Pinterest API ERROR')
            prn(api_data['message'])

    @classmethod
    def send_query_oauth2(cls, provider, api_url, token='', token_secret='', options={}):

        if provider == settings.TWITTER_PROVIDER:
            app_key = settings.SOCIAL_AUTH_TWITTER_KEY
            app_secret = settings.SOCIAL_AUTH_TWITTER_SECRET
        elif provider == settings.PINTEREST_PROVIDER:
            app_key = settings.SOCIAL_AUTH_PINTEREST_KEY
            app_secret = settings.SOCIAL_AUTH_PINTEREST_SECRET
        # token = '3940088003-WencvC7vRxJXx12pVSbaNtnRoLJGFbKaqbSNej4'
        # secret_token = '091I7J44twn9SOKcz0oOHYItsjqBORiRB7L2HmRADtYJO'

        consumer = oauth2.Consumer(key=app_key,
                                   secret=app_secret)
        token_oauth = None
        if token or token_secret:
            token_oauth = oauth2.Token(key=token, secret=token_secret)

        client = ClientCustom(consumer, token_oauth)

        method = options['method'] if 'method' in options else "GET"
        parameters = options['post_parameters'] if 'post_parameters' in options else {}

        resp, content = client.request(api_url, method, parameters=parameters)
        api_data = json.loads(content.decode("utf-8"))
        if 'errors' in api_data:
            errors = ''
            for one_error in api_data['errors']:
                errors += '%s(API Error code=%s). \n' % (one_error['message'], one_error['code'],)
            api_data['error'] = errors
        return api_data

    def get_permissions(self):
        pass
        # permissions check
        # api_url = '%s%s/permissions?access_token=%s' % (settings.FACEBOOK_API_URL, user_id, access_token)
        # response = requests.get(api_url)

