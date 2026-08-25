# Fundamentos de Computação Quântica — Curso de Extensão

Site e materiais do curso de extensão **Fundamentos de Computação Quântica para Engenharia de Software** (IFPB — Campus João Pessoa), ministrado pelo Prof. Me. Maxwell Anderson Ielpo do Amaral.

O projeto utiliza **Quarto** para geração do site de documentação/aulas e **Python (via `uv`)** com **Qiskit** para os notebooks executáveis.

---

## 🛠️ Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (Gerenciador de ambientes e pacotes Python)
- [Quarto CLI](https://quarto.org/docs/get-started/) (Gerador de sites e documentos)
- [TeX Live / LuaLaTeX](https://www.tug.org/texlive/) (Necessário para a compilação do PDF da apostila)

## 🚀 Como Utilizar o Projeto

### 1. Clonar e instalar dependências

```bash
git clone git@github.com:maxwellamaral/aula-quantum.git
cd aula-quantum
uv sync
```

### 2. Renderizar o site localmente

```bash
quarto preview          # abre em http://localhost:4201
```

### 3. Gerar a apostila em PDF

```bash
quarto render content/apostila.qmd --to pdf
```

### 4. Executar os notebooks

Os notebooks originais ficam em `notebooks/`:

```bash
uv run jupyter lab notebooks/
```

> 💡 As células de código dos módulos exigem as dependências instaladas (`uv sync`).
> Os arquivos `.qasm` em `notebooks/qasm/` podem ser importados no [IBM Quantum Composer](https://quantum.ibm.com/composer).

---

## 📂 Estrutura

```
aula-quantum/
├── _quarto.yml            # Configuração do site Quarto
├── index.qmd              # Página inicial
├── about.qmd              # Sobre o curso (ficha técnica)
├── content/
│   ├── index.qmd          # Índice de módulos
│   ├── apostila.qmd       # Apostila mestre (PDF único)
│   ├── references.bib     # Bibliografia central
│   └── NN-modulo/         # Um diretório por aula
│       ├── index.qmd      # Página da aula
│       ├── _content.qmd   # Conteúdo integral (incluído por index e apostila)
│       └── slides.qmd     # Slides RevealJS (opcional)
├── notebooks/             # Notebooks Jupyter originais + QASM
│   └── qasm/
├── assets/
│   ├── css/               # Tema escuro "Dark Abyss"
│   ├── js/
│   ├── images/
│   └── simuladores/       # Simuladores HTML interativos
├── src/                   # Módulos Python de apoio (quantum_viz.py)
├── scripts/               # Utilitários (render_apostila.sh, nb_to_content.py)
└── .github/workflows/     # CI: render + publish no GitHub Pages
```
