/*
// 1_全フィールドの値取得
//
// 1-1__手動入力フィールド値取得
// 全フィールド(全行)の数量入力を取得
const qtyInputs = document.querySelectorAll('.field-qty input');

// 全フィールド(全行)の標準価格入力を取得
const lpInputs = document.querySelectorAll('.field-lp input');

// 全フィールド(全行)の仕切率入力を取得
const discountRateInputs = document.querySelectorAll('.field-discount_rate input');

// 全フィールド(全行)の原価/台(unitcost)入力を取得
const unitcostInputs = document.querySelectorAll('.field-unitcost input');


// 1-2__計算結果入力フィールド値取得
// 全フィールド(全行)の提供単価入力を取得
const offerUnitPriceInputs = document.querySelectorAll('.field-offer_unit_price input');

// 全フィールド(全行)のご提供価格(offer_price)入力を取得
const offerPriceInputs = document.querySelectorAll('.field-offer_price input');

// 全フィールド(全行)の原価*台数(unitcost_by_number)入力を取得
const unitcostByNumberInputs = document.querySelectorAll('.field-unitcost_by_number input');

// 全フィールド(全行)の粗利(gross_profit)入力を取得
const grossProfitInputs = document.querySelectorAll('.field-gross_profit input');
// 全フィールド(全行)の利益率(profit_rate)入力を取得
const profitRateInputs = document.querySelectorAll('.field-profit_rate input');
*/

// 2_計算
//
// 計算を行う関数
function calculateBtn() {

  // 数量の行数分ループ(要はレコード分繰り返し)
  qtyInputs.forEach((_, index) => {

    // 1--入力値取得
    // indexを使って対応する入力値を取得
    // qty：数量、lp：標準価格、discountRate：仕切率、unitcost：原価 / 台
    const qty = qtyInputs[index].value; //数量
    const lp = lpInputs[index].value; //標準価格
    const discountRate = discountRateInputs[index].value; //仕切率
    const unitcost = unitcostInputs[index].value; //原価/台


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
    offerUnitPriceInputs[index].value = offerUnitPrice; //ご提供単価
    offerPriceInputs[index].value = offerPrice; //ご提供価格
    unitcostByNumberInputs[index].value = unitcostByNumber //原価*台数
    grossProfitInputs[index].value = grossProfit // 粗利
    profitRateInputs[index].value = profitRate // 利益率

  });
  // 完了アラートを表示
  alert('製品情報の計算が完了しました。\n\n注意：正常に計算がされない場合は一度「保存」ボタンをクリックして下さい。\n(改修中です。)');
}

// ボタンクリック時にcalculateを実行
const calculateButton = document.getElementById('calculate-button');
calculateButton.addEventListener('click', calculateBtn);

