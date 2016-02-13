import argparse
import settings
import datetime

from session import get_session
from tablegenerator import TableGenerator


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--table',  help='Name of the table to generate')
parser.add_argument('-c', '--connection_string', help='Database connection string',
                    default = settings.DEFAULT_CONNECTION_STRING)
"""
def print_row(*args):
    print('|'.join([str(element) for element in args]))


def print_users(session):
    print_row('Bruker ID', 'Brukernavn', 'Fornavn', 'Etternavn', 'Epost', 'Klasse', 'Klassetrinn', 'Kjønn')

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
    print_row('Event ID', 'Eventnavn', 'Eventtype', 'Eventintro', 'Eventsted', 'Event Antall Plasser', 'Event Trenger Registrering', 'Eventstart', 'Eventslutt', 'Event Trenger Feedback', 'Eventpris Medlemmer', 'Eventpris Gjester')
    events = session.query(Event).filter(Event.capacity < 1000) # filter bogus events
    for event in events:
        print_row(
            event.id,
            format_text(event.name),
            format_event_type(event.type),
            format_text(event.intro),
            format_text(event.location),
            event.capacity if event.capacity > 0 else 'Ubegrenset',
            format_boolean(event.is_registration_required),
            event.start_date,
            event.end_date,
            format_boolean(event.feedback_when_registering),
            event.price_members,
            event.price_guests
        )

def print_user_groups(session):
    print_row('Gruppenavn', 'Gruppe Er Komite')
    groups = session.query(Group)\
        .filter(Group.deleted == False)
    for group in groups:
        print_row(
            format_text(group.name),
            format_boolean(group.is_committee)
        )

def print_membership(session):
    print_row('Bruker ID', 'Gruppe ID')
    for m in session.query(Membership):
        print_row(
            m.user_id,
            m.group_id
        )


"""
if __name__ == '__main__':
    args = parser.parse_args()
    session = get_session(args.connection_string)
    gen = TableGenerator(session)
    gen.generate_tables(args.table)
