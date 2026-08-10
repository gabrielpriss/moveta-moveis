# Movetá Móveis Planejados: Contexto do Projeto

LP de captação para campanha de **Google Ads**. Canal principal de conversão: **WhatsApp**.

## Stack
- HTML estático single-page em `public/index.html` (arquivo único, CSS e JS inline)
- Tailwind CSS via CDN (config inline no `<head>`), AOS, Font Awesome 6
- Fontes: Montserrat (corpo), Marcellus (títulos, serif clássica no estilo do lettering da logo)
- Hospedagem prevista: Cloudflare Pages

## Rodar localmente
```bash
npm run dev
```
Sobe em http://localhost:8934. Alternativa com o runtime real do Cloudflare: `npm run dev:wrangler`.

## Identidade visual (extraída da logo oficial)
Logo: monograma M dourado em moldura quadrada, wordmark prata, subtítulo dourado.

A arte original (`arte-original/logo horizontal.png`, 1774x887) é um mockup:
letreiro metálico fotografado sobre parede escura, com vinheta. O script
`scripts/preparar-logo.py` recorta e remove o fundo, gerando:

- `public/assets/logo-moveta.png` (955x240, transparente) — header e rodapé
- `public/assets/favicon-moveta.png` (256x256) — só o monograma

```bash
npm run logo   # regenera a partir da arte original
```

O fundo sai por luminância: medindo a própria arte, a parede vai no máximo a
L=67 e 95% do metal está acima de L=108, então a rampa 70→112 vira o canal alfa.
Isso preserva o relevo e é seguro porque a logo sempre aparece sobre fundo
escuro na página — qualquer sombra semitransparente mostra um escuro parecido
por trás. Se a logo for usada sobre fundo claro algum dia, refazer o recorte.

```
carvao: #211D1A  (fundo escuro da logo; header, hero, cards, CTA final)
ouro:   #C9A24B  (dourado do monograma; usar sobre fundo escuro)
bronze: #7A5F24  (dourado escuro; texto e ícones sobre fundo claro, contraste AA)
prata:  #D8D5D0  (wordmark; texto sobre fundo escuro)
areia:  #EDE7DB  (fundo claro alternado)
creme:  #F7F4EE  (fundo claro geral)
pedra:  #6B6560  (texto secundário)
zap:    #25D366  (verde reservado exclusivamente aos CTAs de WhatsApp)
```

## Regra de conteúdo (importante)
A página afirma **somente o que o cliente citou** na reunião de onboarding
(03/08/2026). Auditado duas vezes: por grep na transcrição e por um workflow de
3 agentes adversariais (claims, tipografia, contraste WCAG). Não existe menção a
projeto 3D, showroom, garantia, parcelamento, nota fiscal, sábado, amostras,
"sem custo", estações de trabalho ou balcão de recepção, então nada disso
aparece no copy. Cuidados extras da auditoria: a lavanderia de Fazenda Rio
Grande foi FECHADA, não entregue; os armários da empresa foram um PEDIDO aceito;
o prazo anunciado é de 25 dias e também depende da fila de projetos; a sociedade ainda
está em formalização (CNPJ em transição, 1:04:05). Antes de adicionar qualquer
claim novo, confirmar com o cliente. Também não usar travessão (em dash) em
nenhum texto.

### Tom: nada que tire credibilidade
Decisão do Gabriel (07/08). A página **não** menciona que a empresa é nova, que
não tem loja física nem que a execução depende de um único marceneiro. A
marcenaria aparece sempre como **competência e estrutura da empresa**, nunca
como uma pessoa sozinha, e o texto de "Sobre" enquadra a Movetá como a união de
duas frentes societárias: marcenaria (técnica, projeto, execução) e gestão
(comercial, prazos, atendimento). A capacidade limitada foi reenquadrada como
escolha deliberada ("um número controlado de projetos por vez"), que é o que
sustenta o prazo. Ao editar o copy, manter esse enquadramento.

### Prazo: anunciar 25 dias, não a faixa
Decisão do Gabriel (07/08). O cliente disse "entre 22 a 25 dias" (20:02) e que
"22 dias já tá cortando". A página anuncia o **teto: 25 dias**, em todos os 9
pontos onde o prazo aparece. Anunciar o piso criaria risco de furar a promessa
logo na primeira obra; anunciar o teto permite entregar antes. Não voltar para
"22 a 25" nem para "22".

## Contexto do cliente (reunião de onboarding, 03/08/2026)

Empresa **nova**, cerca de 2 meses, faturamento zero no início da campanha.
Sociedade entre a dupla comercial/financeira (Eduardo e Grazi) e o marceneiro
responsável pelo projeto e pela execução. Nome anterior: DEG Planejados.

O que foi citado e sustenta o copy:

| Fato usado na página | Ref. |
|---|---|
| Sob medida ("Eu sob medida, né?") | 17:07 |
| Prazo "entre 22 a 25 dias" para cozinha de apartamento; projetos maiores alongam e o cliente sabe antes | 19:20, 20:02, 20:50 |
| Montagem agendada assim que os móveis ficam prontos | 20:02 |
| Prazo também depende da fila de projetos fechados | 19:20, 20:50 |
| "Nosso prazo tá excelente porque a gente é novo, vamos entregar mais rápido" | 21:06 |
| Pedido aceito: armários sob medida para funcionários de uma empresa | 21:38 |
| Escritório: execução mais rápida, decisão mais objetiva | 22:10, 52:01 |
| Exemplos de móvel de escritório: mesa para 6 pessoas, tomadas, painel para TV | 52:16 |
| Lavanderia fechada (vendida) em Fazenda Rio Grande | 24:29 |
| Público B / médio, não premium | 18:09 |
| Sem showroom, "eu vou até o cliente" | 29:02 |
| Dores do mercado: qualidade, prazo, "pegou o dinheiro e não entregou" | 09:26 |
| Objeção planejado × móvel pronto | 26:14 |
| Atendimento em horário comercial confirmado | 49:08 |
| Marcenaria própria (barracão de produção e montagem) | 45:16 |
| Cores da logo confirmadas pela Grazi | 1:06:47 |

Por isso a página não usa "alto padrão", não anuncia showroom, não exibe anos de
mercado e não fala de 3D, garantia ou parcelamento.

### Escopo de produto: o que pode e o que não pode aparecer
Terceira auditoria (07/08) confrontou cada item de escopo com a transcrição.

**Citado, pode usar:** cozinha, dormitório/guarda-roupa, lavanderia, painel para
TV, bancada, armários e divisórias para funcionários, mesa de reunião (a "mesa
que atenda seis pessoas"), móveis para escritório, ferragens.

**Removido por não ter nenhuma menção:** torre quente, espelheira, cabeceira,
rack, estante, comércio e loja.

**Banheiro foi devolvido em 10/08.** Tinha sido removido por não aparecer na
transcrição, mas as fotos do Drive mostram um gabinete de banheiro executado
por eles (15.58.04-1). A foto é a prova; o card voltou.

**Vale confirmar com o cliente:** o Drive também traz um balcão de recepção
(15.56.44) e divisórias ripadas (15.36.50-2/3). Se confirmarem, dá para abrir
cards próprios para esses serviços na seção de empresas.

## Header responsivo
A logo é larga (955x240, proporção ~4:1), então em telas estreitas ela precisa encolher, senão
empurra o CTA e o hamburguer para fora da viewport (bug encontrado a 320px: o
botão do menu terminava 57px além da tela, invisível por causa do
`overflow-x: clip`). Comportamento atual:

| Largura | Logo | CTA do header |
|---|---|---|
| < 360px | `h-8` | só o ícone (nome vem do `aria-label`) |
| 360 a 639px | `h-10` | "Orçamento" |
| >= 640px | `h-12` | "Pedir orçamento" |

Ao mexer no header, testar a 320px (iPhone SE) antes de subir.

## Estrutura da página
1. Header sticky escuro (+ menu mobile)
2. Hero carvão/dourado, prazo de 25 dias como gancho. A imagem grande é um
   **carrossel** de 10 obras; as duas laterais são estáticas
3. Bifurcação casa × empresa
4. Residencial, 6 ambientes
5. Empresas, 4 tipos de projeto
6. Como funciona, 5 etapas
7. Acabamentos
8. Sobre, história real sem inflar tempo de mercado, seguido de duas galerias
   de obras (residencial e comercial)
9. Avaliações do Google (ver abaixo)
10. CTA final
11. FAQ, 4 perguntas com termos soft
13. "Você já ouviu alguma dessas histórias" (as 3 dores do 09:26), última seção
14. Rodapé

A seção "Antes de decidir" (comparativo planejado × móvel pronto) foi removida
a pedido do Gabriel em 07/08. O FAQ ainda cobre o tema, que era o que capturava
termo soft.

## Carrosséis

**Hero (`#hero-carrossel`).** 10 obras alternando 1 residencial / 1 comercial,
em `hero-slide-01` a `10` (ímpares residenciais, pares comerciais). Troca por
fade a cada 4s e também nos botões e nos pontos. Uma ação manual reinicia a
contagem, para o slide escolhido não trocar logo em seguida. Pausa no hover, no
foco do teclado e quando a aba sai de vista. Respeita `prefers-reduced-motion`:
com a preferência ligada, não roda sozinho e só anda no clique. Só o slide
visível fica com `aria-hidden="false"`.

> Ao testar em aba de background, o avanço automático **não** acontece: é o
> `visibilitychange` pausando de propósito, não bug. Verificar com a aba visível.

**Galerias abaixo de "Quem faz".** Duas faixas de rolagem horizontal com
scroll-snap, `#galeria-residencial` e `#galeria-comercial`, 8 fotos cada
(`galeria-res-01..08`, `galeria-com-01..08`). As setas rolam 85% da largura
visível, para sempre sobrar uma imagem de referência entre um avanço e outro.
No mobile as setas somem e a rolagem é por toque.

## WhatsApp
Número no arquivo: `5541991264615`

> ⚠️ **Confirmar antes de publicar.** O informado foi `+55 41 9126-4615`, com 8
> dígitos após o DDD. Celular no Paraná tem 9, então foi assumido o 9 inicial:
> (41) 99126-4615. Se estiver errado, buscar e substituir `5541991264615` no
> `index.html` (rodapé, `tel:` e constante `WHATSAPP` do script).

Todos os CTAs abrem o **popup qualificador** (4 etapas: perfil, ambiente, prazo,
nome e telefone) e terminam abrindo o `wa.me` com a mensagem pronta:

```
Olá! Sou Ana e vim pelo site da Movetá.

Projeto para: Minha casa
Ambiente: Cozinha
Pretendo começar: O quanto antes
Meu WhatsApp: (41) 98888-7777
```

Botões com `data-perfil` / `data-ambiente` pulam as etapas que já respondem.
Telefone visível **apenas no rodapé**; no resto da página, só CTA de WhatsApp.

## Imagens
Os `.svg` em `public/assets/` são **placeholders** dos ambientes que ainda não
têm foto. A logo (`logo-moveta.png`) e o favicon vêm de `npm run logo`; as fotos
tratadas (`.webp`) vêm de `npm run fotos`. Nenhum dos dois é tocado pelo gerador
de placeholders.

Para aplicar as fotos reais, salve os arquivos numa pasta usando os nomes-base
esperados e rode:

```bash
./scripts/aplicar-fotos.sh ~/Downloads/fotos-moveta
```

O script redimensiona (máx. 1600px), grava em `public/assets/`, troca a
referência no `index.html` e remove o placeholder correspondente. Só mexe nas
fotos que encontrar; o resto continua placeholder. Saída em `.webp` se houver
`cwebp` ou `magick` (`brew install webp`), senão `.jpg` via `sips`
(o `sips` do macOS lê webp mas não escreve).

```bash
npm run placeholders   # regenera os placeholders (preserva a logo)
```

### Fotos: obras reais do cliente (10/08/2026)

Vieram do Drive **DEG MÓVEIS - Prime** (88 arquivos, 86 fotos + 2 vídeos), em
1071 a 1600px. São **obras executadas pela Movetá**, não banco de imagens: a
galeria é portfólio de verdade e os `alt` podem atribuir autoria.

Originais das 14 selecionadas em `fotos-originais/`. Reprocessar com:

```bash
npm run fotos
```

| Slot | Foto de origem | O que mostra |
|---|---|---|
| `hero-slide-01` R | 15.36.42-1 | painel ripado com TV e bancada |
| `hero-slide-02` C | 15.56.44 | balcão de recepção |
| `hero-slide-03` R | 15.58.02 | home office fendi com LED |
| `hero-slide-04` C | 16.00.33 | escritório com mesa em L |
| `hero-slide-05` R | 15.37.01 | cozinha branca em L, granito preto |
| `hero-slide-06` C | 0722-17.11.36-1 | mesa de reunião com gaveteiros |
| `hero-slide-07` R | 15.37.05-1 | painel ripado com TV ligada |
| `hero-slide-08` C | 16.00.36 | estações de trabalho |
| `hero-slide-09` R | 15.36.40-1 | armários com nichos e LED |
| `hero-slide-10` C | 15.37.24 | sala de reunião com painel para TV |
| `hero-detalhe-1` | 15.58.05 | guarda-roupa fendi (lateral estática) |
| `hero-detalhe-2` | 16.00.36 | estações de trabalho (lateral estática) |
| `residencial-cozinha` | 15.37.01 | cozinha branca em L |
| `residencial-dormitorio` | 15.36.40-1 | armários com nichos e LED |
| `residencial-painel-tv` | 15.37.05-1 | painel ripado com TV ligada |
| `residencial-banheiro` | 15.58.04-1 | gabinete fendi com granito |
| `residencial-lavanderia` | 15.36.58 | área de serviço, torneira de parede |
| `residencial-home-office` | 15.57.58-1 | bancada com armários aéreos |
| `empresa-mesa` | 15.56.44 | balcão de recepção |
| `empresa-escritorio` | 16.00.33 | escritório com mesa em L |
| `empresa-sala-reuniao` | 0722-17.11.36-1 | mesa de reunião |
| `empresa-armarios` | 15.36.39-1 | escaninhos para equipe |
| `empresa-painel-tv` | 15.37.24 | sala de reunião com TV |
| `galeria-res-01..08` | ver `scripts/tratar-fotos.py` | 8 obras residenciais |
| `galeria-com-01..08` | ver `scripts/tratar-fotos.py` | 8 obras comerciais |

> ⚠️ **Lavanderia a confirmar.** A foto que estava no card (15.36.52) é uma
> **copa**: bancada de granito, cuba e frigobar, não lavanderia. Foi trocada por
> 15.36.58, que tem torneira de parede e cara de área de serviço, mas nenhuma
> foto do Drive mostra máquina de lavar ou tanque com clareza. Confirmar com o
> cliente ou pedir uma foto de lavanderia de verdade.

Todas ficaram em **100% ou mais** da resolução que o slot pede em tela retina
(antes, com as miniaturas, quatro estavam em 42%).

Cuidados no processamento:
- **Marca d'água**: várias fotos de cozinha trazem "POCO X6 5G" e data no rodapé.
  O campo `cortar_rodape` no script remove a faixa (a da cozinha corta 6%).
  Ao trocar por outra foto de cozinha, conferir se precisa do mesmo corte.
- **Nunca ampliar acima de 2x**: o script respeita a largura-alvo por slot e só
  reduz quando a origem é maior. Nitidez mais leve (60%) ao reduzir, mais forte
  (90%) ao ampliar.
- Fotos descartadas por defeito: 15.36.45 (pessoa refletida no espelho),
  15.36.57 (luz roxa de LED distorce a cor real do móvel).

Ainda sem foto, seguem placeholder SVG: `processo-medicao`,
`processo-apresentacao`, `sobre-equipe`, `marcenaria-01/02/03`. Não há no Drive
nenhuma foto de pessoas medindo, apresentando projeto ou da oficina.

## Avaliações do Google

Seção estática com a identidade visual do Google (`#depoimentos`), pronta para
receber as avaliações reais do Google Meu Negócio. Cores oficiais da marca:
`#4285F4` `#34A853` `#FBBC05` `#EA4335` no logotipo, `#FBBC04` nas estrelas,
`#1A73E8` no link.

É montada a partir da constante `AVALIACOES` no script do rodapé:

```js
{ nome: 'Ana C.', inicial: 'A', quando: 'há 2 semanas', nota: 5,
  texto: 'Texto da avaliação.' }
```

A nota média e o total do topo são calculados sozinhos a partir da lista.

**Três estados, todos testados:**

| Estado | Quando | O que aparece |
|---|---|---|
| Exemplo | alguma entrada com `exemplo: true` | cartões + **tarja âmbar de aviso** |
| Real | nenhuma entrada com `exemplo: true` | cartões, sem tarja |
| Vazio | `AVALIACOES = []` | convite honesto, resumo escondido |

> A empresa tem **zero avaliações** hoje. Por isso a seção ships com três
> entradas marcadas `exemplo: true`, cujo texto descreve o próprio layout em vez
> de simular depoimento de cliente. Publicar avaliação inventada com nome de
> pessoa seria fraude e viola as políticas do Google. Ao colar as reais, apagar
> o campo `exemplo: true` de cada uma: a tarja some sozinha.

Falta ainda trocar `LINK_GOOGLE` (hoje aponta para o Google Maps genérico) pelo
perfil do Meu Negócio quando ele for criado.

**Integração futura:** trocar a constante por um `fetch` que devolva o mesmo
formato (Places API, endpoint `place/details`, campo `reviews`, ou um JSON
gerado por rotina). O resto da seção não muda, ela só lê o array.

## SEO

Aplicado em 10/08. Domínio oficial: **movetaplanejados.com.br** (apex, sem www),
já aplicado nos 11 lugares (canonical, og:url, og:image, twitter:image, os 4
campos do JSON-LD, `robots.txt` e `sitemap.xml`).

> ⚠️ Configurar no Cloudflare o **301 de `www` para o apex**. O canonical aponta
> para o apex; se o www responder 200 por conta própria, o Google enxerga duas
> páginas com o mesmo conteúdo.

- `canonical`, `robots` com `max-image-preview:large`, `geo.region`/`geo.placename`
- Open Graph completo e Twitter `summary_large_image`
- `public/robots.txt` e `public/sitemap.xml`, com cache de 1h no `_headers`

**JSON-LD, dois blocos:**
1. `HomeAndConstructionBusiness`: nome, telefone, `areaServed` (Curitiba, Fazenda
   Rio Grande e região metropolitana), horário e `makesOffer` com os 5 serviços
   confirmados.
2. `FAQPage` com as 4 perguntas, **gerado a partir do HTML do próprio FAQ**, para
   não haver divergência entre o que o Google lê e o que o usuário vê. Ao editar
   uma pergunta, regenerar o bloco.

> Deixei de fora, de propósito: `aggregateRating` (a empresa não tem avaliações;
> declarar nota inventada é motivo de penalização manual do Google) e o endereço
> de rua (o barracão não foi confirmado como endereço público). Quando o Meu
> Negócio existir, os dois entram juntos.

## Deploy

Repositório: `gabrielpriss/moveta-moveis`. Projeto Cloudflare Pages: `moveta-moveis`.

```bash
npm run deploy    # wrangler pages deploy public --project-name=moveta-moveis
```

O `.gitignore` exclui `arte-original/` e `fotos-originais/` (~10 MB), que ficam
no Drive do cliente.

## Negrito nos blocos de texto

Aplicado em 10/08: 29 termos em `<strong>` nos blocos longos (FAQ, cards de
diferenciais, "Sobre", aberturas de seção, etapas do processo). Critério: **1 a 2
por parágrafo**, sempre no diferencial ou no número decisivo (25 dias, no seu
endereço, antes de fechar, cada centímetro, medida real). Bold demais anula o
próprio destaque.

A cor acompanha o fundo: `text-white` sobre carvão, `text-carvao` sobre creme e
areia. Verificado que nenhum ficou com contraste invertido.

> ⚠️ As respostas do FAQ existem **duas vezes** no arquivo: no HTML e no JSON-LD.
> O negrito entra só no HTML; o schema fica em texto puro. Ao editar, limitar a
> busca ao trecho depois de `</head>`.

## Reunião de apresentação ao cliente (10/08/2026)

Participantes: Eduardo, Grazi e Diego (o marceneiro sócio). Transcrição em
`Meeting Transcription (84).txt`.

### Aplicado (fechado na reunião)

| Mudança | Ref. |
|---|---|
| Foto da cozinha trocada: o fogão roubava a atenção (15.37.01 → 15.36.59, sem fogão no quadro) | 07:32 |
| Foto do escritório trocada: o móvel estava cortado e não favorecia o gaveteiro (16.00.36 → 16.00.34-1) | 07:38 |
| Fotos de **dormitório e home office trocadas entre si**: estavam invertidas | 14:13 |
| Título do residencial virou **"Sua casa pronta até o final do ano"** | 24:14 |
| Exemplo do prazo deixou de ser cozinha: Eduardo confirmou que **cozinha é dos mais demorados**. Agora é guarda-roupa ou painel de TV | 36:20 |
| Instagram no rodapé | 15:53, 33:17 |
| Fotos das galerias **clicáveis com lightbox** | 36:36 |
| Botão destacado "Solicitar catálogo no WhatsApp" nos acabamentos | 44:06 |

O **prazo de 25 dias foi mantido**: Diego e Eduardo confirmaram que dá para
entregar, contando a partir do fechamento (35:30 a 36:02).

### Pendente, aguardando material do cliente
- **Foto de lavanderia de verdade**: a atual não é lavanderia. A Grazi ia mandar (12:18)
- **Fotos dos acabamentos**: trocar os blocos de cor por madeiras reais. Ninguém tinha o material na reunião (44:51)
- **Antes e depois**: Eduardo sugeriu um comparador deslizante. Depende de pares de fotos do mesmo ângulo (12:49)
- **Foto da equipe** na seção "Quem faz" (27:28)
- **CNPJ no rodapé**: acordado, mas o número não foi passado e o CNPJ está em transição (33:17)
- **Handle do Instagram**: o perfil ainda estava como "deg"; a Grazi ia trocar para movetaplanejados no mesmo dia. Confirmar antes de publicar (17:22, 55:29)

### Discutido sem decisão, não aplicar sem confirmar
- Renomear "Dormitório" para "Quarto": Gabriel disse "talvez ficaria mais natural", ninguém fechou (11:58)
- Última seção considerada repetitiva por Gabriel e Eduardo, mas sem decisão entre remover ou substituir (32:15, 34:31)
- Empresas tem 4 cards contra 6 do residencial: Gabriel levantou, sem decisão (14:36)
- Power numbers: possibilidade de incluir "projetos entregues", sem decisão (29:30)
