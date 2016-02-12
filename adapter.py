import argparse
import settings
import datetime

from models import *
from session import get_session


parser = argparse.ArgumentParser()
parser.add_argument('table',  help='Name of the table to generate')
parser.add_argument('-c', '--connection_string', help='Database connection string',
                    default = settings.DEFAULT_CONNECTION_STRING)

def print_row(*args):
    print('|'.join(args))


def print_users(session):
    print_row('Brukernavn', 'Fornavn', 'Etternavn', 'Epost', 'Klasse', 'Klassetrinn', 'Kjønn')

    for user in session.query(User):
        program = user.getProgram()
        cls = user.getClass()
        gender = user.getGender()
        if program and cls:
            print_row(user.username, user.first_name, user.last_name, user.mail, program, cls, gender)

if __name__ == '__main__':
    args = parser.parse_args()
    session = get_session(args.connection_string)
    if args.table == 'user':
        print_users(session)

