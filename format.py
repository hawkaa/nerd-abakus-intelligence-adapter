EVENT_MAPPINGS = {
    'Course' : 'Kurs',
    'Company presentation' : 'Bedpres',
    'Party' : 'Fest',
    'Other' : 'Annet',
    'Special' : 'Spesiell'
}

def format_event_type(e):
    if e.name in EVENT_MAPPINGS: return EVENT_MAPPINGS[e.name]
    else: return 'Ukjent'

def format_boolean(b):
    return 'Ja' if b else 'Nei'

