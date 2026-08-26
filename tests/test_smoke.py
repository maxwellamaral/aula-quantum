"""Smoke test: garante que os módulos de conteúdo existem e não estão vazios."""
from pathlib import Path

CONTENT = Path(__file__).parent.parent / "content"

MODULOS = [
    "01-panorama",
    "02-qubit",
    "03-fases",
    "04-circuitos-emaranhamento",
    "05-teletransporte",
    "06-hadamard-experimento",
    "07-interferencia-deutsch-jozsa",
    "08-grover",
    "09-qft-qpe",
    "10-hardware-real",
    "11-qml-vqc",
    "12-compilacao-topologia",
    "13-impacto-engsoft",
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
