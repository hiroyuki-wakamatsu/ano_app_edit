import re
import time
import logging
import pandas as pd

from pathlib import Path
from datetime import datetime
#from smbclient import open_file, register_session, ClientConfig
from sqlalchemy import create_engine
from django.core.management.base import BaseCommand,CommandError
from neocontr.models import NeoContract
from django.conf import settings


#for logging
logging.basicConfig(filename="log/ctmanagecli.log",level=logging.DEBUG , format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

#NEO CSVFile path 
NeoContrFile = '/home/tank/znw_contract_list.csv'
#Target File for writing the last update time of the database.
TempFileWritedUpdateTime = (Path(__file__).resolve().parent.parent.parent).joinpath('templates/ct','LastUpdateTime.html')

#Japanese header names to be included database in original neocsv file.
OriginHeader = ['外部ＩＤ', '受注日付','受注番号', '受注枝番', '客先注文番号', '当社担当者', '受注品番', '受注品名', '受注単価', '受注備考', 'SID', '本体グループＩＤ', 'TELキー番号',
                'サブキー番号', 'CID', '本体SN', '本体出荷時Ver', '本体出荷日', '本体フラグ', '本体交換履歴', '保守開始日', '保守終了日', '更新フラグ', '販売状態', '仮受注',
                'キャンセルフラグ', '仕入番号', '仕入枝番', '仕入品番', 'ContractNo', 'ExpDate', '発注書作成日', '入荷日', '出荷日', '納品日', '案内書作成日', '依頼書作成日',
                '売上月', '請求書作成日', '入金予定日', '機種名', '商品区分コード', '商品分類記号', '保守種別', 'ライセンス期間', 'ノーティス品番', 'ノーティス品名', '発注元コード',
                '発注元会社名', '納品先コード', '納品先会社名', '納品先部署名', '納品先担当者', '納品先TEL', '納品先〒', '納品先住所', '請求先コード', '請求先会社名',
                '請求先部署名', '請求先担当者', '請求先TEL', '請求先〒', '請求先住所', 'EUコード', 'EU営業配信', 'EU技術配信', 'EU会社名', 'EU部署名', 'EU担当者名', 'EUメールアドレス', 
                'リセラーコード', 'リセラー営業配信', 'リセラー技術配信', 'リセラー会社名', 'リセラー部署名', 'リセラー担当者名', 'リセラーメールアドレス', '設置先コード', '設置先会社名', '設置先部署名',
                '設置先担当者名', '設置先メールアドレス', '設置先TEL', '設置先〒', '設置先住所', '保守案内先コード', '保守案内先会社名', '保守案内先部署名', '保守案内先担当者名', 
                '保守案内先メールアドレス', '保守案内先TEL', '保守案内先〒', '保守案内先住所', '直サポートフラグ', '本体受注番号', '本体受注品番', '本体発注品番', 'IP Address', 
                'ST(PartNo)', '見積番号', '登録備考', '保守備考', 'FortiCare種別']
        
#The database fields name changed from the original csv header fields
ChangedHeader = ['ExtID', 'OrdDe', 'OrdNo', 'OrdBrNo', 'CustPoNo', 'OurRep', 'OrdProdNo', 'OrdProdName', 'OrdUnitPrice', 'OrdRemarks', 'SIdn', 
                 'MainUnitGrID', 'TELKeyNo', 'SubKeyNo', 'CID', 'MainUnitSN', 'MainUnitShipVer', 'MainUnitShipDe', 'MainUnitFlag', 'MainUnitExcHist',
                 'MaintStartDe', 'MaintEndDe', 'UpdateFlag', 'SalStatus', 'ProvisionalOrd', 'CancelFlag', 'PoNo', 'PoBranchNo', 'PoProdNo', 'ContNo', 
                 'ExpDe', 'PoCreatDe', 'ArrivalDe', 'ShipDe', 'DelivDe', 'GuidebookCreatDe', 'ReqFormCreatDe', 'SalesMonth', 'InvoiceCreatDe', 'ExpectedPayDe', 
                 'ModelName', 'ProdClassCode', 'ProdClassSymbol', 'MaintType', 'LicensePeriod', 'NoticeProdNo', 'NoticeProdName', 'OrdCode', 'OrdCoName', 'DelDestCode', 
                 'DelDestCoName', 'DelDestDtName', 'DelDestPic', 'DelDestTEL', 'DelDestPostalCode', 'DelDestAdd', 'BillDestCode', 'BillDestCoName', 'BillDestDtName', 
                 'BillDestPic', 'BillDestTEL', 'BillDestPostalCode', 'BillDestAdd', 'EUCode', 'EUSalesDist', 'EUTechDist', 'EUCoName', 'EUDtName', 'EUContName',
                 'EUEmailAdd', 'ResellerCode', 'ResellerSalesDist', 'ResellerTechDist', 'ResellerCoName', 'ResellerDtName', 'ResellerContName', 'ResellerEmailAdd',
                 'InstCode', 'InstCoName', 'InstDtName', 'InstContName', 'InstEmailAdd', 'InstTEL', 'InstPostalCode', 'InstAdd', 'MaintInfoCode', 'MaintInfoCoName', 
                 'MaintInfoDtName', 'MaintInfoContName', 'MaintInfoEmailAdd', 'MaintInfoTEL', 'MaintInfoPostalCode', 'MaintInfoAdd', 'DirectSupportFlag', 'MainUnitOrdNo',
                 'MainUnitOrdProdNo', 'MainUnitPoProdNo', 'IPAdd', 'StPartNo', 'EstimateNo', 'RegRemarks', 'MaintRemarks', 'FortiCareType']

#The Field having value ="string" should remove =""
NeedCleanDataField = ['受注番号','客先注文番号','受注品番','本体SN','仕入品番','本体交換履歴','ContractNo']
#The fields datetype
FieldofDate = ['受注日付', '本体出荷日', '保守開始日', '保守終了日', 'ExpDate', '発注書作成日', '入荷日', '出荷日', '納品日', '案内書作成日', '依頼書作成日', '売上月', '請求書作成日', '入金予定日']
        
def check_file_update(input_file,timestamp_file):
    """
    概要:ファイルがUpdateされたか確認する。
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
    help = 'The command to overwrite from a neo contract csv file to the table of NEO Contract model'

    def handle(self, *args, **options):
        
        ##Step1 :Convert the neo csv file to pandas dataframe
        #Convert the csv file to pandas dataframe with the fields name for including database and change to data type for date fields. 
        if check_file_update(NeoContrFile, TempFileWritedUpdateTime):
            try:
                df = pd.read_csv(NeoContrFile, sep=",",encoding="cp932",usecols=OriginHeader,parse_dates=FieldofDate,na_filter=False)
            except:
                msg='Error converting csv file to dataframe.'
                logging.error(msg)
                raise CommandError(msg)
        else:
            msg='Please check file updating : {}.'.format(NeoContrFile)
            logging.info(msg)
            raise CommandError(msg)
    
        #Remove ="" from ="string" cell to string cell
        for i in NeedCleanDataField:
            df[i] = df[i].replace(r'="(.*)"', r'\1', regex=True)
                  
        #Change field name from japanese to english
        MappedHeader = dict(zip(OriginHeader,ChangedHeader))
        try:
            df = df.rename(columns=MappedHeader)
        except:
            msg='Error changing field name from japanese to english.'
            logging.error(msg)
            raise CommandError(msg)
        
        #Set Index field to be ExtID
        try:
            df.set_index("ExtID", inplace=True)
        except:
            msg='Error setting index field to be CaseID.'
            logging.error(msg)
            raise CommandError(msg)
                
        
        ##Step2 :Input the dataframe's data to Model's database by converting dataframe to sql.
        #Useing settings.py for database connection information.
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
                df.to_sql(NeoContract._meta.db_table,if_exists='replace',con=engine,index_label="ExtID",chunksize=1000)
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
                print('Process for dataframe to sql took {mt} seconds.'.format(mt=end_time - start_time))
                logging.info('Success converting dataframe to sql.')
                logging.info('Process for dataframe to sql took {mt} seconds.'.format(mt=end_time - start_time))
    
                #Recode data updated time to Templates file
                m_timestamp = Path(NeoContrFile).stat().st_mtime
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
                    #Path(NeoContrFile).unlink