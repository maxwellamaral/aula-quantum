"""Post-render: gera o PDF da apostila apenas em renders completos do projeto.

Substituto multiplataforma de render_apostila.sh (funciona no Windows e Unix).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Garante saída UTF-8 no Windows (console do Quarto não aceita bytes não-UTF-8)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    # Evita compilar o PDF repetidamente em modo de preview (quarto preview)
    if os.environ.get("QUARTO_PROJECT_RENDER_ALL") != "1" or os.environ.get("QUARTO_POST_RENDER"):
        print("Modo preview/parcial detectado. Geração do PDF ignorada.")
        return 0

    pdf = ROOT / "content" / "apostila.pdf"
    if pdf.exists():
        try:
            subprocess.run(
                ["git", "diff", "--quiet", "HEAD", "--",
                 "content/*/_content.qmd", "content/apostila.qmd"],
                cwd=ROOT, check=True,
            )
            print("Apostila PDF atual e sem mudanças de conteúdo — geração pulada.")
            return 0
        except FileNotFoundError:
            pass  # git indisponível: segue com o render
        except subprocess.CalledProcessError:
            pass  # houve mudanças: re-renderiza

    print("Renderizando apostila.qmd para PDF...")
    result = subprocess.run(["quarto", "render", "content/apostila.qmd", "--to", "pdf"], cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    dest_dir = ROOT / "_site" / "content"
    dest_dir.mkdir(parents=True, exist_ok=True)
    if pdf.exists():
        shutil.copy2(pdf, dest_dir / "apostila.pdf")
        print("Apostila PDF copiada para _site/content/apostila.pdf com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
