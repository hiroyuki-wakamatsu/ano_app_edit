import os
import sys
import unicodedata

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

from ftnapp.models import FtnQuoteHeader

#ハンコ作成用
from commonapp.views import get_quote_info_by_id
from commonapp.views import HankoGenerator


# 定数モジュールをインポート
# import estimatepdf_const as const
from . import estimatepdf_const as const

# Public関数
# 機能：半角単位で何文字分か調べて返却する(半角を1文字、全角を2文字とする)
# 引数：引数1->text(文字列)
def countLength(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    return count


# Public関数
# 機能：半角単位で指定した文字数で文字列を分割。タプル型で返却
# 引数：引数1->text(文字列) 引数2->splitLen(分割する文字数)
# 使用例:3文字毎に分割する場合
#         splitStr("12312312", 3)
#           -> retuen ['123', '123','12']
def splitStr(text, splitLen):
    strlists = []
    count = 0
    pstr = ""
    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            if (count + 2) > splitLen:
                strlists.append(pstr)
                pstr = ""
                count = 0
            pstr += c
            count += 2
        else:
            pstr += c
            count += 1
        if count >= splitLen:
            strlists.append(pstr)
            pstr = ""
            count = 0
    if pstr != "":
        strlists.append(pstr)
    return strlists


# クラス
# 機能：見積りフォームの結果をPDFとして出力する
# 引数：引数1->filename(PDFファイル名)
class MakeEstimatePdf:
    """
    クラス名:MakeEstimatePdf
    説明:見積りフォームの結果をPDFとして出力する
    引数説明:
      引数1:filename(PDFファイル名)
    """

    # private変数設定 START -----------------------------------------------------------
    # 補足：「estimatepdf_const」モジュールの定数を使用

    # 会社情報
    COMPANY_NAME = const.COMPANY_NAME
    COMPANY_ADDRESS = const.COMPANY_ADDRESS
    COMPANY_TEL = const.COMPANY_TEL
    COMPANY_FAX = const.COMPANY_FAX

    # デフォルトのフォントを宣言
    FONT_DEFAULT_NAME = const.FONT_DEFAULT_NAME
    FONT_DEFAULT_PATH = const.FONT_DEFAULT_PATH

    # 基準となるグリッドの縦横を格納
    GRID_Y = const.GRID_Y
    GRID_X = const.GRID_X

    # コンテンツを表示できる一番下のY座標
    END_Y = const.END_Y
    # コンテンツ表示でリセットするY座標
    TOP_Y = const.TOP_Y
    # コンテンツテーブル左右のX座標
    LEFT_X = const.LEFT_X
    RIGHT_X = const.RIGHT_X

    # コンテンツテーブル縦線の区切り位置のX座標
    VERTICAL_X1 = const.VERTICAL_X1
    VERTICAL_X2 = const.VERTICAL_X2
    VERTICAL_X3 = const.VERTICAL_X3
    VERTICAL_X4 = const.VERTICAL_X4
    VERTICAL_X5 = const.VERTICAL_X5
    VERTICAL_X6 = const.VERTICAL_X6
    VERTICAL_X7 = const.VERTICAL_X7
    VERTICAL_X8 = const.VERTICAL_X8
    # コンテンツの表示パディング
    PADDING_BOTTOM = const.PADDING_BOTTOM

    # 描画座標位置
    # ヘッダータイトル座標
    HEADER_TITLE_X = const.HEADER_TITLE_X
    HEADER_TITLE_Y = const.HEADER_TITLE_Y
    # ヘッダーお客様名座標
    HEADER_CLIENT_X = const.HEADER_CLIENT_X
    HEADER_CLIENT_Y = const.HEADER_CLIENT_Y
    # ヘッダー見積番号座標
    HEADER_ESTIMATE_NUM_X = const.HEADER_ESTIMATE_NUM_X
    HEADER_ESTIMATE_NUM_Y = const.HEADER_ESTIMATE_NUM_Y
    # ヘッダーZNW情報座標
    HEADER_ZNW_INFO_X = const.HEADER_ZNW_INFO_X
    HEADER_ZNW_INFO_Y = const.HEADER_ZNW_INFO_Y
    # ヘッダーZNW会社印枠座標
    HEADER_ZNW_SEAL_FLAME_X = const.HEADER_ZNW_SEAL_FLAME_X
    HEADER_ZNW_SEAL_FLAME_Y = const.HEADER_ZNW_SEAL_FLAME_Y
    # ヘッダーZNW会社印座標
    HEADER_ZNW_SEAL_X = const.HEADER_ZNW_SEAL_X
    HEADER_ZNW_SEAL_Y = const.HEADER_ZNW_SEAL_Y
    # ヘッダーZNW職印座標
    HEADER_EMPLOYEE_SEAL_X = const.HEADER_EMPLOYEE_SEAL_X
    HEADER_EMPLOYEE_SEAL_Y = const.HEADER_EMPLOYEE_SEAL_Y

    # 本見積コンテンツ座標
    FINAL_ESTIMATE_BODY_X = const.FINAL_ESTIMATE_BODY_X
    FINAL_ESTIMATE_BODY_Y = const.FINAL_ESTIMATE_BODY_Y

    # テーブル改行閾値(半角文字何個分)
    MAX_ZNW_SKU_JP = const.MAX_ZNW_SKU_JP  # 品名の改行文字数の閾値
    MAX_ZNW_SKU = const.MAX_ZNW_SKU  # 型番の改行文字数の閾値
    MAX_ANNO_DATA = const.MAX_ANNO_DATA  # 注釈の改行文字数の閾値

    # フッター文字改行の閾値
    MAX_FOOTER_SENTENCE_SIZE = const.MAX_FOOTER_SENTENCE_SIZE

    # 会社印のパス
    COMPANY_SEAL = const.COMPANY_SEAL

    # ドラフト文字列イメージ
    DRAFT_IMG = const.DRAFT_IMG

    # フッター固定文言1
    FOOTER_FIX_SENTENCE1 = const.FOOTER_FIX_SENTENCE1
    # フッター固定文言2
    FOOTER_FIX_SENTENCE2 = const.FOOTER_FIX_SENTENCE2
    # フッター固定文言3
    FOOTER_FIX_SENTENCE3 = const.FOOTER_FIX_SENTENCE3

    # フッター可変文言_通常
    FOOTER_VAL_SENTENCE1_NORMAL = const.FOOTER_VAL_SENTENCE1_NORMAL
    FOOTER_VAL_SENTENCE2_NORMAL = const.FOOTER_VAL_SENTENCE2_NORMAL

    # フッター可変文言_保守用
    FOOTER_VAL_SENTENCE1_HOSYU = const.FOOTER_VAL_SENTENCE1_HOSYU
    FOOTER_VAL_SENTENCE2_HOSYU = const.FOOTER_VAL_SENTENCE2_HOSYU
    FOOTER_VAL_SENTENCE3_HOSYU = const.FOOTER_VAL_SENTENCE3_HOSYU
    FOOTER_VAL_SENTENCE4_HOSYU = const.FOOTER_VAL_SENTENCE4_HOSYU
    FOOTER_VAL_SENTENCE5_HOSYU = const.FOOTER_VAL_SENTENCE5_HOSYU

    # private変数設定 END -----------------------------------------------------------

    # コンストラクタ
    def __init__(self, filename):
        self.pdf = canvas.Canvas(filename)
        pdfmetrics.registerFont(TTFont(self.FONT_DEFAULT_NAME, self.FONT_DEFAULT_PATH))
        self.font = self.FONT_DEFAULT_NAME
        # 描画した位置座標をインデックスとして保持
        self.index_x = 0
        self.index_y = 0

        # 製品種別識別変数 初期化
        # 製品種別 -> 1:Forti 2:qnap 3:Isilon 4:XXXX(製品が追加される毎に追加していく)
        # ※今後はベースクラスの継承を利用して製品毎のクラスを作成する方針。製品種別方式は廃止
        # 初期値:0
        self.type = 0

    # インスタンス関数
    # 機能：PDFを指定ファイル名で保存する
    # 引数：なし
    def __save(self):
        self.pdf.save()

    # インスタンス関数
    # 機能：改ページ有無の判定をする
    # 引数：なし
    def _checkOverBottomLineAndNewPage(self):
        # Y軸indexがページ表示領域を超えたら改ページ
        # ページ表示領域：self.END_Y + self.GRID_Y -> 6*mm + 6.35*mm
        if self.index_y < self.END_Y + self.GRID_Y:
            # 改ページ後はFontが初期値に戻る為、再度setFontする
            self.pdf.showPage()
            self.index_y = self.TOP_Y - self.GRID_Y

            # 改ページ時のDRAFTイメージを描画。※プレビュー時のみ
            # 暫定で文字列で描画(イメージだと透過が上手くいかない・・・)
            font_size = 50 #DRAFT文字のFont
            grid_x = 12    #描画X座標
            grid_y = 42    #描画Y座標
            grid_x_span = 125 #X軸幅
            grid_y_span = 37 #Y軸幅
            self.pdf.setFont(self.font, font_size)
            self.pdf.setFillColor(colors.red)
            self.pdf.drawString(self.GRID_X * grid_x, self.GRID_Y * grid_y, "DRAFT")
            self.pdf.setStrokeColor(colors.red)
            self.pdf.rect(self.GRID_X * grid_x, self.GRID_Y * grid_y, grid_x_span, grid_y_span, fill=0)
            self.pdf.setFillColor(colors.black)
            self.pdf.setStrokeColor(colors.black)

            """
            img_path = self.DRAFT_IMG
            # draftイメージの描画
            self.pdf.drawImage(
                img_path,
                self.GRID_X * 11,  # X座標
                self.GRID_Y * 41,  # Y座標
                self.GRID_X * 8,  # X軸大きさ
                self.GRID_Y * 4,  # Y軸大きさ
                mask="auto",  # 透過あり
            )
            """
            # 改ページ実行時。戻り値：1
            return 1

    # インスタンス関数
    # 機能：見積価格データ部分(1セル分)の改行数を取得する関数
    # __説明：見積価格データ部分1セル文の改行数を取得(品名、型番が文字数によって改行する為)
    # __呼出元：_getYGrid
    # __引数：item -> 見積価格データ(辞書型)
    # __戻り値：deepCount -> 対象データ1セル分の改行数を返す
    def _getindentNum(self, item):
        deepCount = 1
        switchCount = 1

        # 項
        tmp_x = self.index_x + (self.GRID_X / 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)

        # 見積価格本文
        # 改行処理。見積価格「品名」、「型番」が一定文字より大きくなると改行する
        switchCount = 1
        res = countLength(item["znw_sku_jp"])
        res = float(res / self.MAX_ZNW_SKU_JP)
        if res > 1:  # 品名の文字数が"MAX_ZNW_SKU_JP"より大きかったら改行
            strlists = splitStr(item["znw_sku_jp"], self.MAX_ZNW_SKU_JP)
            for text in strlists:
                switchCount += 1
            switchCount -= 1
        deepCount = max(deepCount, switchCount)
        # 型番
        switchCount = 1
        res = countLength(item["znw_sku"])
        res = float(res / self.MAX_ZNW_SKU)
        if res > 1:
            strlists = splitStr(item["znw_sku"], self.MAX_ZNW_SKU)
            for text in strlists:
                switchCount += 1
            switchCount -= 1
        deepCount = max(deepCount, switchCount)

        return deepCount

    # インスタンス関数
    # 見積価格データ部分全体のY軸Grid数を取得する関数
    # __説明：データ部分全体(ヘッダ、データ、合計部分)のY軸Grid数を取得
    # __呼出元：__drawContent
    # __引数：input_data ->見積価格データ(辞書型)
    # __戻り値：ygrid -> データ部分全体のY軸Grid数(ヘッダ1Grid含む)
    def _getYGrid(self, input_data):

        # 製品種別により参照データを変更---------------------------------------
        type = self.type
        if type == 1:
            fqitems_type = "fqitems"
        elif type == 2:
            fqitems_type = "fqitems_ref"
        elif type == 3:
            fqitems_type = "fqitems_ref_nextyear"
        else:
            print("No Type")
        # ------------------------------------------------------------------

        # Y軸のGridの数をygridに代入
        # 初期値は3。"①本見積価格"部分 + ヘッダ + 合計 = 3Grid
        ygrid = 3
        for item in input_data[fqitems_type]:
            deepCount = self._getindentNum(item)
            ygrid = ygrid + deepCount

        # データ部分全体のY軸Grid数を返す
        return ygrid

    # インスタンス関数
    # 機能：注釈データ部分(1セル分)の改行数を取得する関数
    # __説明：データ部分の改行数を取得(注釈詳細でのデータ部分)
    # __呼出元：_getYGridAnno
    # __引数：item -> 注釈データ(辞書型)
    # __戻り値：deepCount -> 対象データの改行数を返す
    def _getindentNumAnno(self, item):
        deepCount = 1
        switchCount = 1

        # 項
        tmp_x = self.index_x + (self.GRID_X / 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)

        # 注釈本文
        # 改行処理。注釈本文が一定文字より大きくなると改行する
        switchCount = 1
        res = countLength(item["anno_data"])
        res = float(res / self.MAX_ANNO_DATA)
        if res > 1:  # 注釈本文の文字数が"MAX_ANNO_DATA"より大きかったら改行
            strlists = splitStr(item["anno_data"], self.MAX_ANNO_DATA)
            for text in strlists:
                switchCount += 1
            switchCount -= 1
        deepCount = max(deepCount, switchCount)

        return deepCount

    # インスタンス関数
    # 注釈データ部分全体のY軸Grid数を取得する関数
    # __説明：データ部分のY軸Grid数を取得
    # __呼出元：__drawContentAnnotation
    # __引数：input_data -> 注釈データ(辞書型)
    # __戻り値：ygrid -> データ部分のY軸Grid数(ヘッダ1Grid含む)
    def _getYGridAnno(self, input_data):
        # 製品種別により参照データを変更---------------------------------------
        type = self.type
        if type == 1:
            fqitems_type = "fqitems_anno"
        elif type == 2:
            fqitems_type = "fqitems_anno_ref"
        elif type == 3:
            fqitems_type = "fqitems_anno_ref_nextyear"
        else:
            print("No Type")
        # ------------------------------------------------------------------

        # Y軸のGridの数をygridに代入
        # 初期値は1。ヘッダ部分 = 3Grid
        ygrid = 1
        for item in input_data[fqitems_type]:
            deepCount = self._getindentNumAnno(item)
            ygrid = ygrid + deepCount

        # 実データのY軸Gird数を返す
        return ygrid

    # インスタンス関数
    # データ有無判定(参考価格、次年度参考価格。本見積価格は必須入力の為、対象外)
    # __説明：参考価格、次年度参考価格のそれぞれでデータが存在するか判定
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：input_data -> PDFに描画する全データが含まれるタプル型データ
    # __戻り値： confirmFlg -> 1:参考価格のみデータなし 2:次年度参考価格のみデータなし 3:参考価格,次年度参考価格共にデータなし
    def __dataConfirm(self, input_data):
        confirmFlg = 0
        fqitemsCon1 = input_data["fqitems"]
        fqitemsCon2 = input_data["fqitems_ref"]
        fqitemsCon3 = input_data["fqitems_ref_nextyear"]

        # メモ：本見積価格価格は必須入力なので今のところ処理対象外。UIでエラー出力して貰う予定
        # if len(fqitemsCon1) ==0:
        #    confirmFlg = 0

        # 参考価格のデータなし
        if len(fqitemsCon2) == 0:
            confirmFlg = 1
        # 次年度参考価格のデータなし
        if len(fqitemsCon3) == 0:
            confirmFlg = confirmFlg + 2

        return confirmFlg

    # インスタンス関数
    # 注釈データ有無判定(対象：本見積価格、参考価格、次年度参考価格)
    # __説明：本見積価格、参考価格、次年度参考価格で１つも注釈にデータがあるかどうかの判定
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：input_data -> PDFに描画する全データが含まれるタプル型データ
    # __戻り値： confirmAnnoFlg
    #       本見積価格  参考価格  次年度参考価格
    # 000:     なし       なし           なし
    # 001:     あり       なし           なし
    # 010:     なし       あり           なし
    # 011:     あり       あり           なし
    # 100:     なし       なし           あり
    # 101:     あり       なし           あり
    # 110:     なし       あり           あり
    # 111:     あり       あり           あり
    def __dataAnnoConfirm(self, input_data):
        # 返却フラグ初期化
        confirmAnnoFlg = 0

        # 本見積価格の注文番号有無を判定
        confirmAnnoFlg1 = 0
        for item in input_data["fqitems"]:
            # 注釈番号取得
            annotation_no = item["annotation_no"]
            # 1行でも注釈番号が入力されていたらフラグの値を変更
            if annotation_no != "None":
                confirmAnnoFlg1 = 1

        # 参考価格の注文番号有無を判定
        confirmAnnoFlg2 = 0
        for item in input_data["fqitems_ref"]:
            # 注釈番号取得
            annotation_no = item["annotation_no"]
            # 1行でも注釈番号が入力されていたらフラグの値を変更
            if annotation_no != "None":
                confirmAnnoFlg2 = 10

        # 次年度参考価格の注文番号有無を判定
        confirmAnnoFlg3 = 0
        for item in input_data["fqitems_ref_nextyear"]:
            # 注釈番号取得
            annotation_no = item["annotation_no"]
            # 1行でも注釈番号が入力されていたらフラグの値を変更
            if annotation_no != "None":
                confirmAnnoFlg3 = 100

        confirmAnnoFlg = confirmAnnoFlg1 + confirmAnnoFlg2 + confirmAnnoFlg3

        return confirmAnnoFlg

    # Todo 製品価格(本見積、参考価格、次年度参考価格共通)詳細body作成 開始-------------------------------------------------------------------------

    # インスタンス関数
    # 価格詳細body作成_1 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：body部分のヘッダーを作成(項,品名,型番,数量,標準価格,仕切率,ご提供単価,ご提供価格,注釈)
    # __呼出：__drawContent
    # __引数：input_data   1->本見積価格, 2->参考価格, 3->次年度参考価格
    def _drawContentHead(self, input_data):
        start_y = self.index_y - self.GRID_Y

        # 見積種別により描画位置を変更---------------------------------------
        # 見積種別 1:本見積価格 2:参考価格 3:次年度参考価格
        type = self.type
        # 1:本見積価格
        if type == 1:
            typestr = "■本見積価格"
            # 本見積価格文字列_描写Y軸設定(X軸共通)
            var_y1 = start_y + self.GRID_Y + self.PADDING_BOTTOM  # 文字列描画Y軸
            # 本見積_ヘッダーY軸設定
            start_y = self.index_y
        # 2:参考価格
        elif type == 2:
            typestr = "■参考価格"
            # 参考価格文字列_描写Y軸設定
            var_y1 = start_y  # 文字列描画Y軸

            # 参考価格_ヘッダーY軸設定
            start_y = self.index_y - self.GRID_Y - self.PADDING_BOTTOM
        # 3:次年度参考価格
        elif type == 3:
            typestr = "■次年度参考価格"
            # 次年度参考価格文字列_描写Y軸設定
            var_y1 = self.index_y - self.GRID_Y + (self.PADDING_BOTTOM)  # 文字列描画Y軸
            # 次年度参考価格_ヘッダーY軸設定
            start_y = self.index_y - self.GRID_Y - self.PADDING_BOTTOM
        else:
            sys.exit()
        # ------------------------------------------------------------------

        # 枠線太さ設定
        self.pdf.setLineWidth(0.1)
        # Fontサイズ8->9
        font_size = 9
        self.pdf.setFont(self.font, font_size)

        # 1_見積り価格描画
        # 本見積、参考価格、次年度参考価格_文字列を描画。typestrにより座標を変更している
        self.pdf.drawString(
            self.LEFT_X,
            var_y1,
            typestr,
        )
        # Fontサイズ9->8
        font_size = 8
        self.pdf.setFont(self.font, font_size)

        # 2_ヘッダー部分塗りつぶし
        # 見積種別 1:本見積価格 2:参考価格 3:次年度参考価格----------------------------------
        if type == 1:
            self.pdf.setFillColor(colors.yellowgreen, alpha=0.3)  # 色指定。透過度0.3。
            # start_y = self.index_y
        elif type == 2:
            self.pdf.setFillColor(colors.magenta, alpha=0.3)  # 色指定。透過度0.3。
            # start_y = self.index_y - (self.GRID_Y * 2) - self.PADDING_BOTTOM
        elif type == 3:
            self.pdf.setFillColor(colors.aqua, alpha=0.3)  # 色指定。透過度0.3。
        else:
            sys.exit()
        # -------------------------------------------------------------------------------

        self.pdf.rect(  # 塗りつぶし矩形指定。第1,2引数が四角形の左下の座標、第3,4引数は幅と高さ
            self.LEFT_X,
            start_y - self.GRID_Y,
            self.RIGHT_X - self.LEFT_X,
            self.GRID_Y,
            fill=True,
        )
        self.pdf.setFillColor(colors.black)  # 色を黒に戻す

        # 3_ヘッダー縦線描写
        self.pdf.line(self.LEFT_X, start_y, self.LEFT_X, start_y - self.GRID_Y)

        self.pdf.line(
            self.VERTICAL_X1, start_y, self.VERTICAL_X1, start_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X2, start_y, self.VERTICAL_X2, start_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X3, start_y, self.VERTICAL_X3, start_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X4, start_y, self.VERTICAL_X4, start_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X5, start_y, self.VERTICAL_X5, start_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X6, start_y, self.VERTICAL_X6, start_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X7, start_y, self.VERTICAL_X7, start_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X8, start_y, self.VERTICAL_X8, start_y - self.GRID_Y
        )
        self.pdf.line(self.RIGHT_X, start_y, self.RIGHT_X, start_y - self.GRID_Y)

        # 4_枠線内に(項,品名,型番,数量,標準価格,仕切率,ご提供単価,ご提供価格,注釈)の文字列をそれぞれ記載
        x = self.LEFT_X + (self.GRID_X / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)

        self.pdf.drawCentredString(x, y, "項")

        x = self.VERTICAL_X1 + ((self.VERTICAL_X2 - self.VERTICAL_X1) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)  # grid調整

        self.pdf.drawCentredString(x, y, "品名")

        x = self.VERTICAL_X2 + ((self.VERTICAL_X3 - self.VERTICAL_X2) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "型番")

        x = self.VERTICAL_X3 + ((self.VERTICAL_X4 - self.VERTICAL_X3) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "数量")

        x = self.VERTICAL_X4 + ((self.VERTICAL_X5 - self.VERTICAL_X4) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "標準価格")

        x = self.VERTICAL_X5 + ((self.VERTICAL_X6 - self.VERTICAL_X5) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "仕切率")

        x = self.VERTICAL_X6 + ((self.VERTICAL_X7 - self.VERTICAL_X6) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "ご提供単価")

        x = self.VERTICAL_X7 + ((self.VERTICAL_X8 - self.VERTICAL_X7) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "ご提供価格")
        x = self.VERTICAL_X8 + ((self.RIGHT_X - self.VERTICAL_X8) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "注釈")

    # インスタンス関数(他インスタンス関数から呼出し)
    # 本見積価格詳細body作成_2 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：データ行の枠と実データを描写
    # __呼出：_drawContentData
    # __引数：item 製品詳細データ(辞書型データ)
    def _drawContentDataRows(self, item):

        # 特殊処理1_OPEN価格対応：標準価格が"¥-1"の場合は表示を"OPEN価格"に変更
        if item["list_price"] == "¥-1":
            item["list_price"] = "OPEN" #標準価格は"OPEN価格"
            item["discount_rate"] = "-"     #仕切率は"-"

        # 特殊処理2_見積記載用型番対応：型番(見積記載用)フィールドに文字列が入っている場合はその文字列を型番としてPDFに表示
        if item["znw_sku_gen"] != "None":
            item["znw_sku"] = item["znw_sku_gen"] #"型番(見積記載用)"フィールドの文字列を型番フィールドに表示する

        # deepCount : 折り返して階層が深くなると値が上がる, 品名と型番の深さの最大値を格納
        deepCount = 1
        switchCount = 1
        # 項
        tmp_x = self.index_x + (self.GRID_X / 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawCentredString(tmp_x, tmp_y, item["line_number"])
        # 品名
        # Todo テーブル改行実装
        switchCount = 1
        res = countLength(item["znw_sku_jp"])
        res = float(res / self.MAX_ZNW_SKU_JP)
        if res > 1:  # 品名の文字数が"MAX_ZNW_SKU_JP=37"より大きかったら改行
            strlists = splitStr(item["znw_sku_jp"], self.MAX_ZNW_SKU_JP)
            for text in strlists:
                tmp_x = self.VERTICAL_X1 + ( self.PADDING_BOTTOM * 2 )  # PADDING_BOTTOMは微調整部分。以下使用部分も同様
                tmp_y = (
                    self.index_y - (self.GRID_Y * switchCount) + self.PADDING_BOTTOM * 6.5
                )
                self.pdf.drawString(tmp_x, tmp_y, text)

                # 改行時に文字列の間隔が広くならないよう位置調整(switchCountを小さく)
                switchCount += 0.6
            switchCount -= 1
        else:  # 品名の文字数が"MAX_ZNW_SKU_JP=37"より小さかったら改行しない
            tmp_x = self.VERTICAL_X1 + (self.PADDING_BOTTOM * 2)
            tmp_y = self.index_y - (self.GRID_Y / 1.5)
            self.pdf.drawString(tmp_x, tmp_y, item["znw_sku_jp"])
        deepCount = max(deepCount, switchCount)
        # 型番
        switchCount = 1
        res = countLength(item["znw_sku"])
        res = float(res / self.MAX_ZNW_SKU)
        if res > 1:
            strlists = splitStr(item["znw_sku"], self.MAX_ZNW_SKU)
            for text in strlists:
                tmp_x = self.VERTICAL_X2 + (self.PADDING_BOTTOM * 2)
                tmp_y = (
                    self.index_y - (self.GRID_Y * switchCount) + self.PADDING_BOTTOM * 6.5
                )
                self.pdf.drawString(tmp_x, tmp_y, text)
                # 改行時に文字列の間隔が広くならないよう位置調整(switchCountを小さく)
                switchCount += 0.6
            switchCount -= 1
        else:
            tmp_x = self.VERTICAL_X2 + (self.PADDING_BOTTOM * 2)
            tmp_y = self.index_y - (self.GRID_Y / 1.5)
            self.pdf.drawString(tmp_x, tmp_y, item["znw_sku"])
        deepCount = max(deepCount, switchCount)
        # 数量
        tmp_x = self.VERTICAL_X3 + ((self.VERTICAL_X4 - self.VERTICAL_X3) / 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawCentredString(tmp_x, tmp_y, item["qty"])
        # 標準価格
        tmp_x = self.VERTICAL_X5 - (self.PADDING_BOTTOM * 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawRightString(tmp_x, tmp_y, item["list_price"])

        # 仕切率
        tmp_x = self.VERTICAL_X5 + ((self.VERTICAL_X6 - self.VERTICAL_X5) / 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawCentredString(tmp_x, tmp_y, item["discount_rate"])
        # ご提供単価
        tmp_x = self.VERTICAL_X7 - (self.PADDING_BOTTOM * 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawRightString(tmp_x, tmp_y, item["offer_unit_price"])
        # ご提供価格
        tmp_x = self.VERTICAL_X8 - (self.PADDING_BOTTOM * 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawRightString(tmp_x, tmp_y, item["offer_price"])

        # 注釈
        tmp_x = self.RIGHT_X - self.PADDING_BOTTOM
        tmp_y = self.index_y - (self.GRID_Y / 1.5)

        # 注釈が空(None)の場合は空白""を描画
        if item["annotation_no"] == "None":
            self.pdf.drawRightString(tmp_x, tmp_y, "")
        # 注釈が空(None)でない場合はデータを描画
        else:
            self.pdf.drawRightString(tmp_x, tmp_y, item["annotation_no"])

        # drawContent関数でループ処理をする。ループ処理前にindex_yの値と縦線及びデータの描写を実施する。
        self.pdf.line(
            self.LEFT_X,
            self.index_y,
            self.LEFT_X,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X1,
            self.index_y,
            self.VERTICAL_X1,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X2,
            self.index_y,
            self.VERTICAL_X2,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X3,
            self.index_y,
            self.VERTICAL_X3,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X4,
            self.index_y,
            self.VERTICAL_X4,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X5,
            self.index_y,
            self.VERTICAL_X5,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X6,
            self.index_y,
            self.VERTICAL_X6,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X7,
            self.index_y,
            self.VERTICAL_X7,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.VERTICAL_X8,
            self.index_y,
            self.VERTICAL_X8,
            self.index_y - self.GRID_Y * deepCount,
        )
        self.pdf.line(
            self.RIGHT_X,
            self.index_y,
            self.RIGHT_X,
            self.index_y - self.GRID_Y * deepCount,
        )

        self.index_y = self.index_y - self.GRID_Y * deepCount
        self.pdf.line(self.LEFT_X, self.index_y, self.RIGHT_X, self.index_y)  # 横線描写

    # インスタンス関数(他インスタンス関数から呼出し)
    # 本見積価格詳細body作成_3 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：データ行の枠と実データを描写
    # __呼出元：__drawContent
    # __引数：input_data-> PDFに描画する全データが含まれるタプル型データ
    def _drawContentData(self, input_data):
        font_size = 8
        self.pdf.setFont(self.font, font_size)
        self.pdf.setLineWidth(0.1)

        type = self.type
        # 見積種別 1:本見積価格 2:参考価格 3:次年度参考価格--------------------
        if type == 1:
            fqitems_type = "fqitems"
            sum_data = "offer_price_sum"  # 本見積合計金額
        elif type == 2:
            fqitems_type = "fqitems_ref"
            sum_data = "sub1_offer_price_sum"  # 参考合計金額
        elif type == 3:
            fqitems_type = "fqitems_ref_nextyear"
            sum_data = "sub2_offer_price_sum"  # 次年度参考合計金額
        else:
            print("No Type")
            sys.exit()
        # ------------------------------------------------------------------

        # 実データの部分を描写
        # 辞書型データ変数"fqitems"のデータ数文繰り返す。
        # 例){ "line_number": "1","data": "aa",}と{ "line_number": "2","data": "bb",}の2データある場合は2回繰り返し
        for item in input_data[fqitems_type]:
            # 改ページ判定
            # 戻り値：0->改行なし、1->改行あり
            # flg = self._checkOverBottomLineAndNewPage()

            # 改行あり(flg==1)の場合は次ページトップの横線を描画。この処理をしないとトップ横線が引かれない
            # if flg == 1:
            #    self.pdf.line(self.LEFT_X, self.index_y, self.RIGHT_X, self.index_y)

            # 改ページ後のフォントと枠線を再設定
            # self.pdf.setFont(self.font, font_size)
            # self.pdf.setLineWidth(0.1)

            # _drawContentDataRows関数呼出し。
            self._drawContentDataRows(item)

        # 合計の部分を描写
        # 改ページ判定
        # flg = self._checkOverBottomLineAndNewPage()
        # 改行あり(flg==1)の場合は次ページトップの横線を描画。この処理をしないとトップ横線が引かれない仕様
        # if flg == 1:
        #    self.pdf.line(self.LEFT_X, self.index_y, self.VERTICAL_X8, self.index_y)

        font_size = 8
        self.pdf.setFont(self.font, font_size)
        tmp_x = self.LEFT_X + ((self.VERTICAL_X7 - self.LEFT_X) / 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawCentredString(tmp_x, tmp_y, "合　計")

        font_size = 8
        self.pdf.setFont(self.font, font_size)
        tmp_x = self.VERTICAL_X8 - (self.PADDING_BOTTOM * 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.5)
        self.pdf.drawRightString(tmp_x, tmp_y, input_data[sum_data])

        self.pdf.line(
            self.LEFT_X, self.index_y, self.LEFT_X, self.index_y - self.GRID_Y
        )
        self.pdf.line(
            self.VERTICAL_X7, self.index_y, self.VERTICAL_X7, self.index_y - self.GRID_Y
        )

        self.pdf.line(
            self.VERTICAL_X8, self.index_y, self.VERTICAL_X8, self.index_y - self.GRID_Y
        )
        self.index_y = self.index_y - self.GRID_Y
        self.pdf.line(self.LEFT_X, self.index_y, self.VERTICAL_X8, self.index_y)

        # 合計矩形部分塗りつぶし
        # 見積種別により色指定  1:本見積価格 2:参考価格 3:次年度参考価格---------------------
        if type == 1:
            self.pdf.setFillColor(colors.yellowgreen, alpha=0.3)  # 色指定。透過度0.3。
        elif type == 2:
            self.pdf.setFillColor(colors.magenta, alpha=0.3)  # 色指定。透過度0.3。
        elif type == 3:
            self.pdf.setFillColor(colors.aqua, alpha=0.3)  # 色指定。透過度0.3。
        else:
            sys.exit()
        # --------------------------------------------------------------------------------
        self.pdf.rect(  # 塗りつぶし矩形指定。第1,2引数が四角形の左下の座標、第3,4引数は幅と高さ
            self.LEFT_X,
            self.index_y,
            self.VERTICAL_X7 - self.LEFT_X,
            self.GRID_Y,
            fill=True,
        )
        self.pdf.setFillColor(colors.black)  # 色を黒に戻す

    # インスタンス関数
    # 本見積価格詳細body作成_4 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：本見積価格詳細の描画メイン関数
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：
    #       input_data     -> PDFに描画する全データが含まれるタプル型データ
    #       type           -> 見積種別 1:本見積価格 2:参考価格 3:次年度参考価格
    #       x_coordinate   -> 本見積詳細描画書き出し初期X座標
    #       y_coordinate   -> 本見積詳細描画書き出し初期Y座標
    def __drawContent(
        self,
        input_data,
        type: int(),
        x_coordinate=FINAL_ESTIMATE_BODY_X,
        y_coordinate=FINAL_ESTIMATE_BODY_Y,
    ):
        # 見積種別 1:本見積価格 2:参考価格 3:次年度参考価格
        self.type = type

        # Y軸描画開始座標
        # type-> 見積種別 1:本見積価格 2:参考価格 3:次年度参考価格
        #
        # 本見積価格
        if type == 1:
            # Y軸座標は”y_coordinate”
            start_y = y_coordinate
            # 本見積のヘッダー座標は引数(x_coordinate,y_coordinate)を利用する
            self.index_x = x_coordinate
            self.index_y = y_coordinate
            # インデックス更新時のY軸
            update_index = start_y - self.GRID_Y

        # 参考価格
        elif type == 2:
            # Y軸座標は”self.index_y”。インデックスを使用
            start_y = self.index_y
            # インデックス更新時のY軸
            update_index = start_y - (self.GRID_Y * 2)

        # 次年度参考価格
        elif type == 3:
            # Y軸座標は”self.index_y”。インデックスを使用
            start_y = self.index_y
            # インデックス更新時のY軸
            update_index = start_y - (self.GRID_Y * 2)
        else:
            sys.exit()

        # 価格詳細全体を改ページするか判定------------------------------------------------------------------
        #   注釈全体のY軸Grid数を取得
        #   改ページflg初期化  改ページ無し:0　改ページ有り：1
        newPageFlg = 0
        ygrid = self._getYGrid(input_data)

        # 価格詳細全体全体のY軸長が同一ページに収まらない場合は改ページして注釈ヘッダーから描画
        # ※参考価格,次年度参考価格のみ処理。本見積価格は価格詳細のページ跨りを可とする。

        # 本見積価格の処理
        # 改ページ有無判定は実施しない
        if type == 1:
            newPageFlg = 0
        # 参考価格,次年度参考価格の処理
        # 改ページ有無判定を実施
        else:
            # 改ページ判定処理
            #   self.index_y          -> 現在のY軸座標
            #   (ygrid * self.GRID_Y) -> 注釈全体のY軸長
            if self.index_y < ygrid * self.GRID_Y:
                # 改ページ後、y軸indexを初期値に設定
                self.pdf.showPage()
                self.index_y = self.TOP_Y - self.GRID_Y
                # 改ページflg -> 1
                newPageFlg = 1
        # ----------------------------------------------------------------------------------------------

        # 製品詳細ヘッダ描画
        # 関数呼出し:_drawContentHead
        self._drawContentHead(input_data)

        # インデックスの更新(X軸)
        self.index_x = self.LEFT_X

        # インデックスの更新(Y軸)
        # 改ページ有無によってY軸座標の値が変化
        #  改ページされた場合のY軸座標
        if newPageFlg == 1:
            self.index_y = self.TOP_Y - (self.GRID_Y * 3)
        #  改ページされない場合のY軸座標
        else:
            self.index_y = update_index

        # 製品詳細ボディ描画
        # 関数呼出し:_drawContentData
        self._drawContentData(input_data)

    # Todo 製品価格(本見積、参考価格、次年度参考価格共通)詳細body作成 終了-------------------------------------------------------------------------

    # Todo 製品注釈(本見積、参考価格、次年度参考価格共通)body作成 開始-------------------------------------------------------------------------

    # インスタンス関数(他インスタンス関数から呼出し)
    # 注釈body作成_1 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：注釈body部分のヘッダーを作成(注釈,注釈内容)
    # __呼出元：__drawContentAnnotation
    # __引数：なし

    def _drawContentAnnotationHead(self):
        font_size = 8
        self.pdf.setFont(self.font, font_size)
        self.pdf.setLineWidth(0.1)

        # ヘッダー部分の枠線描写
        start_y = self.index_y
        self.pdf.line(self.LEFT_X, self.index_y, self.RIGHT_X, self.index_y)
        self.pdf.line(
            self.LEFT_X,
            self.index_y - self.GRID_Y,
            self.RIGHT_X,
            self.index_y - self.GRID_Y,
        )
        # ヘッダー部分塗りつぶし
        # 製品種別により塗りつぶし色変更--------------------------------------------------
        # 種別：1->本見積価格, 2->参考価格, 3->次年度参考価格
        type = self.type
        if type == 1:
            self.pdf.setFillColor(colors.yellowgreen, alpha=0.3)  # 色指定。透過度0.3。
        elif type == 2:
            self.pdf.setFillColor(colors.magenta, alpha=0.3)  # 色指定。透過度0.3。
        elif type == 3:
            self.pdf.setFillColor(colors.aqua, alpha=0.3)  # 色指定。透過度0.3。
        else:
            sys.exit()
        # -------------------------------------------------------------------------------

        # 塗りつぶし矩形指定。第1,2引数が四角形の左下の座標、第3,4引数は幅と高さ
        self.pdf.rect(
            self.LEFT_X,
            self.index_y - self.GRID_Y,
            self.RIGHT_X - self.LEFT_X,
            self.GRID_Y,
            fill=True,
        )
        self.pdf.setFillColor(colors.black)  # 色を黒に戻す

        # ヘッダー部分縦線描写
        self.pdf.line(self.LEFT_X, start_y, self.LEFT_X, start_y - self.GRID_Y)
        self.pdf.line(
            self.VERTICAL_X1, start_y, self.VERTICAL_X1, start_y - self.GRID_Y
        )
        self.pdf.line(self.RIGHT_X, start_y, self.RIGHT_X, start_y - self.GRID_Y)

        # 枠線内に(注釈No)を記載
        font_size = 7 #"注釈No"のfontサイズを7へ
        self.pdf.setFont(self.font, font_size)

        x = self.LEFT_X + (self.GRID_X / 2.2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y/2)
        self.pdf.drawCentredString(x, y, "注釈")
        self.pdf.drawCentredString(x, y - (self.GRID_Y/2.5) ,"No")

        font_size = 8 #fontサイズを元に戻す
        self.pdf.setFont(self.font, font_size)

        # 枠線内に(注釈内容)を記載
        x = self.VERTICAL_X2 + ((self.VERTICAL_X3 - self.VERTICAL_X2) / 2)
        y = (start_y - self.GRID_Y) + (self.GRID_Y / 3)
        self.pdf.drawCentredString(x, y, "注釈内容")

    # インスタンス関数(他インスタンス関数から呼出し)
    # 注釈body作成_2 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：注釈行の枠と実データを描写する関数
    # __呼出元：__drawContentAnnotation
    # __引数：item -> 注釈データ(タプル型)
    def _drawContentAnnotationDataRows(self, item):
        deepCount = 1
        switchCount = 1
        #switchCount = 0.8


        # 注釈No.
        tmp_x = self.index_x + (self.GRID_X / 2)
        tmp_y = self.index_y - (self.GRID_Y / 1.25)

        self.pdf.drawCentredString(tmp_x, tmp_y, item["anno_line_number"])

        # 改行コード処理---始---------------------------------------------------------
        anno_data = []
        tmp_str = item["anno_data"]

        # 注釈本文を改行コードで分割しリスト変数へ
        # 例) "AAA\r\nBBB\r\nCCC" -> {"AAA","BBB","CCC",}
        anno_data = tmp_str.splitlines()

        # 1_改行コードで分割された文字列を改行して繰り返し描画
        # 2_分割された文字列が規定文字数以上の場合はさらに改行
        # 例) {"AAAAAAAAAAAA","BBB","CCC",}　<-リストの文字列を１つずつ改行判定をする。最大文字列が"8"の場合結果は下記になる。
        # 1      AAAAAAAA
        #        AAAA
        # 2      BBB
        # 3      CCC
        for text in anno_data:
            res = countLength(text)
            res = float(res / self.MAX_ANNO_DATA)
            # 改行判定。注釈本文が一定文字より大きくなると改行する
            if res > 1:  # 注釈本文(改行コードで分割された文字)の文字数が"MAX_ANNO_DATA"より大きかったら改行
                strlists = splitStr(text, self.MAX_ANNO_DATA)
                # 注釈本文(改行コードで分割された文字)リストを繰り返しで描画
                for text in strlists:
                    tmp_x = self.VERTICAL_X1 + (self.PADDING_BOTTOM * 2)
                    tmp_y = (
                        self.index_y
                        - (self.GRID_Y * switchCount)
                        #+ (self.PADDING_BOTTOM * 2.5)  #Y軸調整(改行する場合)
                        + (self.PADDING_BOTTOM * 4)  #Y軸調整(改行する場合)
                    )
                    self.pdf.drawString(tmp_x, tmp_y, text)
                    # 改行した際に、文字列の間隔を狭くする
                    switchCount += 0.6

            # 改行判定。注釈本文が一定文字より小さいと改行しない
            else:
                tmp_x = self.VERTICAL_X1 + (self.PADDING_BOTTOM * 2)
                tmp_y = (
                    self.index_y
                    - (self.GRID_Y * switchCount)
                    + (self.PADDING_BOTTOM * 2.5) #Y軸調整(改行しない場合)
                )
                self.pdf.drawString(tmp_x, tmp_y, text)
                switchCount += 0.7
        switchCount -= 1
        deepCount = max(deepCount, switchCount)

        # 改行コード処理---終---------------------------------------------------------

        # ループ前の更新処理等
        # 左端縦線描写
        self.pdf.line(
            self.LEFT_X,
            self.index_y,
            self.LEFT_X,
            self.index_y - self.GRID_Y * deepCount - (self.PADDING_BOTTOM * 4),
        )
        # "注釈No"右縦線描写
        self.pdf.line(
            self.VERTICAL_X1,
            self.index_y,
            self.VERTICAL_X1,
            #self.index_y - self.GRID_Y * deepCount,
            self.index_y - self.GRID_Y * deepCount - (self.PADDING_BOTTOM * 4),
        )
        # 右端縦線描写
        self.pdf.line(
            self.RIGHT_X,
            self.index_y,
            self.RIGHT_X,
            #self.index_y - self.GRID_Y * deepCount,
            self.index_y - self.GRID_Y * deepCount - (self.PADDING_BOTTOM * 4),
        )

        self.index_y = self.index_y - self.GRID_Y * deepCount
        # 下線まである程度余白を入れる為、Y軸をPADDING_BOTTOM x 2分下方向へ
        #self.pdf.line(self.LEFT_X, self.index_y, self.RIGHT_X, self.index_y)
        self.pdf.line(self.LEFT_X, self.index_y - (self.PADDING_BOTTOM * 4) , self.RIGHT_X, self.index_y - (self.PADDING_BOTTOM * 4))

    # インスタンス関数(他インスタンス関数から呼出し)
    # 注釈body作成_3 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：注釈行の枠と実データを描写する関数
    # __呼出元：__drawContentAnnotation
    # __引数：input_data -> 注釈データ(辞書型)
    def _drawContentAnnotationData(self, input_data):
        font_size = 8
        self.pdf.setFont(self.font, font_size)
        self.pdf.setLineWidth(0.1)

        # 実データの部分を描写
        index = 1
        # 製品種別により参照データを変更---------------------------------------
        type = self.type
        if type == 1:
            fqitems_type = "fqitems_anno"
        elif type == 2:
            fqitems_type = "fqitems_anno_ref"
        elif type == 3:
            fqitems_type = "fqitems_anno_ref_nextyear"
        else:
            print("No Type")
        # ------------------------------------------------------------------

        # 注釈行の数だけ描画を繰り返す
        for item in input_data[fqitems_type]:
            self._drawContentAnnotationDataRows(item)

    # インスタンス関数
    # 注釈body作成_4 (本見積価格,参考価格,次年度参考価格 共通関数)
    # __説明：注釈行の枠と実データを描写する関数
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：
    #       input_data -> 注釈データ(辞書型)
    #       type       -> 1->本見積価格 2->参考価格 3->次年度参考価格
    def __drawContentAnnotation(self, input_data, type: int()):

        # 見積種別取得： 1->本見積価格 2->参考価格 3->次年度参考価格
        self.type = type

        # 描画座標設定
        x_coordinate = self.LEFT_X
        y_coordinate = self.index_y - self.GRID_Y
        start_y = y_coordinate
        self.index_x = x_coordinate
        self.index_y = y_coordinate

        # 注釈全体を改ページするか判定------------------------------------------------------------------
        #   注釈全体のY軸Grid数を取得
        ygrid = self._getYGridAnno(input_data)

        # 注釈全体のY軸長が同一ページに収まらない場合は改ページして注釈ヘッダーから描画
        #   self.index_y -> 現在のY軸座標
        #   (ygrid * self.GRID_Y) -> 注釈全体のY軸長

        #yobun = self.TOP_Y - self.index_y
        y_temp = ygrid * self.GRID_Y
        if self.index_y < ygrid * self.GRID_Y:
            # 改ページ後、y軸indexを初期値に設定
            self.pdf.showPage()
            self.index_y = self.TOP_Y - self.GRID_Y
        # ------------------------------------------------------------------------------------------

        # 注釈ヘッダ描画
        self._drawContentAnnotationHead()
        # インデックスの更新(1Grid分Y軸方向に下げる)
        self.index_y = self.index_y - self.GRID_Y
        # 注釈実データ描画
        self._drawContentAnnotationData(input_data)

    # Todo 製品注釈(本見積、参考価格、次年度参考価格共通)body作成 終了-------------------------------------------------------------------------

    # Todo フッター作成 開始-------------------------------------------------------------------------
    # インスタンス関数(他インスタンス関数から呼出し)
    # フッター作成_1
    # __説明：フッターの作成
    # __呼出元：__drawFooter
    # __引数：data -> 注釈データ(タプル型)
    def _drawFooterItems(self, data):
        font_size = 8
        tmp_x = self.LEFT_X + self.GRID_X
        self.index_y = self.index_y - (self.GRID_Y / 2)
        half_GRID_Y = self.GRID_Y / 2

        for item in data:
            res = countLength(item)
            res = float(res / self.MAX_FOOTER_SENTENCE_SIZE)
            # 改行なし
            if res > 1:
                texts = splitStr(item, self.MAX_FOOTER_SENTENCE_SIZE)
                for text in texts:
                    self._checkOverBottomLineAndNewPage()
                    self.pdf.setFont(self.font, font_size)
                    self.pdf.setLineWidth(0.1)
                    self.pdf.drawString(tmp_x, self.index_y - half_GRID_Y, text)
                    self.index_y = self.index_y - half_GRID_Y
            # 改行あり
            else:
                self._checkOverBottomLineAndNewPage()
                self.pdf.setFont(self.font, font_size)
                self.pdf.setLineWidth(0.1)
                self.pdf.drawString(tmp_x, self.index_y - half_GRID_Y, item)
                self.index_y = self.index_y - half_GRID_Y

    # インスタンス関数
    # フッター作成_2
    # __説明：フッターの作成
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：input_datadata -> 注釈データ(辞書型)
    def __drawFooter(self, input_data):
        # 改ページ必要か
        if self.index_y - (self.GRID_Y * 4) < self.END_Y + self.GRID_Y:
            # 改ページ後はsetFontしないと文字化けします
            self.pdf.showPage()
            self.index_y = self.TOP_Y - self.GRID_Y

        x_coordinate = self.LEFT_X
        y_coordinate = self.index_y - self.GRID_Y
        start_y = y_coordinate

        font_size = 8
        self.pdf.setFont(self.font, font_size)
        self.pdf.setLineWidth(0.1)
        # 1_フッター枠線描画
        x = self.LEFT_X
        y = start_y - self.GRID_Y

        tmp_x = self.LEFT_X + self.GRID_X
        tmp_y = y - (self.GRID_Y / 2)
        self.pdf.line(tmp_x, tmp_y, tmp_x, tmp_y - (self.GRID_Y * 2))
        self.pdf.line(tmp_x, tmp_y, tmp_x + (self.GRID_X * 2), tmp_y)
        tmp_x = self.RIGHT_X - self.GRID_X
        self.pdf.line(tmp_x, tmp_y, tmp_x, tmp_y - (self.GRID_Y * 2))
        self.pdf.line(tmp_x, tmp_y, tmp_x - (self.GRID_X * 8), tmp_y)
        self.pdf.line(
            tmp_x,
            tmp_y - (self.GRID_Y * 2),
            self.LEFT_X + self.GRID_X,
            tmp_y - (self.GRID_Y * 2),
        )

        # 2_フッター枠上文字列描画(固定文言)
        tmp_x = self.LEFT_X + (self.GRID_X * 3.5)
        tmp_y = y - (self.GRID_Y / 2)
        self.pdf.drawString(tmp_x, tmp_y, self.FOOTER_FIX_SENTENCE1)

        tmp_x = self.LEFT_X + (self.GRID_X * 2)
        tmp_y = y - (self.GRID_Y * 1.5)
        self.pdf.drawString(tmp_x, tmp_y, self.FOOTER_FIX_SENTENCE2)

        tmp_y = y - (self.GRID_Y * 2)
        self.pdf.drawString(tmp_x, tmp_y, self.FOOTER_FIX_SENTENCE3)

        self.index_y = y - (self.GRID_Y * 3)

        # 3_フッター枠内文字列描画(可変文言)
        self._drawFooterItems(input_data["footer_items"])

    # Todo フッター作成 終了-------------------------------------------------------------------------

    # Todo Header作成 開始-------------------------------------------------------------------------
    # インスタンス関数
    # ヘッダー作成_1
    # __説明："御 見 積 書"描画
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：x_coordinate -> X軸座標 y_coordinate -> Y軸座標
    def __drawHeaderTitle(
        self, x_coordinate=HEADER_TITLE_X, y_coordinate=HEADER_TITLE_Y
    ):
        # 1,"見積書"固定
        font_size = 20
        title = "御 見 積 書"  # 固定文言
        self.pdf.setFont(self.font, font_size)
        self.pdf.drawString(x_coordinate, y_coordinate, title)
        self.pdf.setLineWidth(0.1)
        #self.pdf.line(
        #    x_coordinate, y_coordinate, x_coordinate + (self.GRID_X * 6), y_coordinate
        #)
        self.pdf.line(
            x_coordinate,
            y_coordinate - (0.5 * mm),
            x_coordinate + (self.GRID_X * 6),
            y_coordinate - (0.5 * mm),
        )

    # インスタンス関数
    # ヘッダー作成_2
    # __説明：ヘッダー左上部分を記述(株式会社 XXXX 御中,XXXX 様向け,御見積件名,納期,御受渡場所,御支払い条件,見積有効期間,見積金額,特記事項)
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：input_data -> 辞書型データ, x_coordinate -> X軸座標, y_coordinate -> Y軸座標
    def __drawHeaderHeadline(
        self, input_data, x_coordinate=HEADER_CLIENT_X, y_coordinate=HEADER_CLIENT_Y
    ):
        # ヘッダー左上部分2～3を記述
        # 2,株式会社 XXXX 御中   <-- XXXXは辞書型変数"input_data"から取得
        # 3,エンドユーザー名     <-- XXXXは辞書型変数"input_data"から取得
        headline_str1 = input_data["customer_id"] + "  御中"
        headline_str2 = input_data["end_user"] + "  様向け"

        # エンドユーザー名が空の場合の処理
        # エンドユーザー名が空の場合、エンドユーザーを描画しない
        if input_data["end_user"] == "None":
            data_headline1 = [
                [headline_str1],
          ]
        # エンドユーザー名が空でない場合、エンドユーザーを描画する
        else:
            data_headline1 = [
                [headline_str1],
                [headline_str2],
            ]
        # 顧客名とエンドユーザー名をTable形式で描画
        table = Table(data_headline1)
        table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (0, 0), self.font, 12), #顧客名Fontサイズ
                    ("FONT", (0, 1), (0, 1), self.font, 10), #エンドユーザー名Fontサイズ
                    ("LINEBELOW", (0, 0), (0, 1), 0.1, colors.black),
                    ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
                    ("VALIGN", (0, 1), (0, 1), "BOTTOM"),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ]
            )
        )
        table.wrapOn(self.pdf, x_coordinate, y_coordinate + (self.GRID_Y * 8))
        table.drawOn(self.pdf, x_coordinate, y_coordinate + (self.GRID_Y * 8))

        # ヘッダー左上部分4～10を記述
        # 4,御見積件名     <-- 辞書型変数"input_data"から取得
        # 5,納    期       <-- 辞書型変数"input_data"から取得
        # 6,御受渡場所     <-- 辞書型変数"input_data"から取得
        # 7,御支払い条件   <-- 辞書型変数"input_data"から取得
        # 8,見積有効期間   <-- 辞書型変数"input_data"から取得
        # 9,見積金額       <-- 辞書型変数"input_data"から取得
        # 10,特記事項      <-- 辞書型変数"input_data"から取得
        data_headline2 = [
            ["御見積件名", ":", input_data["quotation_subject"]],
            ["納    期", ":", input_data["deadline"]],
            ["御受渡場所", ":", input_data["delivery_place"]],
            ["御支払い条件", ":", input_data["payment_terms"]],
            ["見積有効期間", ":", input_data["validity_period"]],
            ["見積金額", ":", input_data["quotation_price"]],
            ["特記事項", ":", input_data["notices"]],
        ]
        table = Table(
            data_headline2,
            colWidths=(self.GRID_X * 3, self.GRID_X / 2, self.GRID_X * 8),
            rowHeights=self.GRID_Y,
        )
        table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), self.font, 8),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.1, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ]
            )
        )
        table.wrapOn(self.pdf, x_coordinate, y_coordinate)
        table.drawOn(self.pdf, x_coordinate, y_coordinate)

    # インスタンス関数
    # ヘッダー作成_3
    # __説明：ヘッダー右上_1 部分を記述(見積番号、見積月日)
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：input_data -> 辞書型データ, x_coordinate -> X軸座標, y_coordinate -> Y軸座標
    def __drawHeaderEstimationNumber(
        self,
        input_data,
        x_coordinate=HEADER_ESTIMATE_NUM_X,
        y_coordinate=HEADER_ESTIMATE_NUM_Y,
    ):

        # 11,見積番号       <-- 辞書型変数"input_data"から取得
        # 12,見積月日       <-- 辞書型変数"input_data"から取得。修正：当日日付から取得するよう変更
        data = [
            ["見積番号", ":", input_data["quotation_id"]],
            ["見積月日", ":", input_data["quotation_date"]],
        ]
        table = Table(
            data,
            colWidths=(self.GRID_X * 2, self.GRID_X / 2, self.GRID_X * 5),
            rowHeights=self.GRID_Y,
        )
        table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), self.font, 8),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.1, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ]
            )
        )
        table.wrapOn(self.pdf, x_coordinate, y_coordinate)
        table.drawOn(self.pdf, x_coordinate, y_coordinate)

    # インスタンス関数
    # ヘッダー作成_4
    # __説明：ヘッダー右上_2 部分を記述(ZNW社名、住所、TEL)
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：input_data -> 辞書型データ, x_coordinate -> X軸座標, y_coordinate -> Y軸座標
    def __drawHeaderOursInfo(
        self, input_data, x_coordinate=HEADER_ZNW_INFO_X, y_coordinate=HEADER_ZNW_INFO_Y
    ):
        # 13,ZNW情報   <-- 現在は固定。今後は可変にする予定
        data = [
            [self.COMPANY_NAME],
            [self.COMPANY_ADDRESS],
            [self.COMPANY_TEL],
            [self.COMPANY_FAX],
        ]
        table = Table(data, colWidths=self.GRID_X * 6, rowHeights=self.GRID_Y)
        table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), self.font, 8),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        table.wrapOn(self.pdf, x_coordinate, y_coordinate)
        table.drawOn(self.pdf, x_coordinate, y_coordinate)

    # インスタンス関数
    # ヘッダー作成_5
    # __説明：ヘッダー右上_3 部分を記述(押印エリアの枠のみ記述)
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：x_coordinate -> X軸座標, y_coordinate -> Y軸座標
    def __drawHeaderStampArea(
        self, x_coordinate=HEADER_ZNW_SEAL_FLAME_X, y_coordinate=HEADER_ZNW_SEAL_FLAME_Y
    ):
        h = self.GRID_Y
        w = self.GRID_X
        # オブジェクトの左下の座標を変数で指定
        x = x_coordinate
        y = y_coordinate
        self.pdf.rect(x, y, (w * 3), (h * 3))
        x += w * 3
        self.pdf.rect(x, y, (w * 3), (h * 3))
        x += w * 3
        self.pdf.rect(x, y, (w * 3), (h * 3))

    # TODO 要確認!!!! 承認フロークラスとの連携が必要。現在は押印は固定!!!!
    # インスタンス関数
    # ヘッダー作成_5
    # __説明：押印実施。3か所
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：x_coordinate -> X軸座標, y_coordinate -> Y軸座標
    def __drawHeaderApprovalStamp(
        self,
        data,
        x_coordinate=HEADER_EMPLOYEE_SEAL_X,
        y_coordinate=HEADER_EMPLOYEE_SEAL_Y,
    ):
        font_size = 8
        self.pdf.setFont(self.font, font_size)

        x = x_coordinate
        y = y_coordinate + (self.GRID_Y / 2)

        # 押印スタンプは可変にする必要あり。要修正
        #approval_seal_01 = os.getcwd() + data["stamp_1_id"]
        #approval_seal_02 = os.getcwd() + data["stamp_2_id"]
        #approval_seal_03 = os.getcwd() + data["stamp_3_id"]
        approval_seal_01 = data["stamp_1_id"]
        approval_seal_02 = data["stamp_2_id"]
        approval_seal_03 = data["stamp_3_id"]

        x += self.GRID_X
        self.pdf.drawImage(
            approval_seal_01, x, y, self.GRID_X * 2, self.GRID_Y * 2, mask="auto"
        )
        x += self.GRID_X * 3
        self.pdf.drawImage(
            approval_seal_02, x, y, self.GRID_X * 2, self.GRID_Y * 2, mask="auto"
        )
        x += self.GRID_X * 3
        self.pdf.drawImage(
            approval_seal_03, x, y, self.GRID_X * 2, self.GRID_Y * 2, mask="auto"
        )

    # インスタンス関数
    # ヘッダー作成_5
    # __説明：ZNW押印実施。固定スタンプ
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数：x_coordinate -> X軸座標, y_coordinate -> Y軸座標
    def __drawHeaderCompanySeal(
        self, x_coordinate=HEADER_ZNW_SEAL_X, y_coordinate=HEADER_ZNW_SEAL_Y
    ):
        # 挿入したいファイルのパス
        # 17,ZNW会社スタンプ
        img_path = self.COMPANY_SEAL
        # 画像ファイルの挿入
        self.pdf.drawImage(
            img_path,
            x_coordinate,
            y_coordinate,
            self.GRID_X * 3,
            self.GRID_Y * 3,
            mask="auto",
        )

    # Todo Header作成 終了-------------------------------------------------------------------------

    # インスタンス関数
    # ドラフト版透かし文字描画
    # __説明：プレビューの際はドラフト版透かし文字を描画。
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    def __drawdraft(
        self, x_coordinate=HEADER_ZNW_SEAL_X, y_coordinate=HEADER_ZNW_SEAL_Y
    ):

        # 暫定で文字列で描画(イメージだと透過が上手くいかない・・・)
        font_size = 50 #DRAFT文字のFont
        grid_x = 12    #描画X座標
        grid_y = 42    #描画Y座標
        grid_x_span = 125 #X軸幅
        grid_y_span = 37 #Y軸幅
        self.pdf.setFont(self.font, font_size)
        self.pdf.setFillColor(colors.red)
        self.pdf.drawString(self.GRID_X * grid_x, self.GRID_Y * grid_y, "DRAFT")
        self.pdf.setStrokeColor(colors.red)
        self.pdf.rect(self.GRID_X * grid_x, self.GRID_Y * grid_y, grid_x_span, grid_y_span, fill=0)
        self.pdf.setFillColor(colors.black)
        self.pdf.setStrokeColor(colors.black)

        """
        # self.pdf.drawString(self.GRID_X * 11, self.GRID_Y * 41, "DRAFT")
        # DRAFTイメージ描画
        img_path = self.DRAFT_IMG
        # 画像ファイルの挿入
        self.pdf.drawImage(
            img_path,
            self.GRID_X * 11,  # X座標
            self.GRID_Y * 41,  # Y座標
            self.GRID_X * 8,  # X軸大きさ
            self.GRID_Y * 4,  # Y軸大きさ
            mask="Auto",  # 透過あり
            # mask=[0, 2, 0, 2, 0, 2, ]
        )
        """

    # Todo 見積IDから辞書型データを作成 開始-------------------------------------------------------------------------

    # インスタンス関数
    # 辞書型データ作成
    # __説明：見積IDから辞書型データを作成
    # __呼出元：クラス estimatepdf_main.ExeMakeEstimatePdf
    # __引数1：見積ID
    # __引数2：保守用フラグ True-> 保守用フッター使用 False->通常フッタ使用(デフォルト値)
    # __戻り値：辞書型データ
    def __makeDictData(self, estimateid: int(),hosyu):
        self.estimateid = estimateid  # 見積ID

        #SBMチームログイン時テスト
        #hosyu =  1
        #SBMチーム以外ログイン時テスト
        #hosyu =  0
        self.hosyu = hosyu  # 保守用フラグ

        # 承認者ハンコ押印機能 add 20231006
        #
        # 1_作成者、第1承認者、第2承認者の社員番号を辞書型データで取得
        employee_num_dict = get_quote_info_by_id(self.estimateid)

        #作成者の社員番号
        creater_id = employee_num_dict['sales_staff']
        #第1承認者の社員番号
        auth1_id = employee_num_dict['auth1_id']
        #第2承認者の社員番号
        auth2_id = employee_num_dict['auth2_id']

        # 2_作成者、第1承認者、第2承認者の社員番号からハンコを作成。格納パスを取得
        hg = HankoGenerator()

        # 社員番号が存在しない場合は空のハンコを押印。後でestimatepdf_const_be.pyへ記載する
        NONECASE_PATH = "/home/dev1/proj/znwproject/static/media/hanko/00000_hanko.png"

        #作成者のハンコの格納パス
        creater_stamp_path = hg.generate_hanko_image(creater_id, True)
        if creater_stamp_path is None:
            creater_stamp_path = NONECASE_PATH

        #第1承認者のハンコの格納パス
        auth1_stamp_path = hg.generate_hanko_image(auth1_id, True)
        if auth1_stamp_path is None:
            auth1_stamp_path = NONECASE_PATH

        #第2承認者のハンコの格納パス
        auth2_stamp_path = hg.generate_hanko_image(auth2_id, True)
        if auth2_stamp_path is None:
            auth2_stamp_path = NONECASE_PATH

        estimateobj = FtnQuoteHeader.objects.get(id=estimateid)  # 見積DBオブジェクトモデル取得
        mainitemset = estimateobj.ftnquotemainitem_set.all().order_by(
            "number"
        )  # 本見積_詳細データ取得(辞書型)
        mainnotesset = estimateobj.ftnquotemainnotes_set.all().order_by(
            "number"
        )  # 本見積_注釈データ取得(辞書型)
        sub1itemset = estimateobj.ftnquotesub1item_set.all().order_by(
            "number"
        )  # 参考価格積_詳細データ取得(辞書型)
        sub1notesset = estimateobj.ftnquotesub1notes_set.all().order_by(
            "number"
        )  # 参考価格_注釈データ取得(辞書型)
        sub2itemset = estimateobj.ftnquotesub2item_set.all().order_by(
            "number"
        )  # 次年度参考価格_詳細データ取得(辞書型)
        sub2notesset = estimateobj.ftnquotesub2notes_set.all().order_by(
            "number"
        )  # 次年度参考価格_注釈データ取得(辞書型)

        # フッター文言
        # 保守用フラグが"True"(つまりSBMチームがユーザーの場合)の場合は保守用フッター
        if self.hosyu == 1:
        #if self.hosyu == "True":

            footer_sentence = [
                self.FOOTER_VAL_SENTENCE1_HOSYU,
                self.FOOTER_VAL_SENTENCE2_HOSYU,
                self.FOOTER_VAL_SENTENCE3_HOSYU,
                self.FOOTER_VAL_SENTENCE4_HOSYU,
                self.FOOTER_VAL_SENTENCE5_HOSYU,
            ]
        # 保守用フラグが"False"の場合は通常フッター
        else:
            footer_sentence = [
                self.FOOTER_VAL_SENTENCE1_NORMAL,
                self.FOOTER_VAL_SENTENCE2_NORMAL,
            ]

        # Todo STEP1_製品詳細 実データ 配列作成(実製品、参考価格製品、次年度参考価格製品 それぞれ作成)--------------------------------------
        # 1_見積製品データ部分に記載する辞書型データを配列として作成 ※32行だと上手くいかない。要確認
        fqitems_dict = {
            "line_number": "",
            "znw_sku_jp": "",
            "znw_sku": "",
            "qty": "",
            "list_price": "",
            "discount_rate": "",
            "offer_unit_price": "",
            "offer_price": "",
            "annotation_no": "",
            "znw_sku_gen": "",
        }
        fqitems = []
        if mainitemset:
            for obj in mainitemset:
                fqitems_dict = {
                    "line_number": str(obj.number),  # 項番
                    "znw_sku_jp": str(obj.znw_sku_jp),  # 品名
                    "znw_sku": str(obj.znw_sku),  # 型番
                    "qty": str(obj.qty),  # 数量
                    "list_price": "¥{:,}".format(obj.lp),  # 標準価格
                    "discount_rate": "{:,%}".format(obj.discount_rate),  # 仕切率
                    "offer_unit_price": "¥{:,}".format(obj.offer_unit_price),  # ご提供単価
                    "offer_price": "¥{:,}".format(obj.offer_price),  # ご提供価格
                    "annotation_no": str(obj.notes_number),  # 注釈番号
                    "znw_sku_gen": str(obj.znw_sku_gen),  # 見積書表示用型番

                }
                # リストに追加する
                fqitems_dict_list = (
                    fqitems_dict.copy()
                )  # 辞書型"fqitems_dict"の値を辞書型"fqitems_dict_list"に格納
                fqitems.append(
                    fqitems_dict_list
                )  # 辞書型"fqitems_dict_list"の値を辞書型配列"fqitems"に項番の数分、追加していく

        # 2_参考データ部分に記載する辞書型データを配列として作成fqitems_ref
        fqitems_dict_ref = {
            "line_number": "",
            "znw_sku_jp": "",
            "znw_sku": "",
            "qty": "",
            "list_price": "",
            "discount_rate": "",
            "offer_unit_price": "",
            "offer_price": "",
            "annotation_no": "",
            "znw_sku_gen": "",

        }
        fqitems_ref = []
        if sub1itemset:
            for obj in sub1itemset:
                fqitems_dict_ref = {
                    "line_number": str(obj.number),  # 項番
                    "znw_sku_jp": str(obj.znw_sku_jp),  # 品名
                    "znw_sku": str(obj.znw_sku),  # 型番
                    "qty": str(obj.qty),  # 数量
                    "list_price": "¥{:,}".format(obj.lp),  # 標準価格
                    "discount_rate": "{:,%}".format(obj.discount_rate),  # 仕切率
                    "offer_unit_price": "¥{:,}".format(obj.offer_unit_price),  # ご提供単価
                    "offer_price": "¥{:,}".format(obj.offer_price),  # ご提供価格
                    "annotation_no": str(obj.notes_number),  # 注釈番号
                    "znw_sku_gen": str(obj.znw_sku_gen),  # 見積書表示用型番

                }
                # リストに追加する
                fqitems_dict_ref_list = (
                    fqitems_dict_ref.copy()
                )  # 辞書型"fqitems_dict_ref"の値を辞書型"fqitems_dict_ref_list"に格納
                fqitems_ref.append(
                    fqitems_dict_ref_list
                )  # 辞書型"fqitems_dict_ref_list"の値を辞書型配列"fqitems"に項番の数分、追加していく

        # 3_次年度参考データ部分に記載する辞書型データを配列として作成
        fqitems_dict_ref_nextyear = {
            "line_number": "",
            "znw_sku_jp": "",
            "znw_sku": "",
            "qty": "",
            "list_price": "",
            "discount_rate": "",
            "offer_unit_price": "",
            "offer_price": "",
            "annotation_no": "",
            "znw_sku_gen": "",
        }
        fqitems_ref_nextyear = []
        if sub2itemset:
            for obj in sub2itemset:
                fqitems_dict_ref_nextyear = {
                    "line_number": str(obj.number),  # 項番
                    "znw_sku_jp": str(obj.znw_sku_jp),  # 品名
                    "znw_sku": str(obj.znw_sku),  # 型番
                    "qty": str(obj.qty),  # 数量
                    "list_price": "¥{:,}".format(obj.lp),  # 標準価格
                    "discount_rate": "{:,%}".format(obj.discount_rate),  # 仕切率
                    "offer_unit_price": "¥{:,}".format(obj.offer_unit_price),  # ご提供単価
                    "offer_price": "¥{:,}".format(obj.offer_price),  # ご提供価格
                    "annotation_no": str(obj.notes_number),  # 注釈番号
                    "znw_sku_gen": str(obj.znw_sku_gen),  # 見積書表示用型番
                }
                # リストに追加する
                fqitems_dict_ref_nextyear_list = (
                    fqitems_dict_ref_nextyear.copy()
                )  # 辞書型"fqitems_dict_ref_nextyear"の値を辞書型"fqitems_dict_ref_nextyear_list"に格納
                fqitems_ref_nextyear.append(
                    fqitems_dict_ref_nextyear_list
                )  # 辞書型"fqitems_dict_ref_list"の値を辞書型配列"fqitems"に項番の数分、追加していく

        # Todo STEP2_製品注釈データ 配列作成(実製品、参考価格製品、次年度参考価格製品 それぞれ作成)--------------------------------------
        # 1_本見積製品データ部分に記載する注釈。辞書型データを配列として作成
        fqitems_dict_anno = {"anno_line_number": "", "anno_data": ""}
        fqitems_anno = []
        if mainnotesset:
            for obj in mainnotesset:
                fqitems_dict_anno = {
                    "anno_line_number": str(obj.number),  # 項番
                    "anno_data": str(obj.notes),  # 注釈本文
                }
                # リストに追加する
                fqitems_dict_anno_list = fqitems_dict_anno.copy()
                fqitems_anno.append(fqitems_dict_anno_list)

        # 2_参考価格データ部分に記載する注釈。辞書型データを配列として作成
        fqitems_dict_anno_ref = {"anno_line_number": "", "anno_data": ""}
        fqitems_anno_ref = []
        if sub1notesset:
            for obj in sub1notesset:
                fqitems_dict_anno_ref = {
                    "anno_line_number": str(obj.number),  # 項番
                    "anno_data": str(obj.notes),  # 注釈本文
                }
                # リストに追加する
                fqitems_dict_anno_ref_list = fqitems_dict_anno_ref.copy()
                fqitems_anno_ref.append(fqitems_dict_anno_ref_list)

        # 3_次年度参考価格データ部分に記載する注釈。辞書型データを配列として作成
        fqitems_dict_anno_ref_nextyear = {"anno_line_number": "", "anno_data": ""}
        fqitems_anno_ref_nextyear = []
        if sub2notesset:
            for obj in sub2notesset:
                fqitems_dict_anno_ref_nextyear = {
                    "anno_line_number": str(obj.number),  # 項番
                    "anno_data": str(obj.notes),  # 注釈本文
                }
                # リストに追加する
                fqitems_dict_anno_ref_nextyear_list = (
                    fqitems_dict_anno_ref_nextyear.copy()
                )
                fqitems_anno_ref_nextyear.append(fqitems_dict_anno_ref_nextyear_list)

        # Todo STEP3_クラス引数作成(辞書型)-------------------------------------------------------------------------
        forti_data = {
            "customer_id": str(estimateobj.customer_id),  # ヘッダー顧客社名
            "end_user": str(estimateobj.end_user),  # エンドユーザー
            "quotation_subject": estimateobj.quotation_subject,  # 御見積件名
            "deadline": estimateobj.deadline,  # 納期
            "delivery_place": estimateobj.delivery_place,  # 御受渡場所
            "payment_terms": estimateobj.payment_terms,  # 御支払い条件
            "validity_period": estimateobj.validity_period,  # 見積有効期間
            "quotation_price": "¥{:,}".format(estimateobj.quotation_price),  # 見積金額
            "notices": estimateobj.notices,  # 見積金額
            "quotation_id": estimateobj.quotation_id,  # 見積番号
            "quotation_date": estimateobj.quotation_date.strftime(
                "%Y年%#m月%#d日"
            ),  # 見積月日
            "fqitems": fqitems,  # 本見積詳細データ(配列)
            "fqitems_ref": fqitems_ref,  # 参考価格詳細データ(配列)
            "fqitems_ref_nextyear": fqitems_ref_nextyear,  # 次年度参考価格詳細データ(配列)
            "fqitems_anno": fqitems_anno,  # 参考価格注釈データ(配列)
            "fqitems_anno_ref": fqitems_anno_ref,  # 参考価格詳細データ(配列)
            "fqitems_anno_ref_nextyear": fqitems_anno_ref_nextyear,  # 次年度参考価格注釈データ(配列)
            "offer_price_sum": "¥{:,}".format(
                estimateobj.main_offer_price_sum
            ),  # 本見積合計金額
            "sub1_offer_price_sum": "¥{:,}".format(
                estimateobj.sub1_offer_price_sum
            ),  # 参考見積合計金額
            "sub2_offer_price_sum": "¥{:,}".format(
                estimateobj.sub2_offer_price_sum
            ),  # 次年度考見積合計金額
            "footer_items": footer_sentence,  # フッター文言(配列)
            "stamp_1_id": auth2_stamp_path,  # 職印_左端
            "stamp_2_id": auth1_stamp_path,  # 職印_中央
            "stamp_3_id": creater_stamp_path,  # 職印_右端

        }
        return forti_data

        # Todo 見積IDから辞書型データを作成 終了-------------------------------------------------------------------------





