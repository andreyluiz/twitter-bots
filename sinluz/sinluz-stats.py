import glob
import sys
import csv
import numpy
import scipy.stats

def get_users(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        return list(csv_reader)

def get_stats(scores):
    a = 1.0 * (numpy.array(scores))
    n = len(a)
    m = numpy.mean(a)
    se = scipy.stats.sem(a)
    h = se * scipy.stats.t._ppf((1 + 0.99) / 2.0, n - 1)
    media = ((100 * m) + (100 * h)) / 2
    sample_count = len(scores)

    stats = ''
    stats += '-------- BEGIN STATS ---------\n'
    stats += 'Amostra: {}\n'.format(str(sample_count))
    stats += 'Média: {0:.2f}%\n'.format(media)
    stats += 'IC: {}, {}\n'.format(str( (m-h) * sample_count ), str( (m+h) * sample_count ))
    stats += '--------- END STATS ----------\n'
    return stats

if __name__ == '__main__':
    users = get_users('files/sinluz-scored.csv')
    scores = [float(col[1]) for col in users if float(col[1]) != -1]
    stats = get_stats(scores)
    
    print(stats)
