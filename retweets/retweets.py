import sys
import tweepy
import botometer
import csv
import os.path

MAX_TWEETS = 15

twitter_auth = {
    'consumer_key': 'ikNwHJe2PFBTBFdAi3NVnkwsM',
    'consumer_secret': 'C65EUhUh7crrSzk5D3p5ZH8NlfGjFjUEPGjmm0Pp2SYUmJTnkO',
    'access_token': '97265487-zw76B5hOJ49TIwvbeewqkkfjlu17irgzMkGa7j9jU',
    'access_token_secret': 'noo7JZGhVK1aXPPNfUT6RYUIqoDboe6c0K8iLQDtuKPvL',
}

def get_twitter_api():
    auth = tweepy.OAuthHandler(twitter_auth['consumer_key'], twitter_auth['consumer_secret'])
    auth.set_access_token(twitter_auth['access_token'], twitter_auth['access_token_secret'])
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60,
                     retry_errors=set([503]))

def get_botometer_api():
    mashape_key = '3513c85054msh51ec072ce1ba338p1d32ffjsn3800d4e150fa'
    return botometer.Botometer(wait_on_ratelimit=True, mashape_key=mashape_key, **twitter_auth)

def get_tweets(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        return list(csv_reader)

def extract_score(bom_result):
    return bom_result['cap']['universal']

def print_progress(count, total):
    print('Progress: {}%'.format(str(int((count / total) * 100))), end='\r')

if __name__ == '__main__':
    api = get_twitter_api()
    bom = get_botometer_api()
    valid_tweets_count = 0
    if len(sys.argv) == 1:
        print('No file has been specified. Please pass a file name as argument.')
        sys.exit(1)

    filename = sys.argv[1]
    tweets = get_tweets('files/{}.csv'.format(filename))

    for tweet in tweets:
        if valid_tweets_count >= MAX_TWEETS:
            break

        tweet_id = tweet[5]

        print('Getting retweeters BOT CAP for tweet {}.'.format(tweet_id))
        retweeters_ids = api.retweeters(tweet_id)
        retweeters_count = len(retweeters_ids)

        if retweeters_count == 0:
            print('No retweeters found. Continuing...')
            continue

        retweets_file = 'files/{}-{}.csv'.format(filename, tweet_id)
        if os.path.isfile(retweets_file):
            print('File already exists. Skipping...')
            continue

        valid_tweets_count += 1
        print('{} retweeters found. Getting scores...'.format(retweeters_count))
        with open(retweets_file, mode='w') as retweet_file:
            csv_writer = csv.writer(retweet_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            count = 0
            print_progress(0, retweeters_count)
            for retweeter_id in retweeters_ids:
                score = -1
                try:
                    result = bom.check_account(retweeter_id)
                    if 'cap' in result:
                        score = extract_score(result)
                except:
                    pass
                count += 1
                print_progress(count, retweeters_count)
                csv_writer.writerow((retweeter_id, score))
                retweet_file.flush()

