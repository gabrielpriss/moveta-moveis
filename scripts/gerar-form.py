#!/usr/bin/env python3
"""
Gera public/form/index.html a partir de public/index.html.

Por que gerar em vez de manter uma segunda pagina: as duas variantes do teste
A/B precisam ser a MESMA pagina, mudando so o destino do CTA. Se fossem dois
arquivos escritos a mao, a primeira troca de foto ou de texto que alguem
fizesse em um deles ja invalidaria o teste, porque as variantes passariam a
comparar coisas diferentes. Aqui a LP e a unica fonte: rode `npm run form`
depois de mexer nela e a variante acompanha.

O que muda na variante:

  1. <title>, canonical, og:url e robots (noindex: a variante e so para o
     trafego pago e nao pode competir com a LP na busca organica)
  2. todo CTA de wa.me vira ancora para #formulario, mantendo data-origem,
     data-perfil e data-ambiente, que o formulario usa para pular etapas
  3. entra a secao #formulario (scripts/form-secao.html), logo depois do
     CTA final e antes do FAQ
  4. entra o script do formulario (scripts/form-script.js)
  5. entra o CSS das bolinhas de progresso

Qualquer marcador que sumir da LP derruba a geracao com erro, de proposito:
melhor falhar aqui do que publicar uma variante pela metade.
"""

import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, 'public', 'index.html')
DESTINO = os.path.join(RAIZ, 'public', 'form', 'index.html')
SECAO = os.path.join(RAIZ, 'scripts', 'form-secao.html')
SCRIPT = os.path.join(RAIZ, 'scripts', 'form-script.js')

AVISO = """<!--
  ============================================================================
  ARQUIVO GERADO. NAO EDITE ESTE ARQUIVO A MAO.
  ============================================================================

  Esta e a variante /form/ do teste A/B: a mesma landing page, com todo CTA
  levando ao formulario em vez de abrir o WhatsApp direto.

  Fonte:  public/index.html  +  scripts/form-secao.html  +  scripts/form-script.js
  Gerar:  npm run form

  Para mudar o conteudo da pagina, edite public/index.html e rode o comando de
  novo. Para mudar as perguntas do formulario, edite scripts/form-secao.html.
  ============================================================================
-->
"""

CSS_EXTRA = """
      /* Progresso do formulario (variante /form/) */
      .f-ponto {
        width: .5rem; height: .5rem; border-radius: 9999px;
        background: #211D1A26; transition: background-color .25s, transform .25s;
      }
      .f-ponto.is-feito { background: #C9A24B; }
      .f-ponto.is-atual { background: #211D1A; transform: scale(1.35); }
"""


def erro(msg):
    sys.stderr.write('gerar-form: ' + msg + '\n')
    sys.exit(1)


def trocar(html, antigo, novo, quantas=1, rotulo=''):
    """Troca exigindo o numero exato de ocorrencias."""
    achou = html.count(antigo)
    if achou != quantas:
        erro('esperava %d ocorrencia(s) de %s, achei %d. A LP mudou de forma; '
             'ajuste o gerador.' % (quantas, rotulo or repr(antigo[:60]), achou))
    return html.replace(antigo, novo, quantas)


def main():
    for caminho in (ORIGEM, SECAO, SCRIPT):
        if not os.path.exists(caminho):
            erro('nao achei ' + caminho)

    html = io.open(ORIGEM, encoding='utf-8').read()
    secao = io.open(SECAO, encoding='utf-8').read().rstrip('\n')
    script = io.open(SCRIPT, encoding='utf-8').read().rstrip('\n')

    # ── 1. Cabecalho ────────────────────────────────────────────────────────
    html = trocar(
        html,
        '<title>Movetá Móveis Planejados | Sob Medida em Curitiba e Região</title>',
        '<title>Peça seu Orçamento | Movetá Móveis Planejados | Curitiba e Região</title>',
        rotulo='<title>')

    html = trocar(
        html,
        '<link rel="canonical" href="https://movetaplanejados.com.br/">',
        '<link rel="canonical" href="https://movetaplanejados.com.br/form/">',
        rotulo='canonical')

    # noindex: a variante existe so para o trafego pago. Indexar as duas faria
    # o Google escolher uma delas sozinho e ainda dividiria o sinal da LP.
    html = trocar(
        html,
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        '<meta name="robots" content="noindex, follow">\n'
        '    <!-- noindex de proposito: variante de teste A/B, so para trafego pago. -->',
        rotulo='meta robots')

    html = trocar(
        html,
        '<meta property="og:url" content="https://movetaplanejados.com.br/">',
        '<meta property="og:url" content="https://movetaplanejados.com.br/form/">',
        rotulo='og:url')

    # O FAQPage sai: o rich result tem de sair da LP, que e a pagina indexada.
    ini = html.index('<script type="application/ld+json">\n    {\n      "@context": "https://schema.org",\n      "@type": "FAQPage"')
    fim = html.index('</script>', ini) + len('</script>')
    html = html[:ini] + '<!-- FAQPage fica so na LP: aqui a pagina e noindex. -->' + html[fim:]

    # ── 2. Caminhos das imagens ─────────────────────────────────────────────
    # A LP mora na raiz e usa src="assets/...". Dentro de /form/ esse caminho
    # relativo vira /form/assets/... e a pagina abre sem nenhuma foto. Aqui
    # todos viram absolutos.
    relativos = html.count('="assets/')
    if relativos < 40:
        erro('achei so %d caminhos "assets/" na LP; esperava dezenas. '
             'Confira se as imagens mudaram de forma.' % relativos)
    html = html.replace('="assets/', '="/assets/')

    # ── 3. CSS das bolinhas ─────────────────────────────────────────────────
    html = trocar(
        html,
        '      @media (prefers-reduced-motion: reduce) {',
        CSS_EXTRA + '\n      @media (prefers-reduced-motion: reduce) {',
        rotulo='bloco <style>')

    # ── 4. CTAs: wa.me vira ancora para o formulario ────────────────────────
    # O <a> inteiro e reescrito: sai o href do wa.me, saem target e rel (a
    # ancora e na mesma aba) e fica tudo o mais, inclusive os data-*.
    def virar_ancora(m):
        attrs = m.group(1)
        attrs = re.sub(r'\s*target="_blank"', '', attrs)
        attrs = re.sub(r'\s*rel="noopener"', '', attrs)
        return '<a href="#formulario"' + attrs

    html, trocados = re.subn(
        r'<a\s+href="https://wa\.me/[^"]*"((?:(?!</a>).)*?)(?=\sclass=|\s*>)',
        virar_ancora, html, flags=re.S)
    if trocados < 15:
        erro('so %d CTAs de wa.me viraram ancora; esperava os 19 da pagina. '
             'Confira se a LP ainda usa <a href="https://wa.me/...">.' % trocados)

    if 'href="https://wa.me/' in html:
        erro('sobrou link direto de wa.me na variante: a conversao do teste '
             'ficaria contaminada. Verifique a LP.')

    # ── 5. Rotulos dos CTAs ─────────────────────────────────────────────────
    # Um botao escrito "Falar no WhatsApp agora" que rola ate um formulario
    # quebra a expectativa de quem clicou, e quem desiste ali derruba a
    # conversao da variante por um motivo que nao e o que o teste quer medir.
    # Trocamos so o que promete WhatsApp imediato; o que descreve o processo
    # ("Resposta no WhatsApp", "Conversa no WhatsApp") continua verdadeiro,
    # porque o formulario termina abrindo o WhatsApp do mesmo jeito.
    for antigo, novo, rotulo in [
        ('aria-label="Pedir orçamento no WhatsApp"', 'aria-label="Pedir orçamento"', 'aria-label do header'),
        ('      Falar no WhatsApp agora\n',          '      Pedir meu orçamento\n',  'CTA final'),
        ('              WhatsApp\n            </a>', '              Pedir orçamento\n            </a>', 'link do rodapé'),
        ('aria-label="Falar no WhatsApp"',           'aria-label="Pedir orçamento"', 'aria-label do botão flutuante'),
        ('    Pedir orçamento no WhatsApp\n',        '    Pedir meu orçamento\n',    'barra mobile'),
    ]:
        html = trocar(html, antigo, novo, rotulo=rotulo)

    # ── 6. Secao do formulario, entre o CTA final e o FAQ ───────────────────
    marca_faq = ('<!-- ═══════════════════════════════════════════════════════════\n'
                 '     12. FAQ: termos soft para o Google Ads / SEO')
    html = trocar(html, marca_faq, secao + '\n\n' + marca_faq, rotulo='inicio do FAQ')

    # ── 7. Script do formulario ─────────────────────────────────────────────
    marca_js = '  // ── Carrosséis de obras (hero e "Quem faz") ─────────────────'
    html = trocar(html, marca_js, script + '\n\n' + marca_js, rotulo='inicio dos carrosseis')

    # ── 8. Aviso de arquivo gerado ──────────────────────────────────────────
    html = html.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + AVISO, 1)

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    io.open(DESTINO, 'w', encoding='utf-8').write(html)

    print('gerado: public/form/index.html')
    print('  %d CTAs agora apontam para #formulario' % trocados)
    print('  %.1f KB' % (len(html.encode('utf-8')) / 1024.0))


if __name__ == '__main__':
    main()
