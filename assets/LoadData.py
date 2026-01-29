import pandas as pd
import spacy
import sys
import assets.manipulate_str as ms

class LoadData:
    def __init__(self, nome_arquivo):
        """
        Método responsável por carregar as informações necessárias para a identificação
        dos dados sensíveis. 
        
        :param: O parâmetro é o nome do nosso arquivo de entrada no formato de xlsx,
        mas coloque o nome sem a extensão e veja se o arquivo esta na pasta data.
       
        """
        self.BLACKLIST_INVALIDADORA, self.BLACKLIST_LIMPEZA, self.BLACKLIST_CORTE = self._carregar_regras_blacklist()
        self.nlp = self._carregar_modelo_spacy()
        self.banco_ibge = self._carregar_banco_nomes_offline()
        self.df = self._carregar_entrada(nome_arquivo)
        
    


    def _carregar_regras_blacklist(self):
        """"
        Método responsável por carregar e retornar a nossa blacklist, ou seja, as palavras que iremos tomar cuidado
        ao analisar. Mais detalhes se encontram no README
        """
        try:
            df = pd.read_csv('data/regras_blacklist.csv')
            
            # Cria as 3 listas filtrando pelo tipo
            lista_invalidadora = set(df[df['tipo'] == 'INVALIDADORA']['termo'].str.lower().tolist())
            lista_limpeza = set(df[df['tipo'] == 'LIMPEZA']['termo'].str.lower().tolist())
            lista_corte = set(df[df['tipo'] == 'CORTE']['termo'].str.lower().tolist())
            return lista_invalidadora, lista_limpeza, lista_corte
            
        except FileNotFoundError:
            print("AVISO: Arquivo 'regras_blacklist.csv' não encontrado.")
            print("Usando listas de emergência (vazias).")
            return set(), set(), set()
        
    def _carregar_modelo_spacy(self):
        """"
        Método responsável por carregar e retornar a biblioteca spacy que é responsável pelo processamento
        em linguagem natural, ou seja, possui a função de fazer a primeira triagem de quais
        palavras são nomes próprios ou não.
        """
        try:
            return spacy.load("pt_core_news_lg")
        except:
            print("MODELO NÃO ENCONTRADO. Baixando...")
            import os
            os.system("python -m spacy download pt_core_news_lg")
            return spacy.load("pt_core_news_lg")
        
    def _carregar_banco_nomes_offline(self):
        """
        Método responsável por carregar e retornar um banco de nomes do IBGE, retirado do repositório
        https://github.com/datasets-br/prenomes/blob/master/data/nomes-censos-ibge.csv
        
        
        """
        ARQUIVO_CSV_NOMES = "data/nomesIBGE.csv" 
        NOME_COLUNA_CSV = "Nome" 
        
        print(f"Carregando banco offline de '{ARQUIVO_CSV_NOMES}'...")
        try:
            df = pd.read_csv(ARQUIVO_CSV_NOMES, encoding='utf-8')
            
            if NOME_COLUNA_CSV not in df.columns:
                print(f"ERRO: Coluna '{NOME_COLUNA_CSV}' não encontrada. Colunas: {df.columns.tolist()}")
                sys.exit()

            #Converte os valores da coluna para string, aplica uma função de limpeza customizada
            # e padroniza o texto em letras maiúsculas.
            lista_nomes = df[NOME_COLUNA_CSV].astype(str).apply(lambda x: ms.limpar_texto(x).upper())
            banco_set = set(lista_nomes)
            
            return banco_set
            
        except FileNotFoundError:
            print(f"ERRO: Arquivo '{ARQUIVO_CSV_NOMES}' não encontrado.")
            sys.exit()
            
    def _carregar_entrada(self, nome_arquivo):
        """
        Método responável por carregar e retornar a entrada em formato de dataframe.
        
        
        """
        try:
            df = pd.read_excel(f'data/{nome_arquivo}.xlsx', engine='openpyxl')
            return df
        except:
            print("Erro ao abrir Excel.")
            sys.exit()
            return