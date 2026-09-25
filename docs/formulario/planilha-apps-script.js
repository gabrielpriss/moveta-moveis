/**
 * Movetá: recebe os envios do formulário de /form/ e grava numa planilha.
 *
 * Como publicar (leva uns 3 minutos, ver README.md ao lado):
 *   1. Crie uma planilha no Google Sheets
 *   2. Extensões > Apps Script, apague o conteúdo e cole este arquivo
 *   3. Implantar > Nova implantação > Tipo: App da Web
 *        Executar como:        Eu
 *        Quem pode acessar:    Qualquer pessoa
 *   4. Copie a URL gerada e cole em ENDPOINT_PLANILHA, em
 *      scripts/form-script.js, depois rode `npm run form`
 *
 * A aba é criada sozinha no primeiro envio, com o cabeçalho.
 */

var ABA = 'Leads';

var COLUNAS = [
  'Data',
  'Nome',
  'WhatsApp',
  'Projeto para',
  'Ambiente',
  'Prazo',
  'Origem do clique',
  'Página',
];

function doPost(e) {
  try {
    var dados = JSON.parse(e.postData.contents);
    var aba = pegarAba();

    aba.appendRow([
      new Date(),
      dados.nome || '',
      // Apóstrofo na frente para o Sheets não comer o zero nem tratar
      // "(41) 99126-4615" como conta de subtração.
      "'" + (dados.telefone || ''),
      dados.perfil || '',
      dados.ambiente || '',
      dados.prazo || '',
      dados.origem || '',
      dados.pagina || '',
    ]);

    return resposta({ ok: true });
  } catch (err) {
    return resposta({ ok: false, erro: String(err) });
  }
}

/** Só para testar a URL no navegador: deve responder {"ok":true,...}. */
function doGet() {
  return resposta({ ok: true, aba: ABA, dica: 'Endpoint no ar. Os leads chegam por POST.' });
}

function pegarAba() {
  var planilha = SpreadsheetApp.getActiveSpreadsheet();
  var aba = planilha.getSheetByName(ABA);

  if (!aba) {
    aba = planilha.insertSheet(ABA);
    aba.appendRow(COLUNAS);
    aba.getRange(1, 1, 1, COLUNAS.length).setFontWeight('bold');
    aba.setFrozenRows(1);
  }
  return aba;
}

function resposta(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
