import io
import time
import logging
import pandas as pd

from django.core.management.base import BaseCommand,CommandError
from book.models import Book
from sqlalchemy import create_engine
from django.conf import settings
from os import environ
from datetime import datetime

#for logging
logging.basicConfig(filename="log/bookmanagecli.log",level=logging.DEBUG , format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'A command to add data from an excel file to the database'
    
    
    def handle(self, *args, **options):
        excel_file ='book/inputdata/books.csv'
        Headers = ['No','title','category','author','published_date','price','stock']
        df = pd.read_csv(excel_file,usecols=Headers,encoding='cp932',parse_dates=['published_date'],na_filter=False)
        print(df)

        try:
            df.set_index("No", inplace=True)
        except:
            msg='Error setting index field to be No.'
            logging.error(msg)
            raise CommandError(msg)
        
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@127.0.0.1:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )
        #Information of the database to be connected.
        engine = create_engine(database_url, echo=False)

        #Connect to the database and Input the data converted dataframe to the table created.
        start_time = time.time()
        with engine.connect() as conn:
            tran = conn.begin()
            try:
                df.to_sql(Book._meta.db_table,if_exists='replace',con=engine,index_label="No")
                print("Success")
                logging.info('Success converting dataframe to sql.')
                #Recode data updated time to os.environ variable
                try:
                    environ['add_bookdatasmb_executime'] = datetime.now().strftime("%Y%m%d%H")
                except:
                    logging.error('Error recoding update time to add_bookdatasmb_executime of os.eviron')
                else:
                    logging.info('Recoded update time:{}'.format(environ['add_bookdatasmb_executime']))
            except:
                print("Error")
                tran.rollback()
                logging.error('Error converting dataframe to sql.')
        end_time = time.time()
        logging.info('Process for dataframe to sql took {mt} seconds.'.format(mt=end_time - start_time))