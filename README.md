# Solução de Anonimização - Hackathon Participa DF (Categoria Acesso à Informação)

Este projeto apresenta uma solução automatizada para identificar dados pessoais em pedidos de acesso à informação, utilizando técnicas híbridas de Expressões Regulares (Regex) e Processamento de Linguagem Natural (NLP).

## 🗂️ Estrutura do Projeto 

A organização dos arquivos segue uma lógica modular para facilitar a manutenção:

* **`main.py`**: Script principal responsável por orquestrar a execução, carregar os dados e gerar o relatório final.
* **`assets/`**: Módulos auxiliares contendo a lógica de negócio.
    *`LoadData.py`: Gerencia o carregamento de arquivos e recursos pesados (Modelo Spacy, Base IBGE).
    *`private_data.py`: Contém as regras de detecção de dados sensíveis (CPFs, e-mails, nomes).
    *`manipulate_str.py`: Funções utilitárias para tratamento de strings e normalização.
* **`data/`**: Diretório destinado aos arquivos de entrada (`.xlsx`) e bases de conhecimento (regras e nomes do IBGE).
* **`requirements.txt`**: Lista de dependências para instalação automatizada.

---

## ⚙️ Instalação e Configuração

### 1. Pré-requisitos
 **Linguagem**: Python 3.12.3 ou superior.
 **Sistema Operacional**: Windows, Linux ou macOS.

### 2. Configuração do Ambiente 
Recomenda-se o uso de um ambiente virtual para isolar as dependências. Execute os comandos abaixo sequencialmente no terminal, a partir da raiz do projeto:

**Windows:**
bash
python -m venv venv
venv\Scripts\activate  

### 3. Configuração da Pasta Data
Para que o programa funcione é necessário o armazenamento do arquivo de entrada na pasta `data` que deve estar no formato `.xlsx` e com o nome `.amostra.xlsx`. Caso deseje colocar o arquivo com outro nome, basta ir no arquivo `.main.py` e trocar o argumento do método `.LoadData` pelo nome do arquivo, mas sem a extensão `.xlsx`.