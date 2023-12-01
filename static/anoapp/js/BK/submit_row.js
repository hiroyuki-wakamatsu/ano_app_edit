// 空行に追加したレコードをsubmitするjs
// ファイル名：submit_row.js

// 空行追加時
$input.attr('id', 'input-' + uniqueId);
$input.addClass('input-data');

// 送信時
let inputData = {};

$('.input-data').each(function() {
  // id取得
  let id = $(this).attr('id');
  // inputDataへ追加
  inputData[id] = $(this).val();
});

// AJAX通信の設定
$.ajax({
  type: 'POST',
  url: '/api/send',
  data: JSON.stringify(inputData)
})
.done(function(response) {
  // 通信成功時の処理
  alert('データの送信が成功しました');
})
.fail(function(error) {
  // 通信失敗時の処理
  alert('データの送信が失敗しました');
});