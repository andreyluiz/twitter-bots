import glob
import sys
import csv
import numpy
import scipy.stats

filename = sys.argv[1]

def get_tweets(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        return list(csv_reader)

def get_stats(tweet_id, retweets_count, scores):
    a = 1.0 * (numpy.array(scores))
    n = len(a)
    m = numpy.mean(a)
    se = scipy.stats.sem(a)
    h = se * scipy.stats.t._ppf((1 + 0.99) / 2.0, n - 1)
    media = ((100 * m) + (100 * h)) / 2
    sample_count = len(scores)

    stats = ''
    stats += '-------- BEGIN STATS ---------\n'
    stats += 'Tweet ID: {}\n'.format(tweet_id)
    stats += 'Total: {}\n'.format(str(retweets_count)) 
    stats += 'Amostra: {}\n'.format(str(sample_count))
    stats += 'Média: {0:.2f}%\n'.format(media)
    stats += 'IC: {}, {}\n'.format(str( (m-h) * retweets_count ), str( (m+h) * retweets_count ))
    stats += '--------- END STATS ----------\n'
    return stats

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('No file has been specified. Please pass a file name as argument.')
        sys.exit(1)

    files = glob.glob('files/{}-*.csv'.format(filename))

    tweets = get_tweets('files/{}.csv'.format(filename))

    for file in files:
        tweet_id = file.replace('files/{}-'.format(filename), '').replace('.csv', '')

        tweet = [t for t in tweets if t[5] == tweet_id][0]

        with open(file, mode='r') as retweets_file:
            csv_reader = csv.reader(retweets_file, delimiter=',')
            retweets_list = list(csv_reader)
            scores = [float(col[1]) for col in retweets_list if float(col[1]) != -1.0]
            stats = get_stats(tweet_id, int(tweet[3]), scores)
            
            print(stats)
