# GTM: conversão de WhatsApp

Container do site: **GTM-MBGK6P3J**, já instalado no `public/index.html`
(script no `<head>`, `<noscript>` logo depois do `<body>`).

Arquivo de importação: [`moveta-conversao-whatsapp.json`](moveta-conversao-whatsapp.json)

## O que a página manda para o dataLayer

Desde 21/08 todo CTA da página é um `<a href="https://wa.me/...">` com
`target="_blank"` e a mensagem já escrita. Um único ouvinte no `index.html`
cobre todos eles e empurra **um evento por clique**:

```js
{
  event:        'clique_whatsapp',
  cta_origem:   'Ambiente',   // Header, Hero, Card Residencial, CTA Final, Rodapé...
  cta_perfil:   'casa',       // casa | empresa | nao informado
  cta_ambiente: 'Cozinha'     // nome do ambiente, ou nao informado
}
```

Como o link abre em aba nova, a página não é descarregada e o dataLayer tem
tempo de sobra para processar o push. Não é preciso `eventCallback` nem
`transport_type: beacon`.

## Como importar

1. GTM > **Administrador** > **Importar contêiner**
2. Selecione o `moveta-conversao-whatsapp.json`
3. Espaço de trabalho: **Existente** (ou um novo)
4. Opção de importação: **Mesclar** > **Renomear conflitos**

   Use *Mesclar*, nunca *Substituir*: substituir apaga o que já existir no
   contêiner.
5. Confirme e revise a prévia das alterações antes de aplicar.

## Preencher antes de publicar

A importação entra com 3 constantes vazias, de propósito. Sem elas as tags
sobem mas não registram nada.

| Variável | Onde achar o valor |
|---|---|
| `CONST - GA4 Measurement ID` | GA4 > Administrador > Fluxos de dados > o fluxo do site. Formato `G-XXXXXXXXXX` |
| `CONST - Google Ads Conversion ID` | Google Ads > Objetivos > Conversões > ação **Contato WhatsApp** > Configurar tag. Formato `AW-XXXXXXXXXX` |
| `CONST - Google Ads Conversion Label` | mesma tela, ao lado do ID |

A ação de conversão no Google Ads precisa ser criada antes, como
**Site > Contato**, com contagem **Uma** (um clique em WhatsApp é um lead, não
importa quantas vezes a pessoa clique).

## O que entra no contêiner

**Variáveis**

- `DLV - cta_origem`, `DLV - cta_ambiente`, `DLV - cta_perfil`, todas com
  valor padrão `nao informado`
- as 3 constantes da tabela acima

**Gatilho**

- `CE - clique_whatsapp`, evento personalizado, sem filtro extra

**Tags**

| Tag | Dispara em | Para que serve |
|---|---|---|
| `GA4 - Configuracao` | todas as páginas | tag base do GA4 |
| `GA4 - gerar_lead (clique WhatsApp)` | `CE - clique_whatsapp` | evento `gerar_lead` com origem, ambiente e perfil |
| `Google Ads - Vinculador de conversoes` | todas as páginas | grava o GCLID no cookie `_gcl`, sem ele o Ads não atribui a conversão ao clique no anúncio |
| `[PREENCHER ID] Google Ads - Conversao Contato WhatsApp` | `CE - clique_whatsapp` | conversão nativa do Google Ads |

## Dois caminhos para a conversão, escolha um

O arquivo entrega os dois montados. Deixar os dois ativos **conta a mesma
conversão duas vezes** no Google Ads e estraga o CPA do relatório.

- **Tag nativa do Ads** (recomendado para campanha nova): mantenha a tag
  `[PREENCHER ID] Google Ads - Conversao Contato WhatsApp` e não importe o
  `gerar_lead` do GA4 para o Ads. Conversão chega mais rápido, o que ajuda o
  Smart Bidding no começo.
- **Importar do GA4**: pause a tag nativa e, no Google Ads, importe o evento
  `gerar_lead` como conversão. Vale a pena se você quiser o mesmo número no
  GA4 e no Ads.

No GA4, marque `gerar_lead` como evento-chave em Administrador > Eventos, nos
dois casos.

## Testar antes de publicar

1. GTM > **Visualizar**, aponte para `https://movetaplanejados.com.br`
2. Clique em um CTA qualquer. O Tag Assistant deve mostrar:
   - o evento `clique_whatsapp` na coluna da esquerda
   - as tags de conversão em **Tags Fired**
   - em **Variables**, `DLV - cta_origem` com o nome do CTA clicado
3. Repita num card de ambiente (ex.: Cozinha) e confira que `DLV - cta_ambiente`
   chega preenchido
4. Só então **Enviar** e publicar a versão

## Limite conhecido

Isto mede **clique no CTA**, não conversa iniciada. Quem clica e desiste antes
de mandar a mensagem entra na conta do mesmo jeito. Para a campanha começar já
com sinal de conversão é o suficiente; se depois o cliente quiser contar só
quem realmente falou, o caminho é uma API de WhatsApp Business com conversão
offline, e aí a estrutura muda.
