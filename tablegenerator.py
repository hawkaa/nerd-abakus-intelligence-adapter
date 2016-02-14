import os
from datetime import datetime, date
from models import *

class TableGenerator():

    session = None

    def __init__(self, session):
       self.session = session

    def get_table_names(self):
        # find all gen methods
        methods = [m for m in dir(self) if callable(getattr(self, m)) and m.startswith('_gen_')]
        # remove _gen_
        return list(map( lambda x : x[5:], methods))



    def generate_tables(self, table = None):
        all_tables = self.get_table_names()
        if table != None:
            if table in all_tables: tables = [table]
            else: raise Exception('Invalid table name')
        else: tables = all_tables
        for t in tables:
            printer = Printer(t + '.csv')
            m = getattr(self, '_gen_' + t)
            m(printer)


    def _gen_brukere(self, p):
        users = self.session.query(User)\
            .filter(User.deleted == False)
        p.row('Bruker ID', 'Brukernavn', 'Fornavn', 'Etternavn', 'Epost', 'Klasse', 'Klassetrinn', 'Kjønn')
        for user in users:
            program = user.getProgram()
            cls = user.getClass()
            gender = user.getGender()
            if program and cls:
                p.row(
                    user.id,
                    user.username,
                    user.first_name,
                    user.last_name,
                    user.mail,
                    program,
                    cls,
                    gender
                )

    def _gen_eventer(self, p):
        events = self.session.query(Event)\
            .filter(Event.deleted == False)\
            .filter(Event.start_date >= date(2000, 1, 1))\
            .filter(Event.capacity < 1000) # filter bogus events

        event_mappings = {
            'Course' : 'Kurs',
            'Company presentation' : 'Bedpres',
            'Party' : 'Fest',
            'Other' : 'Annet',
            'Special' : 'Spesiell'
        }

        def format_event_type(e):
            if e.name in event_mappings: return event_mappings[e.name]
            else: return 'Ukjent'

        p.row('Event ID', 'Eventnavn', 'Eventtype', 'Eventintro', 'Eventsted', 'Event Antall Plasser', 'Event Trenger Registrering', 'Eventstart', 'Eventslutt', 'Event Trenger Feedback', 'Eventpris Medlemmer', 'Eventpris Gjester')
        for event in events:
            p.row(
                event.id,
                event.name,
                format_event_type(event.type),
                event.intro,
                event.location,
                event.capacity if event.capacity > 0 else 'Ubegrenset',
                event.is_registration_required,
                event.start_date,
                event.end_date,
                event.feedback_when_registering,
                event.price_members,
                event.price_guests
            )

    def _gen_brukergrupper(self, p):
        groups = self.session.query(Group)\
            .filter(Group.deleted == False)
        p.row('Gruppe ID', 'Gruppenavn', 'Gruppe Er Komite')
        for group in groups:
            p.row(
                group.id,
                group.name,
                group.is_committee
            )

    def _gen_medlemskap(self, p):
        p.row('Bruker ID', 'Gruppe ID')
        for m in self.session.query(Membership):
            p.row(
                m.user_id,
                m.group_id
            )
    def _gen_eventregistrering(self, p):
        reg = self.session.query(EventRegistration)\
            .filter(EventRegistration.deleted == False)

        status = {
            1 : 'Påmeldt',
            2 : 'Uregistrert',
            3 : 'Fest',
            4 : 'Annet'
        }
        presence = {
            0 : 'Uvisst',
            1 : 'Tilstede',
            2 : 'Ikke tilstede',
            3 : 'Uvisst'
        }

        p.row('Eventregistrering ID', 'Bruker ID', 'Event ID', 'Eventregistrering Dato', 'Eventregistrering Status', 'Eventregistrering Tilstedeværelse')

        for r in reg:
            p.row(
                r.id,
                r.user_id,
                r.event_id,
                r.date,
                status[r.status],
                presence[r.presence]
            )


class Printer:
    file = None
    def __init__(self, filename):
        try:
            os.makedirs(settings.OUT_DIR)
        except: pass
        self.file = open(settings.OUT_DIR + filename, 'w+')

    def clean_value(self, val):
        if isinstance(val, str):
            return val.replace('\n', ' ').replace('\r', ' ').replace('|', '')
        elif isinstance(val, bool):
            return 'Ja' if val else 'Nei'
        elif type(val) is datetime.datetime:
            return val.strftime('%Y-%m-%d %H:%M')
        return val

    def row(self, *args):
        values = map(self.clean_value, args)
        self.file.write('|'.join([str(element) for element in values]))
        self.file.write('\n')

