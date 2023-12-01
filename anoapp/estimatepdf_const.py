import os
from reportlab.lib.units import mm


# 説明：estimatepdf_funcモジュールのPrivate変数として使用

# 会社情報
COMPANY_NAME = "図研ネットウエイブ株式会社"
COMPANY_ADDRESS = "〒222-8505 横浜市港北区新横浜3-1-1"
COMPANY_TEL = "Tel: 045-473-6821"
COMPANY_FAX = "Fax: 045-473-1782"

# デフォルトのフォントを宣言
FONT_DEFAULT_NAME = "MS Mincho"
# FONT_DEFAULT_PATH = "./Fonts/msmincho.ttc"
FONT_DEFAULT_PATH = "msmincho.ttc"

# 基準となるグリッドの縦横を格納
GRID_Y = 6.35 * mm
GRID_X = 6.76 * mm

# コンテンツを表示できる一番下のY座標
END_Y = 6 * mm

# コンテンツ表示でリセットするY座標
TOP_Y = 298.10 * mm

# コンテンツテーブル左右のX座標
LEFT_X = 4 * mm
RIGHT_X = 205.80 * mm

# コンテンツテーブル縦線の区切り位置のX座標
VERTICAL_X1 = 9.76 * mm  # 項(右線)
VERTICAL_X2 = 75.00 * mm  # 品名(右線)
VERTICAL_X3 = 118.00 * mm  # 型番(右線)
VERTICAL_X4 = 125.00 * mm  # 数量(右線)
VERTICAL_X5 = 145.00 * mm  # 標準価格(右線)
VERTICAL_X6 = 154.00 * mm  # 仕切率(右線)
VERTICAL_X7 = 175.00 * mm  # ご提供単価(右線)
VERTICAL_X8 = 194.00 * mm  # ご提供価格(右線)

# コンテンツの表示パディング
PADDING_BOTTOM = 0.5 * mm

# 描画座標位置
# ヘッダータイトル座標
HEADER_TITLE_X = 83.74 * mm
HEADER_TITLE_Y = 287.40 * mm

# ヘッダーお客様名座標
HEADER_CLIENT_X = 12.76 * mm
HEADER_CLIENT_Y = 221.90 * mm

# ヘッダー見積番号座標
HEADER_ESTIMATE_NUM_X = 154.72 * mm
HEADER_ESTIMATE_NUM_Y = 279.05 * mm

# ヘッダーZNW情報座標
HEADER_ZNW_INFO_X = 141.20 * mm
HEADER_ZNW_INFO_Y = 247.30 * mm

# ヘッダーZNW会社印枠座標
HEADER_ZNW_SEAL_FLAME_X = 141.20 * mm
HEADER_ZNW_SEAL_FLAME_Y = 221.90 * mm

# ヘッダーZNW会社印座標
HEADER_ZNW_SEAL_X = 185.00 * mm
HEADER_ZNW_SEAL_Y = 247.30 * mm

# ヘッダーZNW職印座標
HEADER_EMPLOYEE_SEAL_X = 138 * mm
HEADER_EMPLOYEE_SEAL_Y = 221.90 * mm

# 本見積コンテンツ座標
FINAL_ESTIMATE_BODY_X = 12.76 * mm
FINAL_ESTIMATE_BODY_Y = 209.20 * mm

# テーブル改行閾値(半角文字何個分)
MAX_ZNW_SKU_JP = 45  # 品名の改行文字数の閾値
MAX_ZNW_SKU = 29  # 型番の改行文字数の閾値
MAX_ANNO_DATA = 137  # 注釈の改行文字数の閾値

# フッター文字改行の閾値
MAX_FOOTER_SENTENCE_SIZE = 134

# 会社印のパス
# COMPANY_SEAL = os.getcwd() + "/media/company-seal.png"
COMPANY_SEAL = os.getcwd() + "/static/anoapp/media/company-seal.png"

# ドラフト文字イメージのパス
DRAFT_IMG = os.getcwd() + "/static/anoapp/media/draft.png"

# フッター固定文言
FOOTER_FIX_SENTENCE1 = "フッター文言は変更可能!!!【保守サービス基本情報確認書】"
FOOTER_FIX_SENTENCE2 = "保守サポートをご提供する上で必要となる基本情報を記入いただく書類です。"
FOOTER_FIX_SENTENCE3 = "※本書類のご提出がない場合、保守サービスのご提供及び更新のご案内ができませんので、ご注意をお願いします。"

# フッター可変文言_通常
FOOTER_VAL_SENTENCE1_NORMAL = "※この部分も変更可能!!!"
FOOTER_VAL_SENTENCE2_NORMAL = (
    "※初年度のBasicサービスの期間は、弊社製品出荷日から始まり翌年の同月末までとなります。(当月残日数＋12ヶ月)"
)

# フッター可変文言_保守用
FOOTER_VAL_SENTENCE1_HOSYU = "※ご注文の際には、必ず保守サポートIDをご明記ください。"
FOOTER_VAL_SENTENCE2_HOSYU = "※設置先様情報・御社ご担当者様にご変更のある場合は、「保守サービス基本情報確認書」のご提出をお願いいたします。"
FOOTER_VAL_SENTENCE3_HOSYU = "※ライセンス登録には、ご注文書を頂いてから約2週間程の日数が必要となります。早めのご発注をお願いいたします。"
FOOTER_VAL_SENTENCE4_HOSYU = "※保守契約期間中に中途解約をされる場合は残り期間分のご返金は致しかねますのでご了承ください。"
FOOTER_VAL_SENTENCE5_HOSYU = "【将来の消費税率引き上げに伴い保守期間が新税率の施行日をまたぐ場合、複数の税率が適用される場合があります。】"
FOOTER_VAL_SENTENCE6_HOSYU = "※上記見積金額には消費税は含まれておりません。"
