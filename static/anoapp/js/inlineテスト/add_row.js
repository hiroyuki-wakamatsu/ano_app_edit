// 製品情報、注釈情報、社内確認情報の空行をそれぞれimport
// インポートファイル：empty_row_const.js
import {
  mainEmptyRow,
  notesEmptyRow,
  confirmEmptyRow
} from './empty_row_const.js';

// DOM読み込み時のアクション(画面遷移時 or 画面リフレッシュ時など)
$(document).ready(function () {

  // カウンター変数
  let confirmCounter = 0;
  let mainCounter = 0;
  let notesCounter = 0;

  // prefix変数
  //const confirmPrefix = 'form-CONFIRM';

  // リンクがクリックされた時の処理を関数化
  function addRow(linkId) {

    // 空行変数
    var emptyRow;

    // クリックされたリンクによって空行の形式を変更(製品情報、注釈情報、社内確認情報)
    // 空行のid属性を設定
    if (linkId === 'confirmLink') {
      confirmCounter++;
      emptyRow = confirmEmptyRow.attr('id', `confirm-empty-${confirmCounter}`);
    } else if (linkId === 'mainLink') {
      mainCounter++;
      emptyRow = mainEmptyRow.attr('id', `main-empty-${mainCounter}`);
    } else if (linkId === 'notesLink') {
      notesCounter++;
      emptyRow = notesEmptyRow.attr('id', `notes-empty-${notesCounter}`);
    }

    // リンクIDからテーブルIDを導出
    var tableId = linkId.replace('Link', 'Table');

    // テーブル要素を取得
    var table = $('#' + tableId + ' tbody');

    // レコードの下に空行追加。レコードがない場合は新規レコード追加
    table.append(emptyRow);

    // name属性設定
    emptyRow.find('input, textarea').attr('name', `${confirmPrefix}-${confirmCounter}`);
  }

  // 各リンクがクリックされた時に行追加処理を実行
  // 'mainLink', 'notesLink','confirmLink'はテンプレート内で定義しているLinkID
  // 説明：
  // mainLinkクリック → linkIdに'mainLink'が入る → addRow('mainLink')が呼ばれる
  // notesLinkクリック → linkIdに'notesLink'が入る → addRow('notesLink')が呼ばれる
  // confirmLinkクリック → linkIdに'confirmLink'が入る → addRow('confirmLink')が呼ばれる
  ['mainLink', 'notesLink','confirmLink' ].forEach(function(linkId) {
    $('#' + linkId).click(function(e) {

      // デフォルトのsubmit動作を抑制
      e.preventDefault();

      // 行追加リンクをクリックした場合のアクション
      // 行追加処理関数を実行
      addRow(linkId);
    });

  });
console.log("DOM開始読み込み");

});