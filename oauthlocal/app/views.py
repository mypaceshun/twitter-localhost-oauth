import os
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

base_url = 'https://api.twitter.com/'


@require_http_methods(['GET', 'POST'])
def top_view(request):
    twitter = OAuth1Session(consumer_key, consumer_secret)

    request_token_url = base_url + 'oauth/request_token'
    response = twitter.post(request_token_url)
    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    authenticate_url = base_url + 'oauth/authenticate'
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])
    context = {'link_url': authenticate_endpoint}
    return render(request, 'top.html', context)

@require_http_methods(['GET'])
def callback_view(request):
    data = request.GET
    print(data)
    oauth_token = data['oauth_token']
    oauth_verifier = data['oauth_verifier']
    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_verifier,
    )
    access_token_url = base_url + 'oauth/access_token'
    response = twitter.post(
        access_token_url,
        params={'oauth_verifier': oauth_verifier}
    )
    access_token = dict(parse_qsl(response.content.decode("utf-8")))
    context = {'access_token': access_token}

    return render(request, 'result.html', context)
