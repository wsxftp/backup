#!/usr/bin/python3
import os
import re
import pymysql
import datetime


def File_name(path='/NIIS/FileRoot/live/'):
    file = os.listdir(path)
    # print(file)
    for i in file:
        if re.search(r'm3u8', i):
            for y in os.listdir('{}/Ts/{}'.format(path, i[0:32])):
                yield '{}Ts/{}/{}'.format(path, i[0:32], y)


def Format_size(size):
    size = round(size / 1048576, 2)
    return '{}M'.format(size)


def clear_data():
    db = pymysql.connect("47.94.135.239", "grafana", "grafana", "grafana")
    db.cursor().execute('DELETE FROM big_file')
    db.commit()
    db.close()


def insert_data(file, size):
    db = pymysql.connect("47.94.135.239", "grafana", "grafana", "grafana")
    if not db.cursor().execute(
            "SELECT size from big_file WHERE file='{}'".format(file)):
        db.cursor().execute(
            "INSERT INTO big_file (file,size) VALUES ('{}','{}')".format(
                file, size))
    db.commit()
    db.close()


def main():
    # time = datetime.datetime.now().strftime('%d')
    for i in File_name():
        sizefile = os.stat(i).st_size
        # if datetime.datetime.now().strftime('%d') != time:
        #     clear_data()
        #     time = datetime.datetime.now().strftime('%d')
        if sizefile > 2097152:
            insert_data(i, Format_size(sizefile))


if __name__ == '__main__':
    main()
