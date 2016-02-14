import argparse
import settings

from session import get_session
from tablegenerator import TableGenerator

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--table',  help='Name of the table to generate')
parser.add_argument('-c', '--connection_string', help='Database connection string',
                    default = settings.DEFAULT_CONNECTION_STRING)

if __name__ == '__main__':
    args = parser.parse_args()
    session = get_session(args.connection_string)
    gen = TableGenerator(session)
    gen.generate_tables(args.table)
