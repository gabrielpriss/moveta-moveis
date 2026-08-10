#!/usr/bin/env python3
"""
Prepara as fotos das obras para a LP.

    python3 scripts/tratar-fotos.py

Origem: `fotos-originais/` (fotos reais das obras, vindas do Drive do cliente).

Para cada slot ha uma largura-alvo, calculada a partir do tamanho que ele ocupa
na pagina vezes 2 (telas retina). O tratamento muda conforme a origem:

  - origem >= alvo  -> reduz com Lanczos e aplica nitidez leve, so para
                       recuperar o micro-contraste que toda reducao come;
  - origem <  alvo   -> amplia com Lanczos e aplica nitidez um pouco mais
                       forte. NUNCA passa de 2x: acima disso o ganho e nulo
                       e o arquivo so engorda.

Algumas fotos trazem marca d'agua do celular no rodape ("POCO X6 5G",
data e hora). O campo `cortar_rodape` remove essa faixa antes de tudo.

Notas de ajuste, para quem for mexer: nao existe filtro de mediana antes da
ampliacao. Foi testado e apagava detalhe de 1px (as frestas entre gavetas
viravam linha tracejada). A mascara de nitidez usa raio 1.1; valores maiores
criavam halo visivel nas bordas de alto contraste.
"""

from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAIS = RAIZ / 'fotos-originais'
DESTINO = RAIZ / 'public' / 'assets'

QUALIDADE = 88

# nome-base: (arquivo de origem, largura-alvo, fracao do rodape a cortar)
#
# A largura-alvo e o tamanho que o slot ocupa na pagina vezes 2 (retina),
# arredondado para cima. `cortar_rodape` remove a marca d'agua do celular
# ("POCO X6 5G" + data) que aparece em varias fotos de cozinha.
FOTOS = {
    # ---- Hero: duas laterais estaticas ----
    'hero-detalhe-1':          ('15.58.05.jpg',        420, 0),
    'hero-detalhe-2':          ('16.00.34-1.jpg',      420, 0),

    # ---- Hero: carrossel, alternando residencial e comercial ----
    'hero-slide-01':           ('15.36.42-1.jpg',      800, 0),      # R painel ripado com TV
    'hero-slide-02':           ('15.56.44.jpg',        800, 0),      # C balcao de recepcao
    'hero-slide-03':           ('15.58.02.jpg',        800, 0),      # R home office fendi
    'hero-slide-04':           ('16.00.33.jpg',        800, 0),      # C escritorio mesa em L
    'hero-slide-05':           ('15.36.59.jpg',        800, 0.06),   # R cozinha branca
    'hero-slide-06':           ('0722-17.11.36-1.jpg', 800, 0),      # C mesa de reuniao
    'hero-slide-07':           ('15.37.05-1.jpg',      800, 0),      # R painel com TV ligada
    'hero-slide-08':           ('16.00.36.jpg',        800, 0),      # C estacoes de trabalho
    'hero-slide-09':           ('15.36.40-1.jpg',      800, 0),      # R armarios com nichos
    'hero-slide-10':           ('15.37.24.jpg',        800, 0),      # C sala de reuniao com TV

    # ---- Cards residenciais ----
    'residencial-cozinha':     ('15.36.59.jpg',       1200, 0.06),
    'residencial-dormitorio':  ('15.57.58-1.jpg',      800, 0),
    'residencial-painel-tv':   ('15.37.05-1.jpg',      800, 0),
    'residencial-banheiro':    ('15.58.04-1.jpg',      800, 0),
    'residencial-lavanderia':  ('15.36.58.jpg',        800, 0),
    'residencial-home-office': ('15.36.40-1.jpg',      800, 0),

    # ---- Cards de empresa ----
    'empresa-mesa':            ('15.56.44.jpg',       1200, 0),
    'empresa-escritorio':      ('16.00.33.jpg',        800, 0),
    'empresa-sala-reuniao':    ('0722-17.11.36-1.jpg', 800, 0),
    'empresa-armarios':        ('15.36.39-1.jpg',      800, 0),
    'empresa-painel-tv':       ('15.37.24.jpg',        800, 0),

    # ---- Galeria residencial (carrossel abaixo de "Quem faz") ----
    'galeria-res-01':          ('15.36.42.jpg',        560, 0),
    'galeria-res-02':          ('15.36.40-2.jpg',      560, 0),
    'galeria-res-03':          ('15.37.10.jpg',        560, 0),
    'galeria-res-04':          ('15.36.53.jpg',        560, 0),
    'galeria-res-05':          ('15.37.09.jpg',        560, 0),
    'galeria-res-06':          ('15.37.23.jpg',        560, 0),
    'galeria-res-07':          ('15.58.03-1.jpg',      560, 0),
    'galeria-res-08':          ('15.36.41.jpg',        560, 0),

    # ---- Galeria comercial ----
    'galeria-com-01':          ('16.00.34-1.jpg',      560, 0),
    'galeria-com-02':          ('16.00.35.jpg',        560, 0),
    'galeria-com-03':          ('16.00.36-2.jpg',      560, 0),
    'galeria-com-04':          ('16.00.37.jpg',        560, 0),
    'galeria-com-05':          ('0722-17.11.36.jpg',   560, 0),
    'galeria-com-06':          ('15.36.50-2.jpg',      560, 0),
    'galeria-com-07':          ('16.00.33-1.jpg',      560, 0),
    'galeria-com-08':          ('16.00.38.jpg',        560, 0),
}


def tratar(origem: Path, alvo: int, cortar_rodape: float) -> Image.Image:
    img = Image.open(origem).convert('RGB')

    if cortar_rodape:
        img = img.crop((0, 0, img.width, int(img.height * (1 - cortar_rodape))))

    ampliando = img.width < alvo
    largura = min(alvo, img.width * 2)          # teto de 2x
    altura = round(img.height * largura / img.width)
    img = img.resize((largura, altura), Image.LANCZOS)

    forca = 90 if ampliando else 60
    img = img.filter(ImageFilter.UnsharpMask(radius=1.1, percent=forca, threshold=2))

    if ampliando:                                # miniatura costuma vir lavada
        img = ImageEnhance.Contrast(img).enhance(1.05)
        img = ImageEnhance.Color(img).enhance(1.04)

    return img


def main():
    if not ORIGINAIS.exists():
        raise SystemExit(f'nao encontrei {ORIGINAIS}')

    total = 0
    for base, (arquivo, alvo, corte) in FOTOS.items():
        origem = ORIGINAIS / arquivo
        if not origem.exists():
            print(f'  pulou   {base}: falta {arquivo}')
            continue

        antes = Image.open(origem).size
        img = tratar(origem, alvo, corte)
        saida = DESTINO / f'{base}.webp'
        img.save(saida, 'WEBP', quality=QUALIDADE, method=6)
        (DESTINO / f'{base}.svg').unlink(missing_ok=True)   # tira o placeholder

        kb = saida.stat().st_size // 1024
        total += kb
        marca = ' (rodapé cortado)' if corte else ''
        print(f'  ok   {base:<24} {antes[0]}x{antes[1]} -> {img.width}x{img.height}'
              f'  {kb} KB{marca}')

    print(f'\ntotal: {total} KB')


if __name__ == '__main__':
    main()
