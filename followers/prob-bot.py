import random
import sys
import botometer
import pymysql
import tweepy


def conecta_banco():
    db = pymysql.connect("localhost", "root", "82356000", "twitterbots2")
    return db

def create_lista (id):
    db = conecta_banco()
    cursor = db.cursor()

    sql = '''
    select seg.* from twitterbots2.seguidores as seg
    inner join twitterbots2.politicos_seguidores as polseg on seg.id = polseg.id_seguidor
    where polseg.id_politico = {} and seg.probabilidade is null
    '''.format(id)
    cursor.execute(sql)

    lista = cursor.fetchall()
    db.close()

    return list(lista)

def update_pessoa(id, prob):
    db = conecta_banco()
    cursor = db.cursor()

    sql = "UPDATE seguidores SET probabilidade = {} WHERE id = {}".format(str(prob), str(id))

    cursor.execute(sql)
    db.commit()
    db.close()

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

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=1, retry_delay=5,
                 retry_errors=set([503]))


lista = create_lista(sys.argv[1])
random.shuffle(lista)
count = 0

for seguidor in lista:
    try:
        result = bom.check_account(seguidor[0])
        count += 1
        print (str(count) + ":\t" + result['user']['screen_name'] + "  " + str(result['cap']['universal']))
        update_pessoa(seguidor[0], result['cap']['universal'])
    except Exception as inst:
        print (seguidor[0])
        update_pessoa(seguidor[0], -1)
        print (inst)

    print()
