# Identificação de Regiões Genéticas Conservadas (LCS)

Este projeto implementa o algoritmo **LCS (Longest Common Subsequence)** para identificar regiões conservadas em sequências biológicas (DNA, RNA ou proteínas). Desenvolvido no âmbito da disciplina de **Computação e Programação (2024/25)**.

O sistema permite alinhar duas ou mais sequências e visualizar os resultados através de uma interface de linha de comando (CLI) e gráficos interativos.

## Funcionalidades

* **Cálculo de LCS:** Identifica a maior subsequência comum entre:
    * Sequências (Matriz Dinâmica padrão).
    * 3 Sequências (Tensor 3D).
    * N Sequências (Generalização).


* **Gestão de Dados:**
    * Inserção manual de sequências.
    * Carregamento de arquivos no formato **FASTA**.

* **Análise e Visualização:**
    * Exibição detalhada do alinhamento e score de identidade.
    * Geração de mapas de visualização interativa (usando Plotly).

## Requisitos
* Python 3.x
* Bibliotecas listadas em `requirements.txt`

## Instalação e Execução

1. **Clone o repositório** ou baixe os arquivos.
2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
python main.py
```

## Estrutura do Projeto

* `main.py`: Menu principal e interface CLI.
* `lcs_finder.py`: Implementação do algoritmo LCS para 2 e 3 sequências.
* `lcs_finder_n_sequences.py`: Implementação do algoritmo para N sequências.
* `sequence.py` / `sequence_database.py`: Classes para modelagem e armazenamento das sequências.
* `visualize.py`: Módulo responsável pela geração dos gráficos com Plotly.
* `fasta_file.fasta` / `example.fasta`: Exemplos de arquivos de entrada.

---

*Projeto académico - 2024/2025*
