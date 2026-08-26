#!/bin/bash
set -e

# Renderizar o PDF da apostila apenas quando for um render completo do projeto (quarto render).
# Evita compilar o PDF repetidamente em modo de preview (quarto preview).
# Pula a geracao se o PDF ja existe e nenhum _content.qmd mudou desde ele (modo CI)
if command -v git >/dev/null 2>&1 && [ -f content/apostila.pdf ] && git diff --quiet HEAD -- content/*/_content.qmd content/apostila.qmd 2>/dev/null; then
  echo "Apostila PDF atual e sem mudancas de conteudo — geracao pulada."
elif [ "$QUARTO_PROJECT_RENDER_ALL" = "1" ] && [ -z "$QUARTO_POST_RENDER" ]; then
  export QUARTO_POST_RENDER=1
  echo "Renderizando apostila.qmd para PDF..."
  quarto render content/apostila.qmd --to pdf
  mkdir -p _site/content
  if [ -f "content/apostila.pdf" ]; then
    cp content/apostila.pdf _site/content/apostila.pdf
    echo "Apostila PDF copiada para _site/content/apostila.pdf com sucesso."
  fi
else
  echo "Modo preview/parcial detectado. Geração do PDF ignorada."
fi
