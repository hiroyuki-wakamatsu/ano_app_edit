from .estimatepdf_func import MakeEstimatePdf


class ExeMakeEstimatePdf:
    """
    クラス名:ExeMakeEstimatePdf
    説明:estimatepdf.MakeEstimatePdfクラスを実行してPDFファイルを出力する
    引数説明:
      引数1:type       ->  製品種別  1:Forti 2:qnap 3:その他
      引数2:filename   ->  HttpResponseオブジェクト
      引数3:estimateid ->  pk (最終的には見積番号?)
      引数4:hosyu      ->  Fortinet用保守フラグ True:保守用フッター False:通常フッター
    """

    def __init__(self, type: int(), filename, estimateid: int(), hosyu):
        # 0_インスタンス作成
        self.em = MakeEstimatePdf(filename)

        # 1_見積IDから辞書型データを作成。戻り値は辞書型データ
        # estimatepdf_func.py:EstimatePdfクラスのmakeDictDataメソッドを呼び出
        data = self.em._MakeEstimatePdf__makeDictData(estimateid, hosyu)

        # ★メモ：今の所、2-1はFortinetのみの処理。
        #
        # 2-1_事前作業_1
        # _データ有無確認(参考価格、次年度参考価格対象。見積価格は必須入力)
        # 戻り値
        #   0-> 参考価格、次年度参考価格 共にデータあり
        #   1-> 参考価格 データなし、 次年度参考価格 データあり
        # 　2-> 参考価格 データあり、 次年度参考価格 データなし
        # 　3-> 参考価格 データなし、 次年度参考価格 データなし
        # confirmFlg = self.em._MakeEstimatePdf__dataConfirm(data)

        # ★メモ：Fortinet   -> 本見積価格,参考価格,次年度参考価格の3項目
        #        その他製品  -> 本見積価格の1項目

        # 2-2_事前作業_2
        # _注釈番号有無確認(見積価格、参考価格、次年度参考価格対象)
        # 注釈番号カラムに1行でも値が入力されていたら"あり"、1行も入力されていなかったら"なし"とする。
        # 戻り値：confirmAnnoFlg
        #       本見積価格  参考価格  次年度参考価格
        # 000:     なし       なし           なし
        # 001:     あり       なし           なし
        # 010:     なし       あり           なし
        # 011:     あり       あり           なし
        # 100:     なし       なし           あり
        # 101:     あり       なし           あり
        # 110:     なし       あり           あり
        # 111:     あり       あり           あり
        confirmAnnoFlg = self.em._MakeEstimatePdf__dataAnnoConfirm(data)

        # ★メモ：その他製品システムのみの機能
        #
        # 2-3_事前作業_3
        # _社内確認情報有無確認
        # 戻り値：confirmConFlg
        #    0 -> 社内確認情報にデータが存在しない場合
        #    1 -> 社内確認情報にデータが存在する場合
        confirmConFlg = self.em._MakeEstimatePdf__dataConConfirm(data)

        # 3-1_描画_ヘッダ描画
        self.em._MakeEstimatePdf__drawHeaderTitle()
        self.em._MakeEstimatePdf__drawHeaderHeadline(data)
        self.em._MakeEstimatePdf__drawHeaderEstimationNumber(data)
        self.em._MakeEstimatePdf__drawHeaderOursInfo(data)
        self.em._MakeEstimatePdf__drawHeaderStampArea()
        self.em._MakeEstimatePdf__drawHeaderApprovalStamp(data)
        self.em._MakeEstimatePdf__drawHeaderCompanySeal()

        # 3-2_Draft文字描画(1ページ目) ※プレビューのみ描画
        self.em._MakeEstimatePdf__drawdraft()

        # ★メモ：その他製品は本見積価格のみなので以下関数の第2引数は”1”固定とする。
        #
        # 3-3_描画_ボディ描画
        # 第2引数で本見積価格、参考価格、次年度参考価格の処理を分岐する
        # 第2引数 1->本見積価格 2->参考価格 3->次年度参考価格
        #

        # 3-3-1_製品情報描画,注釈情報描画
        # 本見積価格：注釈カラムに値が入っている場合は注釈パートを描画する
        if confirmAnnoFlg == 1:
            # 3-3-1_製品情報描画
            self.em._MakeEstimatePdf__drawContent(data, 1)
            # 3-3-2_注釈情報描画
            self.em._MakeEstimatePdf__drawContentAnnotation(data, 1)
        # 本見積価格：注釈カラムに値が入っている場合は注釈パートを描画しない
        else:
            # 3-3-1_製品情報描画
            self.em._MakeEstimatePdf__drawContent(data, 1)

        # ★メモ：その他製品システム限定機能
        #
        # 3-3-3_社内確認情報描画
        # 社内確認情報にデータが存在する場合のみ社内確認情報パートを描画する
        # if confirmConFlg == 1:
        #    self.em._MakeEstimatePdf__drawContentConfirm(data, 1)

        # 3-4_描画_フッタ描画
        self.em._MakeEstimatePdf__drawFooter(data)

        # 3-5_Draft文字描画(最終ページ) ※プレビューのみ描画
        self.em._MakeEstimatePdf__drawdraft()

        # _PDFファイル保存
        # self.em._MakeEstimatePdf__save()  # 呼出し側でsaveしたい(park)

    # pdfオブジェクト取得のため追記(2023.02.20 park)
    def get_pdf(self):
        return self.em.pdf
