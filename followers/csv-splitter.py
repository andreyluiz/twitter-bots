import csv

filename = 'vtvcanal'

def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

with open(filename + '.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    the_list = list(csv_reader)
    splitted = chunks(the_list, 5000)

    for i, lst in enumerate(splitted):
        with open(filename + '-' + str(i) + '.csv', mode='w') as new_file:
            csv_writer = csv.writer(new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in lst:
                csv_writer.writerow(item)
    