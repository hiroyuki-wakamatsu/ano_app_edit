from django.db import models
from django.contrib.auth.models import User
# from ftnapp.models import FtnQuoteHeader


class ZnwQuotationNumbering(models.Model):
    """
    見積番号採番情報モデル。
    各社員に対して、特定の日における見積番号の最大値を保存します。
    """

    employee_no = models.CharField(max_length=16, verbose_name="社員番号")
    quotation_num_date = models.DateField(verbose_name="見積番号基準日")
    quotation_num = models.IntegerField(verbose_name="日毎の見積番号現状の最大値")
    create_user = models.CharField(max_length=100, verbose_name="作成者")
    create_date = models.DateTimeField(verbose_name="作成日")
    update_user = models.CharField(max_length=100, verbose_name="更新者")
    update_date = models.DateTimeField(verbose_name="更新日")
    is_deleted = models.IntegerField(default=0, verbose_name="削除フラグ")

    class Meta:
        managed = True
        unique_together = ("employee_no", "quotation_num_date")
        db_table = "znw_quotation_numbering"
        verbose_name = verbose_name_plural = "見積番号採番情報"


class ZnwMasterDept(models.Model):
    """
    新見積システム部門マスターモデル。
    各部門の情報、およびその部門の責任者や上位部門に関する情報を保存します。
    """

    dept_cd = models.CharField(max_length=16, primary_key=True, verbose_name="部門コード")
    dept_name = models.CharField(max_length=100, verbose_name="部門名")
    manager_employee_no = models.CharField(
        null=True, blank=True, max_length=16, verbose_name="部門責任者社員番号"
    )
    parent_id = models.CharField(
        max_length=16, null=True, blank=True, verbose_name="上位部門コード"
    )
    dept_name_short = models.CharField(
        null=True, blank=True, max_length=3, verbose_name="部門名１文字"
    )
    create_user = models.CharField(max_length=100, verbose_name="作成者")
    create_date = models.DateTimeField(verbose_name="作成日")
    update_user = models.CharField(max_length=100, verbose_name="更新者")
    update_date = models.DateTimeField(verbose_name="更新日")
    is_deleted = models.IntegerField(default=0, verbose_name="削除フラグ")

    class Meta:
        managed = True
        db_table = "znw_master_dept"
        verbose_name = verbose_name_plural = "新見積システム 部門マスター"


class ZnwMasterEmployee(models.Model):
    """
    新見積システム社員マスターモデル。
    各社員の基本情報、部門、役職、上司、および特定の承認フロー関連の情報を保存します。
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_no = models.CharField(max_length=16, primary_key=True, verbose_name="社員番号")
    employee_name = models.CharField(max_length=100, verbose_name="社員氏名")
    dept = models.ForeignKey(
        ZnwMasterDept,
        on_delete=models.SET_NULL,
        db_column="dept_cd",
        verbose_name="部門コード",
        null=True,
        blank=True,
    )
    position = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="役職"
    )
    superior_employee_no = models.CharField(
        max_length=16, null=True, blank=True, verbose_name="上長社員番号"
    )
    skip_approver_no = models.CharField(
        max_length=16, null=True, blank=True, verbose_name="承認スキップ時の承認社員番号"
    )
    irregular_approval_flow_flag = models.BooleanField(
        default=False, verbose_name="承認フロースキップフラグ"
    )
    create_user = models.CharField(max_length=100, verbose_name="作成者")
    create_date = models.DateTimeField(verbose_name="作成日")
    update_user = models.CharField(max_length=100, verbose_name="更新者")
    update_date = models.DateTimeField(verbose_name="更新日")
    is_deleted = models.IntegerField(default=0, verbose_name="削除フラグ")

    class Meta:
        managed = True
        db_table = "znw_master_employee"
        verbose_name = verbose_name_plural = "新見積システム 社員マスター"



# # 見積書承認条件マスタ
# class ZnwApprovalCondition(models.Model):
#     """
#     見積書承認条件マスタモデル。
#     見積書の承認に関連する条件や基準、権限に関する情報を保存します。
#     """

#     # 承認条件ID
#     approval_condition = models.IntegerField(verbose_name="承認条件")
#     # 判断基準
#     judgment_criteria = models.CharField(max_length=24, verbose_name="判断基準")
#     # 権限事項
#     authority_matter = models.CharField(max_length=64, verbose_name="権限事項")
#     # 起案
#     draft = models.CharField(
#         max_length=100, blank=True, null=True, default="担当営業", verbose_name="起案"
#     )
#     # 承認残回数
#     approval_count = models.IntegerField(default=0, verbose_name="承認残回数")

#     create_user = models.CharField(max_length=100, verbose_name="作成者")
#     create_date = models.DateTimeField(verbose_name="作成日")
#     update_user = models.CharField(max_length=100, verbose_name="更新者")
#     update_date = models.DateTimeField(verbose_name="更新日")
#     is_deleted = models.IntegerField(default=0, verbose_name="削除フラグ")

#     class Meta:
#         managed = True
#         db_table = "znw_approval_condition"
#         verbose_name = verbose_name_plural = "見積書承認条件マスター"


# # 見積書承認状態情報テーブル
# class ZnwQuoteApproval(models.Model):
#     """
#     見積書承認状態情報モデル。
#     各見積書の現在の承認状態、承認者、コメントなどの承認関連の詳細情報を保存します。
#     """

#     APPROVAL_STATUS_CHOICES = [
#         ("承認申請", "承認申請"),
#         ("承認中", "承認中"),
#         ("承認", "承認"),
#         ("差戻し", "差戻し"),
#     ]
#     APPROVAL_RESULT_CHOICES = [
#         ("承認申請中", "承認申請中"),  # 営業が承認申請した場合のみ
#         ("承認中", "承認中"),  # 差戻しが無く承認が進む場合
#         ("承認完了", "承認完了"),  # 全ての承認者の承認が完了した場合
#         ("差戻し", "差戻し"),  # 承認者の一人でも差し戻した場合
#     ]
#     # 見積書ヘッダテーブルとのリレーション
#     quote_header = models.ForeignKey(FtnQuoteHeader, on_delete=models.CASCADE)
#     # 承認条件テーブルとのリレーション
#     approval_condition = models.ForeignKey(
#         ZnwApprovalCondition,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     # 承認者1～5（社員マスタテーブルとのリレーション）
#     approver1 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver1",
#         null=True,
#         blank=True,
#     )
#     approver2 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver2",
#         null=True,
#         blank=True,
#     )
#     approver3 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver3",
#         null=True,
#         blank=True,
#     )
#     approver4 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver4",
#         null=True,
#         blank=True,
#     )
#     approver5 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver5",
#         null=True,
#         blank=True,
#     )
#     # 承認状態1～5
#     status1 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         default="承認申請中",
#         verbose_name="承認状態1",
#         null=True,
#         blank=True,
#     )
#     status2 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態2",
#         null=True,
#         blank=True,
#     )
#     status3 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態3",
#         null=True,
#         blank=True,
#     )
#     status4 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態4",
#         null=True,
#         blank=True,
#     )
#     status5 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態5",
#         null=True,
#         blank=True,
#     )
#     # 承認否認コメント1～5
#     approval_comment1 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント1"
#     )
#     approval_comment2 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント2"
#     )
#     approval_comment3 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント3"
#     )
#     approval_comment4 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント4"
#     )
#     approval_comment5 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント5"
#     )
#     # 承認否認日時1～5
#     approval_date1 = models.DateTimeField(verbose_name="承認否認日時1", null=True, blank=True)
#     approval_date2 = models.DateTimeField(verbose_name="承認否認日時2", null=True, blank=True)
#     approval_date3 = models.DateTimeField(verbose_name="承認否認日時3", null=True, blank=True)
#     approval_date4 = models.DateTimeField(verbose_name="承認否認日時4", null=True, blank=True)
#     approval_date5 = models.DateTimeField(verbose_name="承認否認日時5", null=True, blank=True)
#     # 承認条件
#     approval_condition_kind = models.IntegerField(verbose_name="承認条件")
#     # 承認残回数
#     approval_count = models.IntegerField(default=0, verbose_name="承認残回数")
#     # 最終承認結果
#     approval_result = models.CharField(
#         max_length=32,
#         blank=True,
#         null=True,
#         verbose_name="最新承認結果",
#         choices=APPROVAL_RESULT_CHOICES,
#     )
#     # 再承認申請フラグ
#     reapplication_flag = models.BooleanField(default=False, verbose_name="再承認申請フラグ")
#     # 再承認申請コメント
#     reapplication_comment = models.TextField(
#         blank=True, null=True, verbose_name="再承認申請コメント"
#     )

#     create_user = models.CharField(max_length=100, verbose_name="作成者")
#     create_date = models.DateTimeField(verbose_name="作成日")
#     update_user = models.CharField(max_length=100, verbose_name="更新者")
#     update_date = models.DateTimeField(verbose_name="更新日")
#     is_deleted = models.IntegerField(default=0, verbose_name="削除フラグ")

#     class Meta:
#         managed = True
#         db_table = "znw_quote_approval"
#         verbose_name = verbose_name_plural = "見積書承認状態情報"


# class ZnwQuoteApprovalHistory(models.Model):
#     """
#     見積書承認状態情報履歴モデル。
#     各見積書の承認状態の変更履歴を保存します。承認、差戻し、コメントの変更などの情報が含まれます。
#     """

#     APPROVAL_STATUS_CHOICES = [
#         ("承認申請", "承認申請"),
#         ("承認中", "承認中"),
#         ("承認", "承認"),
#         ("差戻し", "差戻し"),
#     ]
#     APPROVAL_RESULT_CHOICES = [
#         ("承認申請中", "承認申請中"),  # 営業が承認申請した場合のみ
#         ("承認中", "承認中"),  # 差戻しが無く承認が進む場合
#         ("承認完了", "承認完了"),  # 全ての承認者の承認が完了した場合
#         ("差戻し", "差戻し"),  # 承認者の一人でも差し戻した場合
#     ]
#     # 見積書ヘッダテーブルとのリレーション
#     quote_header = models.ForeignKey(
#         FtnQuoteHeader,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     # 承認条件テーブルとのリレーション
#     approval_condition = models.ForeignKey(
#         ZnwApprovalCondition,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     # 承認者1～5（社員マスタテーブルとのリレーション）
#     approver1 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver1_h",
#         null=True,
#         blank=True,
#     )
#     approver2 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver2_h",
#         null=True,
#         blank=True,
#     )
#     approver3 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver3_h",
#         null=True,
#         blank=True,
#     )
#     approver4 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver4_h",
#         null=True,
#         blank=True,
#     )
#     approver5 = models.ForeignKey(
#         ZnwMasterEmployee,
#         on_delete=models.SET_NULL,
#         related_name="approver5_h",
#         null=True,
#         blank=True,
#     )
#     # 承認状態1～5
#     status1 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         default="承認申請中",
#         verbose_name="承認状態1",
#         null=True,
#         blank=True,
#     )
#     status2 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態2",
#         null=True,
#         blank=True,
#     )
#     status3 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態3",
#         null=True,
#         blank=True,
#     )
#     status4 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態4",
#         null=True,
#         blank=True,
#     )
#     status5 = models.CharField(
#         max_length=20,
#         choices=APPROVAL_STATUS_CHOICES,
#         verbose_name="承認状態5",
#         null=True,
#         blank=True,
#     )
#     # 承認否認コメント1～5
#     approval_comment1 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント1"
#     )
#     approval_comment2 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント2"
#     )
#     approval_comment3 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント3"
#     )
#     approval_comment4 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント4"
#     )
#     approval_comment5 = models.TextField(
#         blank=True, null=True, verbose_name="承認否認コメント5"
#     )
#     # 承認否認日時1～5
#     approval_date1 = models.DateTimeField(verbose_name="承認否認日時1", null=True, blank=True)
#     approval_date2 = models.DateTimeField(verbose_name="承認否認日時2", null=True, blank=True)
#     approval_date3 = models.DateTimeField(verbose_name="承認否認日時3", null=True, blank=True)
#     approval_date4 = models.DateTimeField(verbose_name="承認否認日時4", null=True, blank=True)
#     approval_date5 = models.DateTimeField(verbose_name="承認否認日時5", null=True, blank=True)
#     # 承認条件
#     approval_condition_kind = models.IntegerField(
#         null=True, blank=True, verbose_name="承認条件"
#     )
#     # 承認残回数
#     approval_count = models.IntegerField(default=0, verbose_name="承認残回数")
#     # 最終承認結果
#     approval_result = models.CharField(
#         max_length=8,
#         blank=True,
#         null=True,
#         verbose_name="最終承認結果",
#         choices=APPROVAL_RESULT_CHOICES,
#     )
#     # 再承認申請フラグ
#     reapplication_flag = models.BooleanField(default=False, verbose_name="再承認申請フラグ")
#     # 再承認申請コメント
#     reapplication_comment = models.TextField(
#         blank=True, null=True, verbose_name="再承認申請コメント"
#     )

#     create_user = models.CharField(max_length=100, verbose_name="作成者")
#     create_date = models.DateTimeField(verbose_name="作成日")
#     update_user = models.CharField(max_length=100, verbose_name="更新者")
#     update_date = models.DateTimeField(verbose_name="更新日")
#     is_deleted = models.IntegerField(default=0, verbose_name="削除フラグ")

#     class Meta:
#         managed = True
#         # 重複レコードを許可
#         unique_together = []

#         db_table = "znw_quote_approval_history"
#         verbose_name = verbose_name_plural = "見積書承認状態情報履歴"
