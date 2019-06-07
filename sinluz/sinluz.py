import sys
import tweepy
import botometer
import csv
import os.path

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

def print_progress(count, total):
    print('Progress: {}%'.format(str(int((count / total) * 100))), end='\r')

def extract_score(bom_result):
    return bom_result['cap']['universal']

if __name__ == '__main__':
    api = get_twitter_api()
    bom = get_botometer_api()
    # tweets = get_tweets('files/sinluz/sinluz.csv')

    # user_ids = [t[8] for t in tweets[1:]]
    # users_count = len(user_ids)

    # count = 0
    # with open('files/sinluz/sinluz-scored.csv', mode='w') as retweet_file:
    #     csv_writer = csv.writer(retweet_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     print_progress(0, users_count)
    #     for user_id in user_ids:
    #         score = -1
    #         try:
    #             result = bom.check_account(user_id)
    #             if 'cap' in result:
    #                 score = extract_score(result)
    #         except:
    #             pass
    #         count += 1
    #         print_progress(count, users_count)
    #         csv_writer.writerow((user_id, score))
    #         retweet_file.flush()
    tweets = get_tweets('files/sinluz-scored.csv')

    users_count = len(tweets)

    count = 0
    with open('files/sinluz-scored2.csv', mode='w') as retweet_file:
        csv_writer = csv.writer(retweet_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        print_progress(0, users_count)
        for tweet in tweets:
            user_id = tweet[0]
            score = float(tweet[1])
            if score == -1:
                try:
                    result = bom.check_account(user_id)
                    if 'cap' in result:
                        score = extract_score(result)
                    else:
                        print(result)
                except Exception as e:
                    print(e)
                    pass
            count += 1
            print_progress(count, users_count)
            csv_writer.writerow((tweet[0], score))
            retweet_file.flush()