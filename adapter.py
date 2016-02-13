import argparse
import settings
import datetime

from models import *
from session import get_session
from format import format_event_type, format_boolean


parser = argparse.ArgumentParser()
parser.add_argument('table',  help='Name of the table to generate')
parser.add_argument('-c', '--connection_string', help='Database connection string',
                    default = settings.DEFAULT_CONNECTION_STRING)

def print_row(*args):
    print('|'.join([str(element) for element in args]))


def print_users(session):
    print_row('UserID', 'Brukernavn', 'Fornavn', 'Etternavn', 'Epost', 'Klasse', 'Klassetrinn', 'Kjønn')

    for user in session.query(User):
        if user.deleted: continue
        program = user.getProgram()
        cls = user.getClass()
        gender = user.getGender()
        if program and cls:
            print_row(
                user.id,
                user.username,
                user.first_name,
                user.last_name,
                user.mail,
                program,
                cls,
                gender
            )

def print_events(session):
    print_row('EventID', 'Eventnavn', 'Eventtype', 'Eventintro', 'Eventsted', 'Event Antall Plasser', 'Event Trenger Registrering', 'Eventstart', 'Eventslutt', 'Event Trenger Feedback', 'Eventpris Medlemmer', 'Eventpris Gjester')
    for event in session.query(Event):
        print_row(
            event.id,
            event.name,
            format_event_type(event.type),
            event.intro,
            event.location,
            event.capacity if event.capacity > 0 else 'Ubegrenset',
            format_boolean(event.is_registration_required),
            event.price_members,
            event.price_guests
        )

if __name__ == '__main__':
    args = parser.parse_args()
    session = get_session(args.connection_string)
    if args.table == 'user':
        print_users(session)
    elif args.table == 'event':
        print_events(session)

