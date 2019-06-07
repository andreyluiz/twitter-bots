import csv
import pymysql

def get_list_from_file():
    with open('files/vtvcanal-updated.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        return list(csv_reader)

def save_to_database(followers):
    print(followers[0])
    followers = [(f[1], f[0]) for f in followers]
    print(followers[0])
    sql = 'UPDATE seguidores SET probabilidade = %s WHERE id = %s;'
    db = pymysql.connect("localhost", "root", "82356000", "twitterbots")
    cursor = db.cursor()
    cursor.executemany(sql, followers)
    db.commit()
    db.close()

if __name__ == '__main__':
    followers = get_list_from_file()
    save_to_database(followers)