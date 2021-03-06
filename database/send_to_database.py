#!/usr/bin/python
import pymysql
from sys import argv
from pync import Notifier


def send_to_db(args):
    '''
    Create your MySQL table with this command:

    CREATE TABLE `Email` (
    `email_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(58) NOT NULL,
    `is_opted_out` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
    `has_bounced` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (`email_id`),
    UNIQUE (`email`)
    ) ENGINE=InnoDB CHARSET=utf8 COLLATE utf8_unicode_ci;

    '''
    host = args.host
    user = args.user
    if args.port:
        port = args.port
    else:
        port = 3306
    passwd = args.password
    database = args.database
    file_to_send = args.file

    # Establish connection to local MySQL database
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database)

    cursor = db.cursor()

    s = str(file(file_to_send).read())
    w = s.split('\n')

    success = 0
    failed = 0

    for e in w:
        try:
            cursor.execute("INSERT INTO email(email) VALUES(%s)", (e))
            db.commit()
            success += 1
            print e + " was successfully added to database."
        except:
            db.rollback()
            failed += 1
            print e + " has failed to be added to database."


    db.close()
    return send_to_db
    Notifier.notify('Your import is complete.', title='Python email list importer')
    print 'There were %s emails successfully added to the database.' % success
    print 'There were %s emails that failed to be added to the database.' % failed


if __name__ == '__main__':
    main()
