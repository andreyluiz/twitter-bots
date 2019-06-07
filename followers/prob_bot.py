import sys
import time
import csv
import random
import botometer
# import pymysql
import tweepy
import pymysql
# from google.cloud import storage
from multiprocessing import Process, Manager

start = time.time()

# bucket_name = 'twitter-bots-239422.appspot.com'
# project_id = 'twitter-bots-239422'
# file_arg = sys.argv[1]
# file_name = file_arg + '.csv'
# updated_file_name = file_arg + '-updated.csv'
# file_name = 'seguidores_sample.csv'

def conecta_banco():
    db = pymysql.connect("localhost", "root", "82356000", "twitterbots")
    return db

# def get_list_from_file():
#     with open(file_name, mode='r') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         return list(csv_reader)

# def save_list_to_file(followers):
#     with open(updated_file_name, mode='w') as target_file:
#         csv_writer = csv.writer(target_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         for f in followers:
#             csv_writer.writerow(f)

# def update_followers_score(followers, score_table):
#     for follower in followers:
#         score = score_table[follower[0]]
#         follower[1] = score

def create_lista(id):
    db = conecta_banco()
    cursor = db.cursor()

    sql = '''
    select seg.* from twitterbots.seguidores as seg
    inner join twitterbots.politicos_seguidores as polseg on seg.id = polseg.id_seguidor
    where polseg.id_politico = {} and seg.probabilidade is null
    '''.format(id)
    cursor.execute(sql)

    lista = list(cursor.fetchall())
    db.close()
    random.shuffle(lista)

    return lista

def update_pessoa(id, prob):
    db = conecta_banco()
    cursor = db.cursor()

    sql = 'UPDATE seguidores SET probabilidade="{}" WHERE id="{}";'.format(str(prob), str(id))

    cursor.execute(sql)
    db.commit()
    db.close()

def process_list(lista, bom):
    count = 1
    results = bom.check_accounts_in(map(lambda x: x[0], lista), retries=3)

    for key, value in results:
        score = -1
        if 'cap' in value:
            cap = value['cap']
            score = cap['universal']
            name = value['user']['screen_name']
            print('{}:\t\t{}\t\t{}\t\t{}'.format(count, name, score, int(time.time() - start)))
        else:
            print('{}:\t\t{}\t\t{}\t\t{}'.format(count, key, value['error'], int(time.time() - start)))
            
        update_pessoa(key, score)
        # out[key] = score
        count += 1

    # return out

    # count = 0

    # for seguidor in lista:
    #     score = -1
    #     try:
    #         id = seguidor[0]
    #         result = bom.check_accounts_in(id)
    #         score = result['cap']['universal']
    #         screen_name = result['user']['screen_name']

    #         print (str(count) + ":\t" + screen_name + "  " + str(score))
    #     except Exception as inst:
    #         print (seguidor[0])
    #         score = -1
    #         print (inst)

    #     out[id] = score
    #     count += 1

# def download_csv_file():
#     storage_client = storage.Client(project_id)
#     bucket = storage_client.bucket(bucket_name, project_id)
#     blob = bucket.blob(file_name)
#     blob.download_to_filename(file_name)

#     print('File {} downloaded successfully.'.format(file_name))
#     print()

# def upload_csv_file():
#     storage_client = storage.Client(project_id)
#     bucket = storage_client.bucket(bucket_name, project_id)
#     blob = bucket.blob(updated_file_name)
#     blob.upload_from_filename(updated_file_name)

#     print('File {} uploaded successfully.'.format(updated_file_name))
#     print()

if __name__ == "__main__":
    mashape_key = "3513c85054msh51ec072ce1ba338p1d32ffjsn3800d4e150fa"
    twitter_app_auth = {
        'consumer_key': 'ikNwHJe2PFBTBFdAi3NVnkwsM',
        'consumer_secret': 'C65EUhUh7crrSzk5D3p5ZH8NlfGjFjUEPGjmm0Pp2SYUmJTnkO',
        'access_token': '97265487-zw76B5hOJ49TIwvbeewqkkfjlu17irgzMkGa7j9jU',
        'access_token_secret': 'noo7JZGhVK1aXPPNfUT6RYUIqoDboe6c0K8iLQDtuKPvL',
    }

    bom = botometer.Botometer(wait_on_ratelimit=True,
                              mashape_key=mashape_key,
                              **twitter_app_auth)

    auth = tweepy.OAuthHandler('ikNwHJe2PFBTBFdAi3NVnkwsM', 'C65EUhUh7crrSzk5D3p5ZH8NlfGjFjUEPGjmm0Pp2SYUmJTnkO')
    auth.set_access_token('97265487-zw76B5hOJ49TIwvbeewqkkfjlu17irgzMkGa7j9jU',
                          'noo7JZGhVK1aXPPNfUT6RYUIqoDboe6c0K8iLQDtuKPvL')

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=2, retry_delay=5,
                     retry_errors=set([503]))

    jobs = []
    # processes = 2
    # chunk_size = int(5000 / processes)
    # manager = Manager()
    # score_table = manager.dict()
    # download_csv_file()
    print('ID: ' + sys.argv[1])
    followers = create_lista(sys.argv[1])
    # followers_chunks = [followers[i:i + chunk_size] for i in range(0, len(followers), chunk_size)]

    print('Starting API calls...')

    process_list(followers, bom)

    # for i in range(0, processes):
    #     job = Process(target=process_list, args=(followers_chunks[i], bom, score_table))
    #     jobs.append(job)

    # for job in jobs:
    #     job.start()

    # for job in jobs:
    #     job.join()

    print()
    # update_followers_score(followers, score_table)
    # save_list_to_file(followers)
    # upload_csv_file()

    print('Finished in {} seconds.'.format(time.time() - start))