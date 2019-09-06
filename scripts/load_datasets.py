import argparse
import csv
from models import Marketing, Users, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util import find_files


def ingest_marketing_data(file, engine, session):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=None)
        for row in reader:
            session.add(
                Marketing(
                    event_id=row['event_id'],
                    phone_id=row['phone_id'],
                    ad_id=row['ad_id'],
                    provider=row['provider'],
                    placement=row['placement'],
                    length=row['length'],
                    event_ts=row['event_ts']
                )
            )


def ingest_user_data(file, engine, session):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=None)
        for row in reader:
            session.add(
                Users(
                    event_id=row['event_id'],
                    user_id=row['user_id'],
                    phone_id=row['phone_id'],
                    property=row['property'],
                    value=row['value'],
                    event_ts=row['event_ts']
                )
            )


parser = argparse.ArgumentParser(description='Ingest Sample Datasets')
parser.add_argument('--user', required=True)
parser.add_argument('--pwd', required=True)
parser.add_argument('--host', required=False, default='localhost')
parser.add_argument('--port', required=False, default=5432)
parser.add_argument('--db', required=False, default='postgres')
parser.add_argument('--input-file-dir', required=True)


if __name__ == '__main__':
    args = parser.parse_args()
    engine = create_engine(
        "postgresql://{user}:{pwd}@{host}:{port}/{db}"
        .format(user=args.user, pwd=args.pwd, host=args.host, port=args.port, db=args.db)
    )

    files_to_load = find_files(args.input_file_dir)

    marketing_files = [args.input_file_dir + '/' + file for file in files_to_load if 'marketing' in file]
    user_files = [args.input_file_dir + '/' + file for file in files_to_load if 'user' in file]

    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine, checkfirst=True)

    for file in marketing_files:
        print('Ingesting {}'.format(file))
        ingest_marketing_data(file, engine, session)
        session.commit()

    for file in user_files:
        print('Ingesting {}'.format(file))
        ingest_user_data(file, engine, session)
        session.commit()
