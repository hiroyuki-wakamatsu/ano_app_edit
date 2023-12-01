// DOMが読み込まれた時に実行
$(document).ready(function() {

  // 社内確認情報行追加リンクがクリックされた時
  $('#confirmLink').click(function(e) {

    // デフォルトのsubmit動作を抑制
    e.preventDefault();

    // 社内確認情報のテーブル要素を取得
    var confirmTable = $('#confirmTable tbody');

    // 最後の行を取得
    var lastRow = confirmTable.find('tr:last');

    // 最後の行を複製
    var newRow = lastRow.clone();

    // 新しい行のinput, textareaを空に
    newRow.find('input[type="text"], textarea').val('');

    // 新しい行を社内確認情報テーブルに追加
    confirmTable.append(newRow);

  });

});