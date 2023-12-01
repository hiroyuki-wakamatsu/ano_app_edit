// 1_計算
//
// 計算を行う関数
function calculateBtn() {

  //新規行も含め最新レコード情報取得
  const qtyInputs2 = document.querySelectorAll('.field-qty input');
  const lpInputs2 = document.querySelectorAll('.field-lp input');
  const discountRateInputs2 = document.querySelectorAll('.field-discount_rate input');
  const unitcostInputs2 = document.querySelectorAll('.field-unitcost input');
  const offerUnitPriceInputs2 = document.querySelectorAll('.field-offer_unit_price input');
  const offerPriceInputs2 = document.querySelectorAll('.field-offer_price input');
  const unitcostByNumberInputs2 = document.querySelectorAll('.field-unitcost_by_number input');
  const grossProfitInputs2 = document.querySelectorAll('.field-gross_profit input');
  const profitRateInputs2 = document.querySelectorAll('.field-profit_rate input');

  // 数量の行数分ループ(要はレコード分繰り返し)
  qtyInputs2.forEach((_, index) => {

    // 1--入力値取得
    // indexを使って対応する入力値を取得
    // qty：数量、lp：標準価格、discountRate：仕切率、unitcost：原価 / 台
    const qty = qtyInputs2[index].value; //数量
    const lp = lpInputs2[index].value; //標準価格
    const discountRate = discountRateInputs2[index].value; //仕切率
    const unitcost = unitcostInputs2[index].value; //原価/台


    // 入力値が空の場合は処理をスキップ
    // 対象：数量、標準価格、仕切率、原価/台が全て入力されていたら計算する
    if(qty === "" || discountRate === ""  || lp === "" || unitcost === "") {
      return;
    }

    // 2--計算
    // 提供単価を計算
    const offerUnitPrice = lp * discountRate * 0.01;
    // ご提供価格を計算
    const offerPrice = lp * discountRate * 0.01 * qty;
    // 原価*台数を計算
    const unitcostByNumber = unitcost * qty;
    // 粗利を計算
    const grossProfit = offerPrice - unitcostByNumber;
    // 利益率を計算
    const profitRate = (grossProfit/offerPrice * 100).toFixed(1);


    // 3--計算結果入力
    offerUnitPriceInputs2[index].value = offerUnitPrice; //ご提供単価
    offerPriceInputs2[index].value = offerPrice; //ご提供価格
    unitcostByNumberInputs2[index].value = unitcostByNumber //原価*台数
    grossProfitInputs2[index].value = grossProfit // 粗利
    profitRateInputs2[index].value = profitRate // 利益率

  });
  // 完了アラートを表示
  alert('製品情報の一括計算が完了しました。\n\n※「数量」、「標準価格」、「仕切率」、「原価/台」が全て入力されていない場合は計算されません。');
}

// ボタンクリック時にcalculateを実行
const calculateButton = document.getElementById('calculate-button');
calculateButton.addEventListener('click', calculateBtn);

