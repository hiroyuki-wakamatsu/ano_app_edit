import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import ZnwQuotationNumbering
from .models import (
    # FtnQuoteHeader,
    ZnwMasterEmployee,
    # ZnwQuoteApproval,
    # ZnwApprovalCondition,
    # ZnwQuoteApprovalHistory,
)
from PIL import Image, ImageDraw, ImageFont
# from quotepdfapp.views.estimatepdf_const import FONT_DEFAULT_PATH
import logging

logger = logging.getLogger(__name__)


def get_quotation_number(base_quotation_number, employee_no, specified_date):
    """
    社員番号と指定日付を元に見積番号を生成します。既に同じ基本の見積番号が存在する場合は、その番号に"-I"を追加して返します。

    引数:
        base_quotation_number (str): 既に存在する場合の基本となる見積番号。
        employee_no (str): 見積番号生成に使用する6桁の社員番号。
        specified_date (datetime.date): 見積番号生成に使用する日付。

    戻り値:
        str: 生成された見積番号。所属部門の略称、社員番号の下3桁、'Z'、日付（年月日）、通し番号（3桁）、'-00'の組み合わせとなります。

    例外:
        ObjectDoesNotExist: 社員番号が存在しない場合に発生します。
    """
    # 引数1に値が入っている場合、元の引数に"-I"を追加して処理終了
    if base_quotation_number:
        return base_quotation_number + "-I"

    # 社員マスタから所属部門のdept_name_short, update_userを取得
    try:
        employee = ZnwMasterEmployee.objects.get(employee_no=employee_no)
        department_alphabet = employee.dept.dept_name_short
        update_user = employee.user.username
    except ZnwMasterEmployee.DoesNotExist:
        logger.error(f"見積番号生成処理関数の実行中にエラーが発生しました:該当する社員番号が存在しません: {employee_no}")
        return ""

    # 引数2と引数3を使用してznw_quotation_numberingの該当レコードを検索、quotation_numを取得
    record, created = ZnwQuotationNumbering.objects.get_or_create(
        employee_no=employee_no,
        quotation_num_date=specified_date,
        defaults={
            "quotation_num": 0,
            "create_user": update_user,
            "create_date": datetime.now(),
            "update_user": update_user,
            "update_date": datetime.now(),
            "is_deleted": 0,
        },
    )

    # quotation_numのカウントを1アップ、update_userに引数４を、update_dateに現在の日時を指定してレコードを更新
    record.quotation_num += 1
    record.update_user = update_user
    record.update_date = datetime.now()
    record.save()

    # 見積番号を生成
    quotation_number = (
        f"{department_alphabet}{employee_no[-3:]}Z{specified_date.strftime('%y%m%d')}"
        f"{record.quotation_num:03}-00"
    )

    # 見積番号を戻り値にして処理終了
    return quotation_number


# def get_approval_status(quote_header_id: int):
#     """
#     見積書ヘッダIDを基に、その見積書の承認状態と関連する承認者情報を取得します。

#     引数:
#         quote_header_id (int): 承認状態と関連する承認者情報を取得する見積書ヘッダのID。

#     戻り値:
#         tuple:
#             - (str): 見積書の現在の承認状態。"承認申請中", "承認中", "差戻し", "承認完了"のいずれか。
#             - (list): 承認者情報のリスト。各要素は[承認者の社員番号, 承認状態, 承認日, コメント]の形式。
#             - (bool): 再申請フラグ。再申請の場合はTrue。
#             - (str): 再申請時のコメント内容。

#     例外:
#         ObjectDoesNotExist: 該当の見積書ヘッダや関連する承認情報がデータベースに存在しない場合に発生。
#     """
#     try:
#         # ヘッダ情報を取得
#         quote_header = FtnQuoteHeader.objects.get(pk=quote_header_id)
#         # 承認状態情報を取得
#         approval_info = ZnwQuoteApproval.objects.get(quote_header=quote_header)

#         # 承認条件から承認回数を取得
#         approval_condition = ZnwApprovalCondition.objects.get(
#             pk=approval_info.approval_condition_id
#         )
#         approval_count = approval_condition.approval_count

#         # 営業情報を取得し、結果リストに追加
#         sales_user = User.objects.get(username=approval_info.create_user)
#         sales_rep = ZnwMasterEmployee.objects.get(user=sales_user)

#         # 承認者情報とその状況を格納するリストを初期化
#         authorizer_status = [
#             [sales_rep.employee_no, "承認申請", approval_info.create_date, None]
#         ]

#         # 再帰問い合わせで承認フローを取得
#         approver = sales_rep
#         for i in range(approval_count):
#             approver = ZnwMasterEmployee.objects.get(
#                 employee_no=approver.superior_employee_no
#             )

#             # status, comment, dateを取得
#             status = getattr(approval_info, f"status{i+1}", None)
#             comment = getattr(approval_info, f"approval_comment{i+1}", None)
#             date = getattr(approval_info, f"approval_date{i+1}", None)

#             # 承認者にスキップフラグが立っている場合
#             if approver.irregular_approval_flow_flag:
#                 if status is None:
#                     # 承認者がスキップフラグ立っているかつ、承認情報がない場合は、"不在"とする
#                     authorizer_status.append([approver.employee_no, "不在", None, None])
#                 else:
#                     # 承認者のスキップフラグ立っているが、承認実情報がある場合、実情報をもとに
#                     # データを作成する。
#                     authorizer_status.append(
#                         [approver.skip_approver_no, status, date, comment]
#                     )
#                     # 承認実情報にそって、次の承認者情報を書き換える
#                     approver = ZnwMasterEmployee.objects.get(
#                         employee_no=approver.skip_approver_no
#                     )
#             else:
#                 if status == "承認中":  # 文字読み替え
#                     status = "承認"
#                 authorizer_status.append([approver.employee_no, status, date, comment])

#         # 最終的な承認状態を取得
#         approval_status = approval_info.approval_result
#         reapplication_flag = approval_info.reapplication_flag
#         reapplication_comment = approval_info.reapplication_comment

#         return (
#             approval_status,
#             authorizer_status,
#             reapplication_flag,
#             reapplication_comment,
#         )

#     except ObjectDoesNotExist:
#         # 該当の見積書ヘッダや承認情報が存在しない場合
#         return None, [], None, None


# def quotation_approval_request(
#     employee_no: str,
#     quote_header_id: int,
#     approval_condition_id: int,
#     reapplication_comment: str = None,
# ):
#     """
#     指定した見積書に対して、承認の依頼を行います。既存の承認依頼情報が存在する場合、履歴テーブルにコピーした後、新しい承認依頼情報を作成します。

#     引数:
#         employee_no (str): 承認依頼を行う社員の社員番号。
#         quote_header_id (int): 承認依頼を行う見積書ヘッダのID。
#         approval_condition_id (int): 承認依頼時に参照する承認条件のID。
#         reapplication_comment (str, 任意): 再申請の際のコメント。

#     戻り値:
#         tuple:
#             - (str): 全体の承認結果のステータス。
#             - (list): 承認者ごとのステータス情報のリスト。各要素は[承認者のユーザー名, ステータス, 承認日, コメント]の形式。

#     例外:
#         ObjectDoesNotExist: 社員情報や見積書ヘッダ情報、承認条件がデータベースに存在しない場合に発生。
#     """
#     # 再申請Workフラグ初期化
#     reapplication_flag_wk = False
#     # 社員情報を取得
#     try:
#         employee = ZnwMasterEmployee.objects.get(employee_no=employee_no)
#         update_user = employee.user.username
#     except ZnwMasterEmployee.DoesNotExist:
#         logger.error(f"見積書承認依頼処理関数の実行時にエラーが発生しました: 社員マスタに該当社員データがありません: {employee_no}")
#         return None, [], None, None

#     # 上長の社員番号を取得
#     try:
#         superior_employee = ZnwMasterEmployee.objects.get(
#             employee_no=employee.superior_employee_no
#         )
#     except ZnwMasterEmployee.DoesNotExist:
#         logger.info(f"見積書承認依頼処理:上長社員番号が設定されていません: {employee.superior_employee_no}")
#         # 上長社員番号がない場合、Noneを設定
#         superior_employee = None

#     # 見積書ヘッダ情報を取得
#     try:
#         quote_header = FtnQuoteHeader.objects.get(id=quote_header_id)
#     except FtnQuoteHeader.DoesNotExist:
#         logger.error(f"見積書承認依頼処理関数の実行時にエラーが発生しました: 該当する見積書が存在しません: {quote_header_id}")
#         return None, [], None, None

#     # 再申請のパターン
#     # 既存の見積書承認状態情報があれば、バックアップテーブルにコピーして削除
#     # 見積書承認状態情報テーブルに同じデータが存在する場合
#     if ZnwQuoteApproval.objects.filter(quote_header_id=quote_header_id).exists():
#         # ZnwQuoteApprovalのレコードを取得
#         znw_quote_approval = ZnwQuoteApproval.objects.get(
#             quote_header_id=quote_header_id
#         )
#         # _stateを除外
#         znw_quote_approval_dict = znw_quote_approval.__dict__.copy()
#         znw_quote_approval_dict.pop("_state")
#         try:
#             # 履歴テーブルにコピー
#             ZnwQuoteApprovalHistory.objects.create(**znw_quote_approval_dict)
#             # コピー元のデータを削除
#             znw_quote_approval.delete()
#             # 再申請フラグON
#             reapplication_flag_wk = True
#         except Exception as e:
#             logger.error(f"Error: {e}")
#             return None, [], None, None

#     # 承認条件を取得
#     try:
#         approval_condition = ZnwApprovalCondition.objects.get(
#             approval_condition=approval_condition_id
#         )
#     except ZnwApprovalCondition.DoesNotExist:
#         logger.error(
#             f"見積書承認依頼処理関数の実行時にエラーが発生しました: "
#             f"見積承認条件マスタに該当データがありません: {approval_condition_id}"
#         )
#         return None, [], None, None

#     # 見積書承認状態情報テーブルにレコードを作成
#     ZnwQuoteApproval.objects.create(
#         quote_header=quote_header,
#         approval_condition=approval_condition,
#         approver1=superior_employee,
#         status1=None,
#         approval_count=approval_condition.approval_count,
#         approval_date1=None,
#         approval_condition_kind=approval_condition_id,
#         approval_result="承認申請中",
#         reapplication_comment=reapplication_comment,
#         reapplication_flag=reapplication_flag_wk,
#         create_user=update_user,
#         create_date=datetime.now(),
#         update_user=update_user,
#         update_date=datetime.now(),
#         is_deleted=0,
#     )

#     # 見積書ヘッダのステータスを更新
#     quote_header.status = "承認申請中"
#     quote_header.save()

#     return get_approval_status(quote_header_id)


# def quotation_approval_process(
#     employee_no: str,
#     quote_header_id: int,
#     approval_status: str,
#     approval_comment: str,
# ):
#     """
#     指定された見積書に対して、承認の処理を行います。承認者の判断に基づき、見積書の承認状態を更新します。

#     引数:
#         employee_no (str): 承認処理を行う社員の社員番号。
#         quote_header_id (int): 承認処理を行う見積書ヘッダのID。
#         approval_status (str): 更新する承認状態。"承認申請中", "承認中", "承認完了", "差戻し"のいずれか。
#         approval_comment (str): 承認または差戻しの際のコメント。

#     戻り値:
#         tuple:
#             - (str): 全体の承認結果のステータス。
#             - (list): 承認者ごとのステータス情報のリスト。各要素は[承認者のユーザー名, ステータス, 承認日, コメント]の形式。

#     例外:
#         ObjectDoesNotExist: 社員情報や見積書ヘッダ情報、関連する承認情報がデータベースに存在しない場合に発生。
#     """
#     # 社員情報を取得
#     try:
#         employee = ZnwMasterEmployee.objects.get(employee_no=employee_no)
#         update_user = employee.user.username
#     except ZnwMasterEmployee.DoesNotExist:
#         logger.error(f"見積書承認処理関数の実行時にエラーが発生しました: 社員マスタに該当社員データがありません: {employee_no}")
#         return None, [], None, None

#     # 上長の社員番号を取得
#     try:
#         superior_employee = ZnwMasterEmployee.objects.get(
#             employee_no=employee.superior_employee_no
#         )
#         irregular_approval_flow_flag_wk = superior_employee.irregular_approval_flow_flag
#         skip_approver_no_wk = superior_employee.skip_approver_no
#     except ZnwMasterEmployee.DoesNotExist:
#         logger.info(f"見積書承認処理:上長社員番号が設定されていません: {employee.superior_employee_no}")
#         superior_employee = None
#         irregular_approval_flow_flag_wk = None
#         skip_approver_no_wk = None

#     # 見積書ヘッダ情報を取得
#     try:
#         quote_header = FtnQuoteHeader.objects.get(id=quote_header_id)
#     except FtnQuoteHeader.DoesNotExist:
#         logger.error(f"見積書承認処理関数の実行時にエラーが発生しました: 該当する見積書が存在しません: {quote_header_id}")
#         return None, [], None, None

#     # 承認処理
#     # 見積書承認状態情報を取得
#     try:
#         quote_approval = ZnwQuoteApproval.objects.get(quote_header=quote_header)
#     except ZnwQuoteApproval.DoesNotExist:
#         logger.error(f"見積書承認処理関数の実行時にエラーが発生しました: 該当する承認依頼データが存在しません: {quote_header}")
#         return None, [], None, None

#     # 承認状態とコメントを更新
#     current_approval_count = (
#         quote_approval.approval_condition.approval_count
#         - quote_approval.approval_count
#         + 1
#     )
#     setattr(quote_approval, f"status{current_approval_count}", approval_status)
#     setattr(
#         quote_approval,
#         f"approval_comment{current_approval_count}",
#         approval_comment,
#     )
#     setattr(
#         quote_approval,
#         f"approval_date{current_approval_count}",
#         datetime.now(),
#     )
#     approval_count_wk = quote_approval.approval_count
#     quote_approval.approval_count = approval_count_wk - 1

#     # 承認回数が0以下の場合、最後なので、最終結果を更新し、処理終了
#     if quote_approval.approval_count <= 0:  # 最後の承認者か？の確認。
#         quote_header.status = approval_status  # 見積書ヘッダのステータスを更新
#         if approval_status == "差戻し":
#             quote_approval.approval_result = "差戻し"
#         else:
#             quote_approval.approval_result = "承認完了"
#         quote_approval.update_user = update_user
#         quote_approval.update_date = datetime.now()
#         quote_approval.is_deleted = 0
#         quote_approval.save()
#         quote_header.save()
#         return get_approval_status(quote_header_id)
#     else:  # 後続に承認者がいる場合、こっち。
#         quote_header.status = approval_status
#         quote_approval.approval_result = approval_status
#         quote_approval.save()
#         quote_header.save()

#     # 承認回数が1以上かつ、現在の承認者の判断が"差戻し"の場合、後続の承認者への承認依頼はしないで処理終了
#     if approval_status == "差戻し":
#         quote_approval.update_user = update_user
#         quote_approval.update_date = datetime.now()
#         quote_approval.is_deleted = 0
#         quote_approval.save()
#         return get_approval_status(quote_header_id)

#     # 承認フロースキップフラグがtrueの場合、承認スキップ時の承認社員番号を上長社員番号として扱う
#     if irregular_approval_flow_flag_wk:
#         # 上長の社員情報を取得
#         try:
#             superior_employee = ZnwMasterEmployee.objects.get(
#                 employee_no=skip_approver_no_wk
#             )
#         except ZnwMasterEmployee.DoesNotExist:
#             logger.error(
#                 f"見積書承認処理関数の実行時にエラーが発生しました: 社員マスタに"
#                 f"該当社員データがありません(2): {skip_approver_no_wk}"
#             )
#             return None, [], None, None

#     # 自分の上長を次の承認者として、設定する
#     setattr(
#         quote_approval,
#         f"approver{current_approval_count+1}",
#         superior_employee,
#     )
#     setattr(quote_approval, f"status{current_approval_count+1}", approval_status)
#     quote_approval.approval_result = approval_status
#     quote_approval.update_user = update_user
#     quote_approval.update_date = datetime.now()
#     quote_approval.is_deleted = 0
#     quote_approval.save()

#     return get_approval_status(quote_header_id)


# class HankoGenerator:
#     """
#     電子印鑑画像の生成と管理を行うクラス。
#
#     Attributes:
#     - _FONT_DEFAULT_PATH (str): 使用するフォントのパス。
#     - HANKO_IMG (str): 電子印鑑画像の保存ディレクトリのパス。
#
#     Methods:
#     - _flattext(moji, rasio, color): 指定された色と比率で文字の画像を生成する。
#     - _getimage(moji, yohaku, color): 文字を中心に配置し、円形の枠を追加した画像を生成する。
#     - generate_hanko_image(employee_no, generate_image_flag=True):
#             社員番号を基に社員の姓を取得し、電子印鑑画像を生成またはファイルパスを返す。
#
#     # 使用例
#     hanko_gen = HankoGenerator()
#     path = hanko_gen.generate_hanko_image("12345", True)
#     """
#
#     def __init__(self):
#         self._FONT_DEFAULT_PATH = FONT_DEFAULT_PATH
#         self.HANKO_IMG = os.getcwd() + "/static/media/hanko"
#
#     def _flattext(self, moji, rasio, color):
#         """
#         文字を指定された色と比率で画像として生成します。
#
#         Parameters:
#         - moji (str): 画像化する文字。
#         - rasio (float): 文字の扁平率（高さの縮小比率）。
#         - color (str): 文字の色。
#
#         Returns:
#         - Image: 生成された文字の画像。
#         - tuple: 生成された画像のサイズ。
#         """
#
#         base_W, base_H = (320, 320)  # 画像の基本サイズを定義
#         # 画像の背景色を設定
#         if color == "black":
#             image = Image.new("L", (base_W, base_H), "white")
#         else:
#             image = Image.new("RGBA", (base_W, base_H), (255, 255, 255, 0))
#
#         d = ImageDraw.Draw(image)  # 画像上に描画するためのオブジェクトを生成
#         fontpath = self._FONT_DEFAULT_PATH  # フォントのパスを設定
#         font = ImageFont.truetype(fontpath, 200)  # フォントオブジェクトを生成
#         moji_W, moji_H = d.textsize(moji, font=font)  # 文字のサイズを取得
#         d.text((0, 0 - (moji_H - moji_W)), moji, font=font, fill=color)  # 文字を画像上に描画
#         image_crop = image.crop((0, 0, moji_W, moji_H))  # 文字部分だけの画像に切り抜き
#         image_resize = image_crop.resize((moji_W, int(moji_H * rasio)))  # 画像をリサイズ
#
#         return image_resize, (moji_W, int(moji_H * rasio))
#
#     def _getimage(self, moji, yohaku, color):
#         """
#         文字を中心に配置し、円形の枠を追加した画像を生成します。
#
#         Parameters:
#         - moji (str): 画像化する文字。
#         - yohaku (int): 円形の枠の余白。
#         - color (str): 文字および円形の枠の色。
#
#         Returns:
#         - Image: 生成された画像。
#         - tuple: 生成された画像のサイズ。
#         """
#
#         base_W, base_H = (320, 320)  # 画像の基本サイズを定義
#         # 画像の背景色を設定
#         if color == "black":
#             base_image = Image.new("L", (base_W, base_H), "white")
#         else:
#             base_image = Image.new("RGBA", (base_W, base_H), (255, 255, 255, 0))
#
#         d = ImageDraw.Draw(base_image)  # 画像上に描画するためのオブジェクトを生成
#
#         # mojiが1文字の場合
#         if len(moji) == 1:
#             rasio = 1.0  # 扁平率を設定
#             # 文字を画像化
#             image, (image_W, image_H) = self._flattext(moji, rasio, color)
#             # 文字画像を中心に配置するための座標を計算
#             paste_W = int((base_W - image_W) / 2)
#             paste_H = int((base_H - image_H) / 2)
#             base_image.paste(image, (paste_W, paste_H))  # 文字画像を貼り付け
#
#         # mojiが2文字の場合
#         elif len(moji) == 2:
#             rasio = 0.65  # 扁平率を設定
#             # 1文字目を画像化
#             image, (image_W, image_H) = self._flattext(moji[0], rasio, color)
#             # 1文字目の画像を上部中央に配置するための座標を計算
#             paste_W = int((base_W - image_W) / 2)
#             paste_H = int(((base_H / 2) - image_H) / 2) + yohaku
#             base_image.paste(image, (paste_W, paste_H))  # 1文字目の画像を貼り付け
#
#             # 2文字目を画像化
#             image, (image_W, image_H) = self._flattext(moji[1], rasio, color)
#             # 2文字目の画像を下部中央に配置するための座標を計算
#             paste_W = int((base_W - image_W) / 2)
#             paste_H = int(((base_H / 2) - image_H) / 2) + int((base_H / 2)) - yohaku
#             base_image.paste(image, (paste_W, paste_H))  # 2文字目の画像を貼り付け
#
#         # mojiが3文字以上の場合
#         else:
#             rasio = 0.4  # 扁平率を設定
#             for i, char in enumerate(moji[:3]):  # 最初の3文字のみ使用
#                 image, (image_W, image_H) = self._flattext(char, rasio, color)  # 文字を画像化
#                 # 文字画像を等間隔に配置するための座標を計算
#                 paste_W = int((base_W - image_W) / 2)
#                 paste_H = int(i * (base_H / 3) + (base_H / 3 - image_H) / 2)
#                 base_image.paste(image, (paste_W, paste_H))  # 文字画像を貼り付け
#
#         # 円形の枠を描画
#         d.ellipse(
#             [(yohaku, yohaku), (base_W - yohaku, base_H - yohaku)],
#             outline=color,
#             width=6,
#         )
#         return base_image, (base_W, base_H)
#
#     def generate_hanko_image(self, employee_no, generate_image_flag=True):
#         """
#         社員番号を基に社員の姓を取得し、電子印鑑画像を生成またはファイルパスを返します。
#
#         Parameters:
#         - employee_no (str): 社員番号。
#         - generate_image_flag (bool): 画像生成フラグ。Trueの場合、新たに画像を生成。Falseの場合、ファイルパスのみ返す。
#
#         Returns:
#         - str: 生成された電子印鑑画像のファイルパス、または既存のファイルパス。
#         """
#
#         file_path = f"{self.HANKO_IMG}/{employee_no}_hanko.png"
#
#         if not generate_image_flag:
#             # 画像生成フラグがFalseの場合、ファイルパスのみを返す
#             return file_path
#
#         # データベースからユーザ情報を取得
#         employee = ZnwMasterEmployee.objects.filter(employee_no=employee_no).first()
#         if not employee:
#             # 該当する社員情報がない場合はエラーログを出力
#             logger.error(
#                 f"電子印鑑画像生成関数の実行時にエラーが発生しました: 社員マスタに該当社員データがありません: {employee_no}"
#             )
#             return None
#
#         last_name = employee.employee_name.split()[0]  # 社員の姓を取得
#
#         yohaku = 10  # 円形の枠の余白を設定
#         # 黒と白の画像を生成
#         grayscale_image, (base_W, base_H) = self._getimage(last_name, yohaku, "black")
#         whiteback_image = Image.new("L", grayscale_image.size, "white")  # 白背景の画像を生成
#         waku_image = Image.new("L", grayscale_image.size, 0)  # 黒背景の画像を生成
#         d = ImageDraw.Draw(waku_image)  # 画像上に描画するためのオブジェクトを生成
#         d.ellipse(
#             [(yohaku, yohaku), (base_W - yohaku, base_H - yohaku)], fill=255
#         )  # 円形のマスクを生成
#         # 生成したマスクを使って、黒と白の画像から印鑑画像を生成
#         mask_image = Image.composite(grayscale_image, whiteback_image, waku_image)
#
#         # 赤色の画像を生成
#         color_image, (base_W, base_H) = self._getimage(last_name, yohaku, "red")
#         transparent_image = Image.new(
#             "RGBA", color_image.size, (255, 255, 255, 0)
#         )  # 透明背景の画像を生成
#         # 生成したマスクを使って、赤色の画像から最終的な印鑑画像を生成
#         hanko_image = Image.composite(transparent_image, color_image, mask_image)
#         hanko_image.save(file_path)  # 印鑑画像を保存
#
#         return file_path
