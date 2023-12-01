$(document).ready(function() {

  // 製品情報の空行を作成しておく
  var mainEmptyRow = $(`
    <tr>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="3">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="50">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="10">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="5">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="3">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="3">
        </div>
      </td>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="3">
        </div>
      </td>
    </tr>
  `);

  // 注釈情報の空行を作成しておく
  var notesEmptyRow = $(`
    <tr>
      <td style="width: 100px;">
        <div class="form-group">
          <input type="text" name="" value="" size="3">
        </div>
      </td>
      <td>
        <div class="form-group">
          <textarea name="" rows="3" class="form-control"></textarea>
        </div>
      </td>
    </tr>
  `);

  // 社内確認事項の空行を作成しておく
  var confirmEmptyRow = $(`
    <tr>
      <td>
        <div class="form-group">
          <input type="text" name="" value="" size="3">
        </div>
      </td>
      <td>
        <div class="form-group">
          <textarea name="" class="form-control" rows="3"></textarea>
        </div>
      </td>
    </tr>
  `);

  // リンクがクリックされた時の処理を関数化
  function addRow(linkId) {

    // 空行変数
    var emptyRow;

    // クリックされたリンクによって空行の形式を変更(製品、注釈情報、社内確認)
    if(linkId === 'confirmLink') {
      emptyRow = confirmEmptyRow;
    } else if(linkId === 'mainLink') {
      emptyRow = mainEmptyRow;
    } else if(linkId === 'notesLink') {
      emptyRow = notesEmptyRow;
    }

    // リンクIDからテーブルIDを導出
    var tableId = linkId.replace('Link', 'Table');

    // テーブル要素を取得
    var table = $('#' + tableId + ' tbody');


    // テーブルにレコードがない場合は空行を追加
    if (table.find('tr').length == 0) {

      table.append(emptyRow);
    // テーブルにレコードがある場合は最終行のレコード形式コピーして空にして追加　
    } else {

      // 最後の行を取得
      var lastRow = table.find('tr:last');

      // 最後の行を複製
      var newRow = lastRow.clone();

      // 新しい行のinput, textareaを空に
      newRow.find('input[type="text"], textarea').val('');

      // 新しい行をテーブルに追加
      table.append(newRow);
    }

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
});