import pathlib
import tweepy
import time

def get_tokens():
    tokens = []
    with open('tokens/tokens.txt') as file:
        tokens = file.read().splitlines()
    return tokens

def authenticate():
    tokens = get_tokens()
    consumer_key        = tokens[0] #
    consumer_secret     = tokens[1] #       ACCESS and API Keys should be saved inside the tokens.txt in this order:
    access_token        = tokens[2] #       1: API Key    2: API Secret
    access_token_secret = tokens[3] #       3: Access Key 4:Access Secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def get_media_id(api, file):
    media = api.media_upload(file)
    media_id_list = []
    media_id_list.append(media.media_id)
    return media_id_list

def get_last_mentions(api):
    list = []
    for mention in api.mentions_timeline():
        list.append(mention.id)
    return list

def reply_to_new_mentions(api, last_mentions, already_replied, media_id_list):
    for mention in last_mentions:
            if mention not in already_replied:
                api.update_status('Ah éé', in_reply_to_status_id = mention, auto_populate_reply_metadata = True, media_ids = media_id_list)
                already_replied.append(mention)
                print(f'Tweet Replied!')
    return

def main():
    auth = authenticate()
    api = tweepy.API(auth, wait_on_rate_limit=True)

    file = 'media/ah eh.mp4'
    media_id_list = get_media_id(api, file)
    already_replied = get_last_mentions(api)

    while True:
        print('Checking last mentions')
        last_mentions = get_last_mentions(api)
        reply_to_new_mentions(api,last_mentions,already_replied,media_id_list)
        time.sleep(60)

if __name__ == '__main__':
    main()