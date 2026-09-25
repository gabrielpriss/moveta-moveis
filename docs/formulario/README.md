# Teste A/B: página do formulário (`/form/`)

Fechado com o Eduardo e a Grazi na reunião de **25/09/2026**, usando o
[Espaço Pirâmide](https://xn--espaopiramideeventos-60b.com.br/form/) como
referência, que roda o mesmo teste.

## Por que esta página existe

No primeiro mês de campanha o relatório do Google acusou **50 conversões**, mas
a planilha do cliente tinha **18 leads reais**. A diferença não é erro de
medição: hoje a conversão dispara no **clique** no botão de WhatsApp, e clicar
não é o mesmo que mandar mensagem. Quem clica e desiste no app entra na conta
do Google e não entra na conta do cliente.

Com o formulário a conversão só dispara quando alguém **termina** de preencher.
O número do Google passa a ser o número real, e a campanha pode ser otimizada
em cima dos termos que trazem lead de verdade, não clique.

O Eduardo levantou a dúvida certa: *"não sei se o público que a gente tá
trabalhando vai ter essa paciência de preencher"*. Por isso não trocamos a
página, **testamos as duas**.

| Variante | URL | Conversão dispara em |
|---|---|---|
| A (atual) | `movetaplanejados.com.br/` | clique em qualquer CTA de WhatsApp |
| B (nova) | `movetaplanejados.com.br/form/` | envio do formulário |

Metade do orçamento para cada, como no Espaço Pirâmide.

## O que muda na variante B

É a **mesma landing page**: mesmas fotos, mesmo texto, mesmas seções. Só o
destino do CTA muda. Todos os 19 CTAs, do header ao rodapé, viram âncora para
o formulário em vez de abrir o WhatsApp.

Manter as duas idênticas fora isso é o que torna o teste legítimo: se as
páginas divergirem, o resultado deixa de medir formulário × WhatsApp e passa a
medir página velha × página nova.

### O formulário

Quatro etapas, as mesmas perguntas do popup qualificador que já existia no
projeto. As três primeiras qualificam; o contato só é pedido no fim, quando a
pessoa já investiu tempo:

1. O projeto é para onde? · Minha casa / Minha empresa
2. Qual ambiente? · muda conforme a etapa 1
3. Quando pretende começar? · O quanto antes / Nos próximos 3 meses / Ainda estou pesquisando
4. Nome e WhatsApp

Os cards já sabem o que a pessoa quer, então **pulam as etapas que respondem**:
quem clica no card "Cozinha" cai direto na etapa 3, e não responde de novo que
o projeto é para casa.

Ao enviar: o lead é medido, vai para a planilha e a pessoa é levada ao WhatsApp
com a mensagem montada. A confirmação aparece **antes** do redirecionamento de
propósito, para que o lead não se perca se o navegador bloquear a ida
automática.

## Como mexer na página

O arquivo `public/form/index.html` é **gerado**. Não edite ele.

```bash
npm run form
```

| Para mudar | Edite |
|---|---|
| conteúdo da página (fotos, textos, seções) | `public/index.html` e rode `npm run form` |
| perguntas e visual do formulário | `scripts/form-secao.html` |
| comportamento do formulário | `scripts/form-script.js` |
| o que difere entre as variantes | `scripts/gerar-form.py` |

O gerador **falha de propósito** se um marcador esperado sumir da LP. É melhor
o comando dar erro do que publicar uma variante pela metade no meio de um teste.

## Ligar a planilha

Enquanto o endpoint não for preenchido, o formulário funciona normal: mede a
conversão e leva para o WhatsApp. Só não grava na planilha.

1. Crie uma planilha no Google Sheets
2. **Extensões > Apps Script**, apague o conteúdo e cole
   [`planilha-apps-script.js`](planilha-apps-script.js)
3. **Implantar > Nova implantação > App da Web**
   - Executar como: **Eu**
   - Quem pode acessar: **Qualquer pessoa**
4. Copie a URL (`https://script.google.com/macros/s/.../exec`) e cole em
   `ENDPOINT_PLANILHA`, no topo de `scripts/form-script.js`
5. `npm run form` e publique

Para conferir, abra a URL no navegador: deve responder `{"ok":true,...}`. A aba
`Leads` nasce sozinha no primeiro envio, com uma coluna por resposta.

## Medição

A página empurra dois eventos para o dataLayer:

```js
{ event: 'abriu_formulario', cta_origem: 'Ambiente' }

{ event: 'lead_formulario',
  cta_origem:   'Ambiente',      // Header, Hero, Card Empresa, CTA Final...
  cta_perfil:   'Minha casa',
  cta_ambiente: 'Cozinha',
  lead_prazo:   'O quanto antes' }
```

**`lead_formulario` é a conversão do teste.** O `abriu_formulario` serve para
ver onde as pessoas desistem: se muita gente abre e pouca envia, o problema é o
formulário; se pouca gente abre, o problema é a página.

> ⚠️ **Falta criar no GTM.** A conversão de hoje escuta `clique_whatsapp`, que
> nesta página nunca dispara, porque não sobrou nenhum link direto de WhatsApp.
> Sem uma segunda tag ouvindo `lead_formulario`, a variante B **marca zero
> conversão** e o teste dá o resultado errado ao contrário. Duplicar a tag
> *Google Ads Conversion Tracking* que já existe (ver `docs/gtm/`), trocando só
> o gatilho, resolve.

## Subir as campanhas

- Duas campanhas, ou dois grupos, com metade do orçamento cada
- Variante B aponta para `https://movetaplanejados.com.br/form/`
- A variante B é `noindex`: existe só para o tráfego pago e não pode disputar a
  busca orgânica com a LP. Ela também fica fora do `sitemap.xml`
- Rodar o tempo suficiente para juntar volume nas duas antes de concluir
  qualquer coisa: com ~18 leads por mês, uma semana não decide nada

## O que olhar no fim

1. **Volume de leads** nas duas. A hipótese do Eduardo é que o formulário traz
   menos; se trouxer o mesmo, ele ganha sozinho pela medição correta
2. **Conversão do relatório × planilha**. Na variante B os dois números têm de
   bater. É esse o ponto do teste
3. **Qualidade**. A previsão da reunião é que o formulário filtre: quem tem
   paciência de responder quatro perguntas tende a ser quem realmente quer
   contratar, e o B2B, que é o foco, costuma ter mais paciência que o
   consumidor final
