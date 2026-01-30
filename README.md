# Solução de Anonimização - Hackathon Participa DF (Categoria Acesso à Informação)

Este projeto apresenta uma solução automatizada para identificar dados pessoais em pedidos de acesso à informação, utilizando técnicas híbridas de Expressões Regulares (Regex) e Processamento de Linguagem Natural (NLP), por meio da biblioteca Spacy.



## 🗂️ Estrutura do Projeto 

A organização dos arquivos segue uma lógica modular para facilitar a manutenção:

* **`main.py`**: Script principal responsável por orquestrar a execução, carregar os dados e gerar o relatório final.
* **`assets/`**: Módulos auxiliares contendo a lógica de negócio.
    ***`LoadData.py`***: Gerencia o carregamento de arquivos e recursos pesados (Modelo Spacy, Base IBGE).
    *`private_data.py`: Contém as regras de detecção de dados sensíveis (CPFs, e-mails, nomes).
    *`manipulate_str.py`: Funções utilitárias para tratamento de strings e normalização.
* **`data/`**: Diretório destinado aos arquivos de entrada (`.xlsx`) e bases de conhecimento (regras e nomes do IBGE).
* **`requirements.txt`**: Lista de dependências para instalação automatizada.

---

## ⚙️ Instalação e Configuração

### 1. Pré-requisitos
 **Linguagem**: Python 3.12.3. OBS: versões mais recentes do python não irão funcionar.
 **Sistema Operacional**: Windows, Linux ou macOS.

### 2. Configuração do Ambiente 
Recomenda-se o uso de um ambiente virtual para isolar as dependências. Execute os comandos abaixo sequencialmente no terminal, a partir da raiz do projeto:

**Windows:**
bash

python -m venv venv

venv\Scripts\activate

**Linux/ MacOS:**
bash

python3 -m venv venv

source venv/bin/activate


### 3. Formato de Dados 
Entrada esperada(`data/amostra.xlsx`): O arquivo deve ser uma planilha Excel (.xlsx) contendo obrigatoriamente:

**Nome do Arquivo**: `amostra.xlsx`

**Nome da Coluna que se Encontra o Texto**: `Texto Mascarado`

**Localização do Arquivo**: `data/amostra.xlsx`


Ou seja, este formato de entrada a mesma estrutura do arquivo que foi oferecido de exemplo.

### 4. Instalação de Dependências e Como executar:
bash


pip install -r requirements.txt

python3 main.py


## Após a Execução
### 1. Saída Gerada(`gabarito.xlsx`)

O script irá gerar um arquivo na raiz do projeto chamado gabarito.xlsx, contendo os dados originais acrescidos da seguinte coluna:

**Contendo Dados Pessoais**: Valor Booleano (True ou False) indicando se foram encontrados dados sensíveis.


## Lógica Implementada

A solução utiliza uma abordagem em camadas ("Pipeline de Detecção") para maximizar a precisão e evitar falsos positivos:

1.  **Sanitização e Tratamento de Ruído**:
    * Antes da análise, o texto passa por uma limpeza que identifica e mascara números de processos administrativos (CNJ, SEI, Protocolos). Isso impede que números públicos de processos sejam confundidos com CPFs ou RGs.

2.  **Identificação de Padrões Rígidos (Regex)**:
    * Utilização de Expressões Regulares otimizadas para detectar formatos fixos obrigatórios: **CPF, RG, CNH, E-mail e Telefone**.

3.  **Processamento de Linguagem Natural (NLP)**:
    * Uso da biblioteca **Spacy** (modelo `pt_core_news_lg`) para identificar entidades nomeadas do tipo `PER` (Pessoas) dentro do contexto da frase, permitindo encontrar nomes que não seguem padrões numéricos.

4.  **Validação Cruzada e Heurísticas**:
    * Os nomes candidatos identificados pela IA passam por uma validação dupla para garantir que não são palavras comuns (falsos positivos):

        * **Regras Blacklist**: Utilização de uma lista de bloqueio categorizada para refinar a extração:
            * **INVALIDADORA**: Termos que, se presentes, descartam imediatamente o candidato (ex: "Secretaria", "Ministério"), pois indicam que a IA confundiu uma organização com uma pessoa.
            * **LIMPEZA**: Termos ignorados durante a montagem do nome, como pronomes de tratamento (ex: "Sr.", "Sra.", "Dr.").
            * **CORTE**: Termos que sinalizam o fim do nome próprio e o início de um contexto externo, servindo para truncar a captura quando a IA excede os limites do nome (ex: cargos ou departamentos colados ao nome).
        * **Base IBGE**: Verificação se o nome consta na base de dados do Censo IBGE.
        * **Verificação de Vocabulário**: Se o nome não for comum, o sistema verifica se é uma palavra de dicionário (ex: "Mesa", "Cadeira"). Se não for palavra de dicionário, é considerado um nome próprio raro, aumentando a sensibilidade do modelo.

## 📜 Licença e Créditos

Este projeto foi desenvolvido para fins de participação no **1º Hackathon em Controle Social: Desafio Participa DF**.

### Créditos e Atribuições
A solução utiliza recursos open-source e dados públicos, aos quais agradeço:

* **IBGE (Instituto Brasileiro de Geografia e Estatística)**: A base de validação de nomes utiliza dados do Censo Demográfico, disponibilizados através do repositório [datasets-br/prenomes](https://github.com/datasets-br/prenomes).
* **Spacy**: Biblioteca de Processamento de Linguagem Natural utilizada sob a licença MIT. O modelo `pt_core_news_lg` é distribuído pela Explosion AI.
* **Pandas & OpenPyXL**: Bibliotecas fundamentais para a manipulação dos dados tabulares e arquivos Excel.



