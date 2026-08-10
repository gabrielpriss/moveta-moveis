#!/usr/bin/env bash
#
# Aplica as fotos reais na LP, substituindo os placeholders SVG.
#
#   ./scripts/aplicar-fotos.sh <pasta-com-as-fotos>
#
# A pasta deve conter arquivos com os nomes-base listados abaixo (qualquer
# extensao: jpg, jpeg, png ou webp). O script redimensiona, grava em
# public/assets/ e troca a referencia no index.html apenas das fotos
# encontradas. O que nao estiver na pasta continua como placeholder.
#
# Formato de saida:
#   - com `cwebp` ou `magick` instalado  -> .webp (recomendado)
#   - sem nenhum dos dois                -> .jpg via `sips` (nativo do macOS;
#                                           o sips le webp mas nao escreve)
#   Para ativar o webp:  brew install webp
#
# Nomes-base esperados:
#
#   hero-principal            foto grande do hero (paisagem)
#   hero-detalhe-1            foto vertical do hero
#   hero-detalhe-2            foto pequena do hero (paisagem)
#   residencial-cozinha       card Cozinha
#   residencial-dormitorio    card Dormitorio
#   residencial-painel-tv     card Sala
#   residencial-banheiro      card Banheiro
#   residencial-lavanderia    card Lavanderia
#   residencial-home-office   card Home office
#   empresa-escritorio        card Moveis para escritorio
#   empresa-painel-tv         card Painel para TV
#   empresa-armarios          card Armarios e divisorias
#   empresa-sala-reuniao      card Mesa de reuniao
#   processo-medicao          etapa de medicao
#   processo-apresentacao     apresentacao do projeto
#   sobre-equipe              foto dos socios
#   marcenaria-01/02/03       faixa de producao e montagem
#
set -euo pipefail

ORIGEM="${1:-}"
if [ -z "$ORIGEM" ] || [ ! -d "$ORIGEM" ]; then
  echo "uso: $0 <pasta-com-as-fotos>" >&2
  exit 1
fi

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DESTINO="$RAIZ/public/assets"
HTML="$RAIZ/public/index.html"
LARGURA_MAX=1600

# Decide o formato de saida uma vez, conforme as ferramentas disponiveis.
if command -v cwebp >/dev/null 2>&1;   then MOTOR=cwebp; EXT=webp
elif command -v magick >/dev/null 2>&1; then MOTOR=magick; EXT=webp
elif command -v sips >/dev/null 2>&1;   then MOTOR=sips;   EXT=jpg
else
  echo "erro: nenhum conversor de imagem encontrado (cwebp, magick ou sips)." >&2
  exit 1
fi

echo "conversor: $MOTOR  ->  .$EXT"
if [ "$MOTOR" = "sips" ]; then
  echo "dica: 'brew install webp' habilita saida em .webp (arquivos ~30% menores)."
fi
echo

# Largura original, para nunca ampliar: upscale nao cria detalhe, so borra
# a imagem e aumenta o arquivo.
largura_de() {
  sips -g pixelWidth "$1" 2>/dev/null | awk '/pixelWidth/{print $2}'
}

converter() {
  local entrada="$1" saida="$2"
  local w; w="$(largura_de "$entrada")"
  local alvo="$LARGURA_MAX"
  [ -n "$w" ] && [ "$w" -lt "$LARGURA_MAX" ] && alvo="$w"

  case "$MOTOR" in
    cwebp)  cwebp -quiet -q 82 -resize "$alvo" 0 "$entrada" -o "$saida" ;;
    magick) magick "$entrada" -resize "${alvo}x>" -quality 82 "$saida" ;;
    sips)
      # Ja e jpeg e nao precisa redimensionar: copia sem reprocessar,
      # para nao perder qualidade num segundo ciclo de compressao.
      # (case sem ${var,,}: o bash do macOS e 3.2 e nao tem essa expansao)
      case "$entrada" in
        *.jpg|*.jpeg|*.JPG|*.JPEG)
          if [ "$alvo" != "$LARGURA_MAX" ]; then cp "$entrada" "$saida"; return 0; fi ;;
      esac
      sips -s format jpeg -s formatOptions 82 -Z "$alvo" "$entrada" --out "$saida" >/dev/null ;;
  esac
}

BASES=(
  hero-principal hero-detalhe-1 hero-detalhe-2
  residencial-cozinha residencial-dormitorio residencial-painel-tv
  residencial-banheiro residencial-lavanderia residencial-home-office
  empresa-escritorio empresa-painel-tv empresa-armarios empresa-sala-reuniao
  processo-medicao processo-apresentacao sobre-equipe
  marcenaria-01 marcenaria-02 marcenaria-03
)

aplicadas=0
for base in "${BASES[@]}"; do
  entrada=""
  for ext in webp jpg jpeg png JPG JPEG PNG WEBP; do
    if [ -f "$ORIGEM/$base.$ext" ]; then entrada="$ORIGEM/$base.$ext"; break; fi
  done
  [ -z "$entrada" ] && continue

  if converter "$entrada" "$DESTINO/$base.$EXT"; then
    # Troca a referencia so desta imagem, seja ela ainda .svg ou ja convertida antes.
    sed -i '' -E "s#assets/${base}\.(svg|webp|jpg)#assets/${base}.${EXT}#g" "$HTML"
    # Remove o placeholder e eventual saida de um formato anterior.
    rm -f "$DESTINO/$base.svg"
    [ "$EXT" != "webp" ] && rm -f "$DESTINO/$base.webp"
    [ "$EXT" != "jpg" ]  && rm -f "$DESTINO/$base.jpg"
    printf '  ok   %s.%s\n' "$base" "$EXT"
    aplicadas=$((aplicadas + 1))
  else
    printf '  falhou  %s\n' "$base" >&2
  fi
done

echo
echo "$aplicadas foto(s) aplicada(s)."
echo "placeholders restantes:"
restantes=0
for base in "${BASES[@]}"; do
  if [ -f "$DESTINO/$base.svg" ]; then
    printf '  %s\n' "$base"
    restantes=$((restantes + 1))
  fi
done
if [ "$restantes" -eq 0 ]; then echo "  nenhum"; fi
