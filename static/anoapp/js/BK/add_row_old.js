// DOMが読み込まれた時に実行
$(document).ready(function() {

  // リンクがクリックされた時の処理を関数化
  function addRow(linkId) {
    // リンクIDからテーブルIDを導出
    var tableId = linkId.replace('Link', 'Table');

    // テーブル要素を取得
    var table = $('#' + tableId + ' tbody');

    // 最後の行を取得
    var lastRow = table.find('tr:last');

    // 最後の行を複製
    var newRow = lastRow.clone();

    // 新しい行のinput, textareaを空に
    newRow.find('input[type="text"], textarea').val('');

    // 新しい行をテーブルに追加
    table.append(newRow);
  }

  // 各リンクがクリックされた時に行追加処理を実行
  ['confirmLink', 'mainLink', 'notesLink'].forEach(function(linkId) {
    $('#' + linkId).click(function(e) {
      // デフォルトのsubmit動作を抑制
      e.preventDefault();

      // 行追加処理を実行
      addRow(linkId);
    });
  });
  console.log("end");

});