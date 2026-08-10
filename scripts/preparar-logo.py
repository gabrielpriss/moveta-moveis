#!/usr/bin/env python3
"""
Prepara a logo oficial para uso na LP a partir de `logo horizontal.png`.

A arte original e um mockup: letreiro metalico fotografado sobre parede escura,
com vinheta. Para usar no header e no rodape a gente precisa dela recortada e
com fundo transparente.

Como o fundo sai por luminancia: o metal (dourado e prata) fica acima de L=105 e
a parede fica abaixo de L=55. A rampa entre os dois vira o canal alfa, o que
preserva as bordas suaves e o relevo. Isso e seguro aqui porque a logo sempre
aparece sobre fundo escuro na pagina, entao qualquer sombra que fique
semitransparente mostra um escuro parecido por tras.

Gera:
  public/assets/logo-moveta.png     horizontal, transparente (header e rodape)
  public/assets/favicon-moveta.png  so o monograma, quadrado

    python3 scripts/preparar-logo.py
"""

from pathlib import Path
from PIL import Image, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / 'public' / 'assets'
ORIGEM = ASSETS / 'logo horizontal.png'

# Rampa de luminancia que vira alfa. Valores medidos na propria arte:
# a parede vai no maximo a L=67 e 95% do metal esta acima de L=108, entao a
# faixa 70..112 separa os dois sem comer o relevo do dourado.
L_FUNDO = 70    # abaixo disto e parede: totalmente transparente
L_METAL = 112   # acima disto e letreiro: totalmente opaco

ALTURA_LOGO = 240      # 2x a maior altura usada na pagina (rodape h-14 = 56px)
LADO_FAVICON = 256


def alfa_por_luminancia(img):
    """Monta o alfa a partir do brilho, com rampa suave entre fundo e metal."""
    cinza = img.convert('L')
    # Desfoque leve so no calculo do alfa: tira ruido do JPEG/parede sem
    # borrar as bordas do metal, que vem do RGB original.
    base = cinza.filter(ImageFilter.GaussianBlur(0.6))
    escala = 255.0 / (L_METAL - L_FUNDO)
    alfa = base.point(lambda v: 0 if v <= L_FUNDO
                      else (255 if v >= L_METAL
                            else int((v - L_FUNDO) * escala)))
    return alfa


def recortar_no_conteudo(rgba, margem=8):
    caixa = rgba.getchannel('A').getbbox()
    if not caixa:
        return rgba
    e, c, d, b = caixa
    w, h = rgba.size
    return rgba.crop((max(0, e - margem), max(0, c - margem),
                      min(w, d + margem), min(h, b + margem)))


def main():
    if not ORIGEM.exists():
        raise SystemExit(f'nao encontrei {ORIGEM}')

    original = Image.open(ORIGEM).convert('RGB')
    rgba = original.copy()
    rgba.putalpha(alfa_por_luminancia(original))

    # ---- Logo horizontal ----
    logo = recortar_no_conteudo(rgba)
    escala = ALTURA_LOGO / logo.height
    logo = logo.resize((round(logo.width * escala), ALTURA_LOGO), Image.LANCZOS)
    logo.save(ASSETS / 'logo-moveta.png', optimize=True)
    print(f'logo-moveta.png       {logo.width}x{logo.height}'
          f'  ({(ASSETS / "logo-moveta.png").stat().st_size // 1024} KB)')

    # ---- Favicon: so o monograma ----
    # O monograma ocupa o primeiro terco da arte; recorta essa faixa e
    # reaproveita o bbox do alfa para centralizar no quadrado.
    faixa = rgba.crop((0, 0, rgba.width // 3, rgba.height))
    mono = recortar_no_conteudo(faixa, margem=6)
    lado = max(mono.size)
    quadrado = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    quadrado.paste(mono, ((lado - mono.width) // 2, (lado - mono.height) // 2))
    quadrado = quadrado.resize((LADO_FAVICON, LADO_FAVICON), Image.LANCZOS)
    quadrado.save(ASSETS / 'favicon-moveta.png', optimize=True)
    print(f'favicon-moveta.png    {LADO_FAVICON}x{LADO_FAVICON}'
          f'  ({(ASSETS / "favicon-moveta.png").stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
