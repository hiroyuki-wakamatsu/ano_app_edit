// ご提供単価 自動計算

/*各種計算
 1_ご提供単価 = 標準価格 * 仕切率 * 0.01
 　関連フィールド：標準価格、仕切率

 2_ご提供価格 = 標準価格*仕切率*0.01 * 数量 =  ご提供単価 * 数量
 　関連フィールド：標準価格、仕切率、数量

 3_原価＊台数 =  (原価/台)＊数量
　関連フィールド：原価/台、数量

 4_粗利 = ご提供価格 - (原価＊台数)
 　関連フィールド：標準価格、仕切率、数量、原価/台

 5_利益率 = 粗利/ご提供価格
 　関連フィールド：標準価格、仕切率、数量、原価/台
*/

/* 現状のフィールド値を取得 */
//
/* ■ご提供単価、ご提供価格関連 */
// 全フィールド(全行)の数量(qty)入力を取得
const qtyInputs = document.querySelectorAll('.field-qty input');
// 全フィールド(全行)の標準価格(lp)入力を取得
const lpInputs = document.querySelectorAll('.field-lp input');
// 全フィールド(全行)の仕切率(discount_rate)入力を取得
const discountRateInputs = document.querySelectorAll('.field-discount_rate input');
// 全フィールド(全行)のご提供単価(offer_unit_price)入力を取得
const offerUnitPriceInputs = document.querySelectorAll('.field-offer_unit_price input');
// 全フィールド(全行)のご提供価格(offer_price)入力を取得
const offerPriceInputs = document.querySelectorAll('.field-offer_price input');

/* ■原価/台、原価*台数関連*/
// 全フィールド(全行)の原価/台(unitcost)入力を取得
const unitcostInputs = document.querySelectorAll('.field-unitcost input');
// 全フィールド(全行)の原価*台数(unitcost_by_number)入力を取得
const unitcostByNumberInputs = document.querySelectorAll('.field-unitcost_by_number input');

/* ■粗利、利益率関連*/
// 全フィールド(全行)の粗利(gross_profit)入力を取得
const grossProfitInputs = document.querySelectorAll('.field-gross_profit input');
// 全フィールド(全行)の利益率(profit_rate)入力を取得
const profitRateInputs = document.querySelectorAll('.field-profit_rate input');

/* ■削除フラグ*/
const deleteTd = document.querySelector('.field-DELETE');



/* ■合計値関連*/
// 1_ご提供価格合計値

// ご提供価格入力要素から配列を作成
const offerPrices = Array.from(offerPriceInputs);

// ご提供価格合計金額を計算
// 空要素がある場合はスキップする
const total = offerPrices.reduce((sum, input) => {

  // 空白文字をトリム
  const value = input.value.trim();

  // 空文字の場合はスキップ(右記のような空サフィックスはスキップ -> anotherquotationmain_set - __prefix__ - qty)
  if(value) {
    return sum + parseInt(value);
  } else {
    return sum;
  }

}, 0); // 初期値は0を指定

// 2_ヘッダーの見積金額入力欄の情報を取得
const quotationPriceInput = document.querySelector('input[name="quotation_price"]');


// ご提供価格合計のinput要素を取得(templateのタグidより)
const outputElement = document.getElementById('totalOfferPrice');

// 合計金額を日本円金額形式の文字列にフォーマット
const formatted = total.toLocaleString('ja-JP', {
  style: 'currency',
  currency: 'JPY'
});

// ■ヘッダー情報フォーム： 「見積金額」フィールドへご提供価格の合計値を入力
quotationPriceInput.value = total;

// ■製品情報フォーム： 「ご提供価格合計」フィールドへご提供価格の合計値を入力
// フォーマットした文字列を出力
outputElement.value = formatted;



/* イベントトリガー条件
  計算項目：計5項目
    ご提供単価(offerUnitPrice)、ご提供価格(offerPrice)、原価*台数(unitcost_by_number)、粗利(grossProfit)、利益率(profit_rate)

  全フィールドが変更された場合にイベント実行
  　数量(qty)、標準価格(lp)、 仕切率(discount_rate)、ご提供単価(offerUnitPrice)ご提供価格(offerPrice、 原価/台(unitcost)、原価*台数(unitcost_by_number)、粗利(grossProfit)、利益率(profit_rate)
*/

// 全てのフィールドで値が変更された場合、イベント開始
// 対象：全フィールドの値
//
//数量(qty)
qtyInputs.forEach((input, index) => {
  input.addEventListener('change', () => {
    const result = calculate(index);

    // 数量(qty)が変更された際、関連する値を再計算し入力欄に設定
    // ご提供価格を再計算し、ご提供価格入力欄に設定
    offerPriceInputs[index].value = result.offerPrice;

    // 原価×台数を再計算し、原価×台数入力欄に設定
    unitcostByNumberInputs[index].value = result.unitcostByNumber;

    // 粗利を再計算し、粗利入力欄に設定
    grossProfitInputs[index].value = result.grossProfit;

    // 利益率を再計算し、利益率入力欄に設定
    profitRateInputs[index].value = result.profitRate;
  });
});

// 標準価格(lp)
lpInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    // calculateの戻り値をresultに受け取る
    const result = calculate(index);

    // 標準価格(lp)が変更された際、関連する値を再計算し入力欄に設定
    // ご提供価格を再計算し、ご提供価格入力欄に設定
    offerPriceInputs[index].value = result.offerPrice;

    // 粗利を再計算し、粗利入力欄に設定
    grossProfitInputs[index].value = result.grossProfit;

    // 利益率を再計算し、利益率入力欄に設定
    profitRateInputs[index].value = result.profitRate;
  });
});

// 仕切率(discount_rate)
discountRateInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    const result = calculate(index);

    // 仕切率が変更された際、ご提供価格を再計算し入力欄に設定
    offerPriceInputs[index].value = result.offerPrice;

    // 仕切率が変更された際、ご提供単価を再計算し入力欄に設定
    offerUnitPriceInputs[index].value = result.offerUnitPrice;

  });

});

// ご提供単価
offerUnitPriceInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    const result = calculate(index);

    // 4つの値をセット
    offerPriceInputs[index].value = result.offerPrice;
    unitCostByNumberInputs[index].value = result.unitCostByNumber;
    grossProfitInputs[index].value = result.grossProfit;
    profitRateInputs[index].value = result.profitRate;

  });

});

// ご提供価格
offerPriceInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    const result = calculate(index);

    // 粗利と利益率をセット
    grossProfitInputs[index].value = result.grossProfit;
    profitRateInputs[index].value = result.profitRate;

  });

});

// 原価/台(unitcost)
unitcostInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    const result = calculate(index);

    // 3つの値を更新
    unitcostByNumberInputs[index].value = result.unitcostByNumber;
    grossProfitInputs[index].value = result.grossProfit;
    profitRateInputs[index].value = result.profitRate;

  });

});

// 原価*台数(unitcost_by_number)
unitcostByNumberInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    const result = calculate(index);

    // 粗利と利益率を更新
    grossProfitInputs[index].value = result.grossProfit;
    profitRateInputs[index].value = result.profitRate;

  });

});

// 粗利
grossProfitInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    const result = calculate(index);

    // 利益率を更新
    profitRateInputs[index].value = result.profitRate;

  });

});

// 利益率(profit_rate)
profitRateInputs.forEach((input, index) => {

  input.addEventListener('change', () => {

    const result = calculate(index);

    // 粗利を更新
    grossProfitInputs[index].value = result.grossProfit;

  });

});


/* 各種計算する関数 */
function calculate(index) {
  // 対象行の入力値を取得

    // 結果オブジェクトの定義
    const result = {};

    /* 1_フィールドの値取得 */
    // 数量
    const qty = qtyInputs[index].value;
    // 標準価格
    const lp = lpInputs[index].value;
    // 仕切率
    const discountRate = discountRateInputs[index].value;
    // ご提供単価
    const offerUnitPrice = offerUnitPriceInputs[index].value;
    // ご提供価格
    const offerPrice = offerPriceInputs[index].value;
    // 原価/台
    const unitcost = unitcostInputs[index].value;
    // 原価*台数
    const unitcostByNumber = unitcostByNumberInputs[index].value;
    // 粗利
    const grossProfit = grossProfitInputs[index].value;
    // 利益率
    const profitRate = profitRateInputs[index].value;


    /* 2_計算 */
    // ご提供単価 = 標準価格 * 仕切率 * 0.01
    const offerUnitPriceNum = lp * discountRate * 0.01;

     // ご提供価格 = ご提供単価 * 数量
    let offerPriceCalc = Math.floor(offerUnitPriceNum * qty);

    //原価＊台数 =  (原価/台)＊数量
    let unitcostByNumberCalc = unitcost * qty;

    // 粗利 = ご提供価格 - (原価＊台数)
    //let grossProfitCalc = offerPrice - unitcostByNumber;
    let grossProfitCalc = offerPrice - unitcostByNumberCalc;

    //利益率 = 粗利/ご提供価格 * 100
    let profitRateCalc =  (grossProfitCalc / offerPrice * 100).toFixed(2);

    // 3. 結果をオブジェクトにセット
    // ご提供単価
    result.offerUnitPrice = offerUnitPriceNum;

    // ご提供価格
    result.offerPrice = offerPriceCalc;

    // 原価*台数
    result.unitcostByNumber = unitcostByNumberCalc;

    // 粗利
    result.grossProfit = grossProfitCalc;

    // 利益率
    result.profitRate = profitRateCalc;

    // 4. 結果オブジェクトを返す
    return result;

}

