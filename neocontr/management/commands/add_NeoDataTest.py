import io
import time
import logging
import pandas as pd

from datetime import datetime
from smbclient import open_file, register_session, ClientConfig
from sqlalchemy import create_engine

from django.core.management.base import BaseCommand,CommandError
from neocontr.models import NeoContract
from django.conf import settings


#for logging
logging.basicConfig(filename="ctmanagecli.log",level=logging.DEBUG , format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

#SMB server informations
SMBSev = '\\\\172.17.0.115\\Tank\\80_システム連携DATA\\'
ContrFile = 'znw_contract_list.csv'
#SFAFile = "export_anken_{}.csv".format(datetime.now().strftime("%Y%m%d%H"))
SMBUserID = 'joonhak'
SMBUserPW = 'imj00nhak'
#print(SMBSev + ContrFile)
class Command(BaseCommand):
    help = 'A command to add data from an csv file in smb server to the database of model'

    def handle(self, *args, **options):
        
        ##Step1 :Connect to smb server and load the csv file.
        #Config user information for smbserver.
        ClientConfig(username=SMBUserID, password=SMBUserPW)
        #loading the csv file from smb server
        """
        try:
            with open_file(r"SMBSev + ContrFile" , encoding="cp932") as fd:
        #    with open_file(r"\\172.17.0.115\Tank\80_システム連携DATA\znw_contract_list.csv" , encoding="cp932") as fd:
                CsvContents = fd.read()
        except:
            msg='Error opening file of SMB connection:'
            logging.error(msg)
            raise CommandError(msg)
        """
        ##Step2 :Convert the csv file to pandas dataframe
        #Japanese header names to be included database in original csv file.
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
        MappedHeader = dict(zip(OriginHeader,ChangedHeader))
        FieldofDate = ['受注日付', '本体出荷日', '保守開始日', '保守終了日', 'ExpDate', '発注書作成日', '入荷日', '出荷日', '納品日', '案内書作成日', '依頼書作成日', '売上月', '請求書作成日', '入金予定日']
      
        
        
        
        #def strip_spaces(a_str_with_spaces):
        #    return a_str_with_spaces.replace(' ', '')

        #Convert the csv file to pandas dataframe with the fields name for including database and change to data type for date fields. 
        try:
        #    df = pd.read_csv(io.StringIO(CsvContents), sep=",",encoding="cp932",usecols=OriginHeader,parse_dates=FieldofDate)
        #    df = pd.read_csv("znw_contract_list.csv", sep=",",encoding="cp932",usecols=OriginHeader,parse_dates=FieldofDate,na_filter=False,converters={'受注枝番': strip_spaces,'サブキー番号':strip_spaces})
             df = pd.read_csv("znw_contract_list.csv", sep=",",encoding="cp932",usecols=OriginHeader,parse_dates=FieldofDate,na_filter=False)

        except:
            msg='Error converting csv file to dataframe.'
            logging.error(msg)
            raise CommandError(msg)
        # for confirming data type of convertied csv file to pandas dataframe
        #Change field name from japanese to english
        try:
            df = df.rename(columns=MappedHeader)
        except:
            msg='Error changing field name from japanese to english.'
            logging.error(msg)
            raise CommandError(msg)
        ###Confirming data type of convertied csv file to pandas dataframe
        
                ##List分解
        #受注情報
        OrderInfo = ['受注日付','受注番号', '受注枝番', '客先注文番号', '当社担当者', '受注品番', '受注品名', '受注単価', '受注備考', '仮受注','キャンセルフラグ',
                      '売上月', '請求書作成日', '入金予定日','見積番号', '登録備考']



        #出荷情報
        ShipInfo = ['SID', '本体グループＩＤ', 'TELキー番号','サブキー番号', 'CID', '本体SN', '本体出荷時Ver', '本体出荷日', '本体フラグ', '本体交換履歴', '仕入番号', '仕入枝番', '仕入品番', 'ContractNo', 
                    'ExpDate', '発注書作成日', '入荷日', '出荷日', '納品日','ST(PartNo)']
        
        #契約情報
        ContractInfo = ['保守開始日', '保守終了日', '更新フラグ', '販売状態', '案内書作成日', '依頼書作成日','機種名', '商品区分コード', '商品分類記号', '保守種別', 'ライセンス期間', 'ノーティス品番', 'ノーティス品名',
                        '直サポートフラグ', '本体受注番号', '本体受注品番', '本体発注品番', 'IP Address', '保守備考', 'FortiCare種別']
            
        #発注元情報
        PurchaserInfo =['発注元コード','発注元会社名']
            
        #納入先情報
        DeliveryInfo = ['納品先コード', '納品先会社名', '納品先部署名', '納品先担当者', '納品先TEL', '納品先〒', '納品先住所']
        
        #請求先情報
        BillingInfo = ['請求先コード', '請求先会社名','請求先部署名', '請求先担当者', '請求先TEL', '請求先〒', '請求先住所']
        
        #エンドユーザー情報
        EnduserInfo = ['EUコード', 'EU営業配信', 'EU技術配信', 'EU会社名', 'EU部署名', 'EU担当者名', 'EUメールアドレス' ]
        
        #リセラー情報
        ResellerInfo = ['リセラーコード', 'リセラー営業配信', 'リセラー技術配信', 'リセラー会社名', 'リセラー部署名', 'リセラー担当者名', 'リセラーメールアドレス']
     
        #設置先情報
        InstLocationInfo = ['設置先コード', '設置先会社名', '設置先部署名','設置先担当者名', '設置先メールアドレス', '設置先TEL', '設置先〒', '設置先住所']

        #保守案内先情報
        SuportInfo = ['保守案内先コード', '保守案内先会社名', '保守案内先部署名', '保守案内先担当者名', '保守案内先メールアドレス', '保守案内先TEL', '保守案内先〒', '保守案内先住所']
        
        Items ={'受注情報':OrderInfo,'出荷情報':ShipInfo,'契約情報':ContractInfo,'発注元情報':PurchaserInfo,'納入先情報':DeliveryInfo,'請求先情報':BillingInfo,'エンドユーザー情報':EnduserInfo,'リセラー情報':ResellerInfo,'設置先情報':InstLocationInfo,'保守案内先情報':SuportInfo}
        for k,v in Items.items():
            print("<!--###{}###-->".format(k))
            for key in v:
                print("<tr>")
                print("\t<th class=\"col-1 table-primary\">{}</th>".format(key))
                if df[MappedHeader[key]].dtype == 'datetime64[ns]':
                    print("\t<td class=\"col-5\">{{{{ ctdetail.{}|date:\"Y-n-j\" }}}}</td>".format(MappedHeader[key]))
                else:
                    print("\t<td class=\"col-5\">{{{{ ctdetail.{}|default_if_none:\"\"}}}}</td>".format(MappedHeader[key]))
                print("</tr>")
        print("########################################################################")
        
"""
        c  = 0
        for i in ChangedHeader:
            if df[i].dtype != 'object':
                print("{}: {} : {}".format(c, i, df[i].dtype))
                c += 1
            else:
                    print("**{}: {} : {}".format(c, i, df[i].dtype))
            c += 1
            
        #Set Index field to be ExtID
        try:
            df.set_index("ExtID", inplace=True)
        except:
            msg='Error setting index field to be CaseID.'
            logging.error(msg)
            raise CommandError(msg)
      
        ##Step3 :Input the dataframe's data to Model's database by converting dataframe to sql.
        #Useing settings.py for database connection information.
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@db:5432/{database_name}'.format(
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
                df.to_sql(NeoContract._meta.db_table,if_exists='replace',con=engine,index_label="ExtID")
                print("Success")
                logging.info('Success converting dataframe to sql.')
            except:
                print("Error")
                tran.rollback()
                logging.error('Error converting dataframe to sql.')
        end_time = time.time()
        logging.info('Process for dataframe to sql took {mt} seconds.'.format(mt=end_time - start_time))

"""