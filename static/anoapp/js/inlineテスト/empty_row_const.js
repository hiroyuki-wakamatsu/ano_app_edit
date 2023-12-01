// 説明：
// empty_row_const.js - 製品情報、注釈情報、社内確認情報の空行HTMLを作成する
// add_row.js内でインポート

// 製品情報空行作成
export const mainEmptyRow = $(`
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

// 注釈情報空行作成
export const notesEmptyRow = $(`
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

// 社内確認情報空行作成
export const confirmEmptyRow = $(`
    <tr>
      <td>
        <div class="form-group">
          <input type="text" name="anotherquotationconfirm_set-100-number" value="" size="3">
        </div>
      </td>
      <td>
        <div class="form-group">
          <textarea name="anotherquotationconfirm_set-100-internal_confirm" class="form-control" rows="3"></textarea>
        </div>
      </td>
    </tr>
`);