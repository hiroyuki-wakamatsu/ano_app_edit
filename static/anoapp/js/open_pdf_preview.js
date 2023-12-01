// Ajaxでレスポンスを取得
$.get('/pdf/preview/123/', function(data) {

  // base64でエンコードされたPDFデータ
  const pdfBase64 = data.pdf;

  // PDFバイナリデータにデコード
  const pdfBytes = atob(pdfBase64);

  // 新しいウィンドウを開く
  const pdfWindow = window.open("");

  // PDFを表示
  pdfWindow.document.write(`
    <html>
      <body>
        <embed src="data:application/pdf;base64,${pdfBase64}" type="application/pdf" />
      </body>
    </html>
  `);

});