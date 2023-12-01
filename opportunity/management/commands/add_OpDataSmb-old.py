import io
import time
import logging
import pandas as pd

from pathlib import Path
from datetime import datetime
#from smbclient import open_file, register_session, ClientConfig
from sqlalchemy import create_engine
#from os import environ
from django.core.management.base import BaseCommand,CommandError
from opportunity.models import opportunity
from django.conf import settings


#for logging
logging.basicConfig(filename="opmanagecli.log",level=logging.DEBUG , format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


#SMB server informations
#SMBSev = '\\\\172.17.0.115\\Tank\\80_システム連携DATA\\'
SFAFile = '/home/tank/export_anken.csv'
#CurrentDateHour = datetime.now().strftime("%Y%m%d%H")
#SFAFile = "export_anken_{}.csv".format(CurrentDateHour)
#SMBUserID = ''
#SMBUserPW = ''


class Command(BaseCommand):
    help = 'A command to add data from an csv file in smb server to the database of model'

    def handle(self, *args, **options):
        
        ##Step1 :Connect to smb server and load the csv file.
        #Config user information for smbserver.
        #ClientConfig(username=SMBUserID, password=SMBUserPW)
        #loading the csv file from smb server
        """
        try:
            with open_file(r"SMBSev + SFAFile" , encoding="cp932") as fd:
        #    with open_file(r"\\172.17.0.115\Tank\80_システム連携DATA\export_anken_20230829172.csv" , encoding="cp932") as fd:
                CsvContents = fd.read()
        except:
            msg='Error opening file of SMB connection:'
            logging.error(msg)
            raise CommandError(msg)
        """
        ##Step2 :Convert the csv file to pandas dataframe
        #Japanese header names to be included database in original csv file.
        OriginHeader = ['案件情報ID','案件名','当社担当者','顧客名','受注予定日','売上予定日[1]','発生日','作成日','作成者','更新日','更新者','案件分類・種別']
        #The database fields name changed from the original csv header fields
        ChangedHeader = ['CaseID','CaseName','Representative','CustomerName','ExpectedOrderDate','ExpectedRevenueDate','OccurDate','CreatedDate','Creator','UpdatedDate','Updater','Category']
        MappedHeader = dict(zip(OriginHeader,ChangedHeader))
        FieldofDate = ['受注予定日','売上予定日[1]','発生日','作成日','更新日']
        #Convert the csv file to pandas dataframe with the fields name for including database and change to data type for date fields. 
        try:
        #    df = pd.read_csv(io.StringIO(CsvContents), sep=",",encoding="cp932",usecols=OriginHeader,parse_dates=FieldofDate)
            df = pd.read_csv(SFAFile, sep=",",encoding="cp932",usecols=OriginHeader,parse_dates=FieldofDate,na_filter=False)
        except:
            msg='Error converting csv file to dataframe.'
            logging.error(msg)
            raise CommandError(msg)
        
        # for confirming data type of convertied csv file to pandas dataframe
        c  = 0
        for i in OriginHeader:
            print("{}: {} : {}".format(c, i, df[i].dtype))
            c += 1
            
        #Change field name from japanese to english
        try:
            df = df.rename(columns=MappedHeader)
        except:
            msg='Error changing field name from japanese to english.'
            logging.error(msg)
            raise CommandError(msg)

        #Set Index field to be CaseID
        try:
            df.set_index("CaseID", inplace=True)
        except:
            msg='Error setting index field to be CaseID.'
            logging.error(msg)
            raise CommandError(msg)

        ##Step3 :Input the dataframe's data to Model's database by converting dataframe to sql.
        #Use settings.py for database connection information.
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
                df.to_sql(opportunity._meta.db_table,if_exists='replace',con=engine,index_label="CaseID")
            except:
                print("Error")
                try:
                    tran.rollback()
                except:
                    msg='Error converting dataframe to sql and Failed to rollback'
                    logging.error(msg)
                    raise CommandError(msg)
                msg='Error converting dataframe to sql.'
                raise CommandError(msg)
            else:
                end_time = time.time()
                print("Success")
                logging.info('Success converting dataframe to sql.')
                logging.info('Process for dataframe to sql took {mt} seconds.'.format(mt=end_time - start_time))
    
                #Recode data updated time to os.environ variable
                #try:
                #    environ['add_opdatasmbExecuteTime'] = CurrentDateHour
                #except:
                #    logging.error('Error recoding update time to add_opdatasmb_executime of os.eviron')
                #else:
                #    logging.info('Recoded update time:{}'.format(environ['add_opdatasmb_executime']))
     
 
        

            
        
