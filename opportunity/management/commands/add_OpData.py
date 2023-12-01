import re
import time
import logging
import pandas as pd

from pathlib import Path
from datetime import datetime
#from smbclient import open_file, register_session, ClientConfig
from sqlalchemy import create_engine
from django.core.management.base import BaseCommand,CommandError
from opportunity.models import opportunity
from django.conf import settings


#for logging
logging.basicConfig(filename="log/opmanagecli.log",level=logging.DEBUG , format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

#SFA CSVFile path 
SFAFile = '/home/tank/export_anken.csv'
#Target File for writing the last update time of the database.
TempFileWritedUpdateTime = (Path(__file__).resolve().parent.parent.parent).joinpath('templates/op','LastUpdateTime.html')
#Japanese header names to be included database in original csv file.
OriginHeader = ['案件情報ID','案件名','当社担当者','顧客名','受注予定日','売上予定日[1]','発生日','作成日','作成者','更新日','更新者','案件分類・種別']
#The database fields name changed from the original csv header fields
ChangedHeader = ['CaseID','CaseName','Representative','CustomerName','ExpectedOrderDate','ExpectedRevenueDate','OccurDate','CreatedDate','Creator','UpdatedDate','Updater','Category']
#The fields name datetype
FieldofDate = ['受注予定日','売上予定日[1]','発生日','作成日','更新日']

def check_file_update(input_file,timestamp_file):
    """
    概要:ファイルがUpdateされたか確認する
    詳細説明:input_fileの変更時間とtimespam_fileの中に書かれた時間を比較する
    Args:
        input_file(string): 読み込むファイルのpath
        timestamp_file(string): 前回読み込まれたファイルの変更時間がかかれたファイルのpath
    Returns:
        Bloolean: 
            True:input_file変更時間が新しい
            False:input_file変更時間が新しくないかtimestamp_fileに時間情報がない
    Raises:
        CommandError:ファイルが存在しないかその他の不正
    """
    i_file = Path(input_file)
    t_file = Path(timestamp_file)
    
    if i_file.exists() and t_file.exists():
        i_mtime = i_file.stat().st_mtime
        i_mtime = (datetime.fromtimestamp(i_mtime)).replace(microsecond=0)
        with open(timestamp_file, 'r') as f:
            match = re.search(r'Last updated : (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', f.read())
            if match is not None:
                previous_mtime = match.group(1)
                previous_mtime = datetime.strptime(previous_mtime, '%Y-%m-%d %H:%M:%S')
            else:
                previous_mtime = None
            #print('i_mtime: {}={}'.format(i_mtime,type(i_mtime)))
            #print('previous_mtime: {}={}'.format(previous_mtime,type(previous_mtime)))
            if i_mtime > previous_mtime:
                return True
            else:
                logging.warning('File is not Updated : {} mtime={} , {} timestamp={}'.format(input_file,i_mtime,timestamp_file,previous_mtime))
                return False
    else:
        logger.error('File not found : {} or {}'.format(input_file, timestamp_file))
        raise CommandError('File not found : {} or {}'.format(input_file, timestamp_file))

def write_time_to_tempelte(time, output_file):
    """
    概要:時刻をファイルに出力
    詳細説明:timeの値をoutput_fileにhtml形式で書き込む
    Args:
        time(string): %Y-%m-%d %H:%M:%Sフォーマット時間
        output_file(string): timeを書き込むファイルのpath
    Returns:
        None:   
    """
    str = "\t<span class=\"badge bg-warning text-dark fs-6\"> Last updated : {} </span>".format(time) 
    with open(output_file, mode='w+',encoding='utf-8') as f:
        f.write(str)
            
class Command(BaseCommand):
    help = 'The command to overwrite data from an sfa csv file to the table of oppartunity model'

    def handle(self, *args, **options):
    
        ##Step1 :Convert the csv file to pandas dataframe
        #Convert the csv file to pandas dataframe with the fields name for including database and change to data type for date fields. 
        if check_file_update(SFAFile, TempFileWritedUpdateTime):
            try:
                df = pd.read_csv(SFAFile, sep=",",encoding="cp932",usecols=OriginHeader,parse_dates=FieldofDate,na_filter=False)
            except:
                msg='Error converting csv file to dataframe.'
                logging.error(msg)
                raise CommandError(msg)
        else:
            msg='Please check file updating : {}.'.format(SFAFile)
            logging.info(msg)
            raise CommandError(msg)

        #Change field name from japanese to english
        MappedHeader = dict(zip(OriginHeader,ChangedHeader))
        
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

        ##Step2 :Input the dataframe's data to Model's database by converting dataframe to sql.
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
                print("Database updating Success")
                logging.info('Success converting dataframe to sql.')
                logging.info('Process for dataframe to sql took {mt} seconds.'.format(mt=end_time - start_time))
    
                #Recode data updated time to Templates file
                m_timestamp = Path(SFAFile).stat().st_mtime
                m_time = datetime.fromtimestamp(m_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                try:
                    write_time_to_tempelte(m_time, TempFileWritedUpdateTime)
                except:
                    msg='Failed to write LastUpdateTime.html file.'
                    logging.error(msg)
                else:
                    msg='Success writing Update time : {} to LastUpdateTime.html.'.format(m_time)
                    logging.info(msg)
                    #delete the csv file inputed data to table
                    #Path(SFAFile).unlink
                     

     
 
        

            
        
