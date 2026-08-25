"""Smoke test: garante que os módulos de conteúdo existem e não estão vazios."""
from pathlib import Path

CONTENT = Path(__file__).parent.parent / "content"

MODULOS = [
    "01-panorama",
    "02-fisica-classica-quanticas",
    "03-ondas-dupla-fenda",
    "04-qubit",
    "05-fases",
    "06-circuitos-emaranhamento",
    "07-teletransporte",
    "08-hadamard-experimento",
    "09-interferencia-deutsch-jozsa",
    "10-grover",
    "11-qft-qpe",
    "12-hardware-real",
    "13-qml-vqc",
    "14-compilacao-topologia",
    "15-impacto-engsoft",
]

def test_modulos_tem_content():
    for m in MODULOS:
        f = CONTENT / m / "_content.qmd"
        assert f.exists(), f"faltando {f}"
        assert len(f.read_text(encoding="utf-8")) > 1000, f"{m} muito curto — conversão integral falhou?"

def test_apostila_inclui_todos_os_modulos():
    ap = (CONTENT / "apostila.qmd").read_text(encoding="utf-8")
    for m in MODULOS:
        assert f"include {m}/_content.qmd" in ap, f"apostila não inclui {m}"
