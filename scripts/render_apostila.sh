#!/bin/bash
set -e

# Renderizar o PDF da apostila apenas quando for um render completo do projeto (quarto render).
# Evita compilar o PDF repetidamente em modo de preview (quarto preview).
if [ "$QUARTO_PROJECT_RENDER_ALL" = "1" ] && [ -z "$QUARTO_POST_RENDER" ]; then
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
