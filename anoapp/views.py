from django.shortcuts import render, redirect, reverse
from django.forms import formset_factory, inlineformset_factory
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required  # 追加


from django.http import HttpResponse
import json
import base64

# pdfプレビュー関連
from .estimatepdf_main import ExeMakeEstimatePdf
from django.http import HttpResponse

# add
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from .models import (
    AnotherQuotationHeader,
    AnotherQuotationMain,
    AnotherQuotationNotes,
    AnotherQuotationConfirm,
)

from .forms import (
    AnotherHeaderForm,
    AnotherMainForm,
    AnotherNotesForm,
    AnotherConfirmForm,
    AnotherMainFormSet,
    AnotherNotesFormSet,
    AnotherConfirmFormSet,
)

from django.urls import reverse_lazy

from django.forms import modelformset_factory, inlineformset_factory

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


####### クラスVIEW定義 ############################
#
#
# 01_その他プロダクト見積書_一覧画面
#
class QuotationListlView(LoginRequiredMixin, ListView):
    # 表示するtemplate名称
    template_name = "anoapp/quotation_list.html"
    # 利用モデル
    model = AnotherQuotationHeader

    # quotation_id列を降順に並べ替え
    header_list = model.objects.order_by(F("quotation_id").desc())

    # レコード情報をテンプレートに渡すオブジェクト(指定のモデルのオブジェクトを含むクエリセット)
    context_object_name = "header_list"

    # 1ページあたりの表示レコード件数
    paginate_by = 12

    # ページネーションを行う場合にqueryset属性
    queryset = AnotherQuotationHeader.objects.order_by(F("quotation_id").desc())


# 02_その他プロダクト見積書_新規作成画面
#
class HeaderCreateView(LoginRequiredMixin, CreateView):
    model = AnotherQuotationHeader
    form_class = AnotherHeaderForm
    template_name = "anoapp/quotation_create.html"

    def get_success_url(self):
        # 保存して戻るボタン
        if "save_and_back" in self.request.POST.values():
            return reverse_lazy("list-page")
        # 保存してするボタン
        else:
            return reverse_lazy("header_main_update", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 新規作成画面は初期行を5行に設定
        AnotherMainFormSet = inlineformset_factory(
            AnotherQuotationHeader,
            AnotherQuotationMain,
            form=AnotherMainForm,
            extra=5,  # extraを設定
            can_delete=True,
        )
        AnotherNotesFormSet = inlineformset_factory(
            AnotherQuotationHeader,
            AnotherQuotationNotes,
            form=AnotherNotesForm,
            extra=2,  # extraを設定
        )
        AnotherConfirmFormSet = inlineformset_factory(
            AnotherQuotationHeader,
            AnotherQuotationConfirm,
            form=AnotherConfirmForm,
            extra=2,  # extraを設定
        )
        if self.request.POST:
            context["main_formset"] = AnotherMainFormSet(self.request.POST)
            context["notes_formset"] = AnotherNotesFormSet(self.request.POST)
            context["confirm_formset"] = AnotherConfirmFormSet(self.request.POST)
        else:
            context["main_formset"] = AnotherMainFormSet()
            context["notes_formset"] = AnotherNotesFormSet()
            context["confirm_formset"] = AnotherConfirmFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        main_formset = context["main_formset"]
        notes_formset = context["notes_formset"]
        confirm_formset = context["confirm_formset"]

        if (
            form.is_valid()
            and main_formset.is_valid()
            and notes_formset.is_valid()
            and confirm_formset.is_valid()
        ):
            self.object = form.save()
            main_formset.instance = self.object
            main_formset.save()
            notes_formset.instance = self.object
            notes_formset.save()
            confirm_formset.instance = self.object
            confirm_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(
                form,
                main_formset=main_formset,
                notes_formset=notes_formset,
                confirm_formset=confirm_formset,
            )

    def form_invalid(
        self, form, main_formset=None, notes_formset=None, confirm_formset=None
    ):
        context = self.get_context_data(
            form=form,
            main_formset=main_formset,
            notes_formset=notes_formset,
            confirm_formset=confirm_formset,
        )
        return self.render_to_response(context)


# 03_その他プロダクト見積書_修正画面
#
class HeaderUpdateView(LoginRequiredMixin, UpdateView):
    model = AnotherQuotationHeader
    form_class = AnotherHeaderForm
    template_name = "anoapp/quotation_update.html"

    # 保存して戻る場合
    # success_url = reverse_lazy("list-page")

    # 保存して画面はそのままの場合
    # def get_success_url(self):
    #    return reverse_lazy("header_main_update", args=[self.object.pk])

    #
    def get_success_url(self):
        # 保存して戻るボタン
        if "save_and_back" in self.request.POST.values():
            return reverse_lazy("list-page")
        # 保存してするボタン
        else:
            return reverse_lazy("header_main_update", args=[self.object.pk])

    # GET、POSTリクエスト時。リクエストにより処理分岐
    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを生成します。
        POSTリクエストの場合、POSTデータからフォームセットを生成します。
        GETリクエストの場合、空のフォームセットを生成します。
        """
        context = super().get_context_data(**kwargs)

        # 製品フォーム
        context["main_formset"] = AnotherMainFormSet(
            self.request.POST or None, instance=self.object
        )
        # 注釈フォーム
        context["notes_formset"] = AnotherNotesFormSet(
            self.request.POST or None, instance=self.object
        )
        # 社内確認欄フォーム
        context["confirm_formset"] = AnotherConfirmFormSet(
            self.request.POST or None, instance=self.object
        )
        return context

    # POSTリクエスト時
    # 各種フォームのバリデーションチェック
    def form_valid(self, form):
        # あなたが提供されたviewの定義
        context = self.get_context_data()
        main_formset = context["main_formset"]
        notes_formset = context["notes_formset"]
        confirm_formset = context["confirm_formset"]

        # 全てのフォームとフォームセットのバリデーションチェック
        if (
            form.is_valid()
            and main_formset.is_valid()
            and notes_formset.is_valid()
            and confirm_formset.is_valid()
        ):
            # 1_HeaderModelFormの保存
            #
            self.object = form.save()

            # 2_MainFormSetの保存
            #
            # MainFormSetの削除対象ModelFormを取得
            # メモ：inlines.jsのDELETEレコード。これがTRUEなら削除対象となる
            #       削除チェックボックスにチェックをしないと"DELETE"変数はcleaned_dateに現れないのでこのチェックをしてる
            deleted_main_forms = [
                f.instance for f in main_formset if f.cleaned_data.get("DELETE")
            ]

            # MainFormSetの保存
            main_formset.instance = self.object
            main_formset.save()

            # MainModelFormの保存
            for f in main_formset:
                f.save()

            # MainFormSetの削除対象ModelFormを削除
            for f in deleted_main_forms:
                f.delete()

            # 3_NotesFormSetの保存
            #
            # NotesFormSetの削除対象ModelFormを取得
            # メモ：inlines.jsのDELETEレコード。これがTRUEなら削除対象となる
            #       削除チェックボックスにチェックをしないと"DELETE"変数はcleaned_dateに現れないのでこのチェックをしてる
            deleted_notes_forms = [
                f.instance for f in notes_formset if f.cleaned_data.get("DELETE")
            ]

            # NotesFormSetの保存
            notes_formset.instance = self.object
            notes_formset.save()

            # NotesModelFormの保存
            for f in notes_formset:
                f.save()

            # NotesFormSetの削除対象ModelFormを削除
            for f in deleted_notes_forms:
                f.delete()

            # 4_ConfirmFormSetの保存
            #
            # ConfirmFormSetの削除対象ModelFormを取得
            # メモ：inlines.jsのDELETEレコード。これがTRUEなら削除対象となる
            #       削除チェックボックスにチェックをしないと"DELETE"変数はcleaned_dateに現れないのでこのチェックをしてる
            deleted_confirm_forms = [
                f.instance for f in confirm_formset if f.cleaned_data.get("DELETE")
            ]

            # ConfirmFormSetの保存
            confirm_formset.instance = self.object
            confirm_formset.save()

            # ConfirmModelFormの保存
            for f in confirm_formset:
                f.save()

            # ConfirmFormSetの削除対象ModelFormを削除
            for f in deleted_confirm_forms:
                f.delete()

            return super().form_valid(form)

        else:
            # バリデーションエラー時は全てのフォームを返す
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    main_formset=main_formset,
                    notes_formset=notes_formset,
                    confirm_formset=confirm_formset,
                )
            )

    # POSTリクエスト時
    # フォームの値検証がNGの場合
    def form_invalid(self, form, main_formset, notes_formset, confirm_formset):
        context = self.get_context_data(
            form=form,
            main_formset=main_formset,
            notes_formset=notes_formset,
            confirm_formset=confirm_formset,
        )
        return self.render_to_response(context)


# 04_その他プロダクト見積書_レコード削除画面
#
class HeaderDeleteView(LoginRequiredMixin, DeleteView):
    """
    見積書ヘッダの削除ビュー

    モデル: AnotherQuotationHeader
    テンプレート: "anoapp/quotation_delete.html"
    成功時のリダイレクト先: "list-page"
    """

    model = AnotherQuotationHeader
    template_name = "anoapp/quotation_delete.html"
    success_url = reverse_lazy("list-page")


####### 関数VIEW定義 ############################
#
#
# その他プロダクト見積書_一覧画面 複製ドロップダウンメニュー機能
#
@login_required
def duplicate_quotation(request, id):
    # 指定IDの見積データを取得
    quotation = AnotherQuotationHeader.objects.get(id=id)

    if request.method == "GET":
        # テンプレートに渡すcontext作成
        context = {"object": quotation}

        # 確認画面を表示
        return render(request, "anoapp/quotation_duplicate.html", context)

    if request.method == "POST":
        # 複製を実施する場合。quotation_duplicate.htmlからのリクエストが"yes"
        if "yes" in request.POST:
            # 見積データを複製した新規オブジェクトを作成
            # model.pyのduplicate関数呼出し
            quotation.duplicate()
            # 一覧画面へ戻る
            return redirect(to="list-page")

        # 複製キャンセルの場合。quotation_duplicate.htmlからのリクエストが"no"
        elif "no" in request.POST:
            # 一覧画面へ戻る
            return redirect(to="list-page")


# その他プロダクト見積書_一覧画面 検索機能
# 検索対象：見積月日、作成者、顧客名、見積件名、見積有効期間、見積金額
@login_required
def quotation_list(request):
    # コンテキスト変数の定義
    context = {}

    # 検索ボックスからクエリを取得
    query = request.GET.get("query", "")

    # 検索クエリにマッチする見積ヘッダ queryset を取得
    # 複数の検索条件を OR でフィルタリング
    # 見積書IDの降順に並べ替え
    header_list = AnotherQuotationHeader.objects.filter(
        Q(quotation_date__icontains=query)
        | Q(create_user__icontains=query)
        | Q(customer_id__icontains=query)
        | Q(quotation_subject__icontains=query)
        | Q(validity_period__icontains=query)
        | Q(quotation_price__icontains=query)
    ).order_by("-quotation_id")

    # 1ページあたり10件でページング
    paginator = Paginator(header_list, 10)

    # 現在のページ番号を取得
    page_number = request.GET.get("page", 1)

    # 指定ページのレコードを取得
    page_obj = paginator.get_page(page_number)

    # ページングされたレコードをコンテキストに設定
    context["page_obj"] = page_obj

    # 検索結果が空の場合、メッセージを表示
    if len(page_obj) == 0:
        context["header_list"] = []
        context["no_result_message"] = "検索結果はありませんでした。"

    # 検索結果が存在する場合、ページングされたレコードを設定
    else:
        context["header_list"] = page_obj

    # レンダリング
    return render(request, "anoapp/quotation_list.html", context)


# その他プロダクト見積書_一覧画面 PDFプレビュー機能
#
@login_required
def pdf_preview_view(request, pk):
    # レスポンスオブジェクトを作成
    response = HttpResponse(status=200, content_type="application/pdf")

    # ダウンロード時のファイル名を設定
    download_name = "quotation_preview.pdf"

    # PDFを生成するクラスのインスタンスを作成
    pdf_creator = ExeMakeEstimatePdf(3, response, pk, False)

    # PDFインスタンスを取得
    my_pdf = pdf_creator.get_pdf()

    # PDFのタイトルを設定
    my_pdf.setTitle(download_name)

    # ページを追加
    my_pdf.showPage()

    # PDFを保存
    my_pdf.save()

    return response


"""
# ダウンロードされる方法
def pdf_preview_view(request, pk):

    response = HttpResponse(content_type="application/pdf")

    pdf_creator = ExeMakeEstimatePdf(3, response, pk, False)
    my_pdf = pdf_creator.get_pdf()
    my_pdf.setTitle("quotation_preview.pdf")
    my_pdf.showPage()
    my_pdf.save()

    # Content-Dispositionをattachmentに設定
    response["Content-Disposition"] = 'attachment; filename="quotation_preview.pdf"'

    # 別タブで開くためにTargetを指定
    response["X-Target"] = "_blank"

    return response


# jsを使用して別タブで開く方法
def pdf_preview_view(request, pk):

    # PDF生成
    response = HttpResponse(content_type="application/pdf")
    pdf_creator = ExeMakeEstimatePdf(3, response, pk, False)
    pdf = pdf_creator.get_pdf()
    pdf.setTitle("quotation_preview.pdf")
    pdf.showPage()
    pdf.save()

    # PDFデータをbase64エンコード
    pdf_base64 = base64.b64encode(response.content).decode("utf-8")

    # レスポンスをJSONでラップ
    wrapped_response = json.dumps({"pdf": pdf_base64})

    return HttpResponse(wrapped_response, content_type="application/json")
"""
