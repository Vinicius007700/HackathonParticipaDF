import pandas as pd
import assets.manipulate_str as ms
import re


def remover_numeros_processuais(texto):
    """
    Função responsável por remover numeros processuais, como CNJ, SEI e administrativo, para 
    higienização do texto para a análise do spacy
    
    :param texto: a nossa linha de entrada
    """
    if pd.isna(texto): return texto
    texto = str(texto)
    
    
    # CNJ: 7 digitos + traço + 2 digitos + ponto + ano + ponto
    padrao_cnj = r'\b\d{1,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b'
    
   
    # SEI = 00000.000000/2024-99 ou sequências longas específicas
    padrao_sei_completo = r'\b\d{3,6}\.\d{3,8}\/\d{4}-\d{2}\b'
    
    
    padrao_administrativo_simples = r'\b\d{5,15}\/\d{4}\b'
    
    padrao_adm_com_dv = r'\b\d{5,15}\/\d{4}-\d{1,2}\b'
    
    texto = re.sub(padrao_cnj, " [PROCESSO_CNJ] ", texto)
    texto = re.sub(padrao_sei_completo, " [PROCESSO_SEI] ", texto)
    texto = re.sub(padrao_adm_com_dv, " [PROCESSO_ADM] ", texto)
    texto = re.sub(padrao_administrativo_simples, " [PROCESSO_ADM] ", texto)
    
    return texto

def detecta_dados_sensiveis(texto, data):
    """
    Função responsável por identificar os dados sensíveis e retornar quais são.
    Retorna (bool, list)
    
    :param texto: o texto que estamos analisando
    :param data: A classe das bibliotecas que carregamos
    """
    texto_para_regex = remover_numeros_processuais(texto)
    
    cpf = detecta_cpf(texto_para_regex)
    
    email = detecta_email(texto_para_regex) 
    
    tel = detecta_telefone(texto_para_regex) 
    
    rg = detecta_rg(texto_para_regex)
    
    cnh = detecta_cnh(texto_para_regex)
    
    encontrados = cpf + email + tel + rg + cnh
    if(len(encontrados) > 0):
        return True, " | ".join(encontrados)
    
    nomes = detecta_nomes(texto_para_regex, data)
    
    
    encontrados += nomes
    
    if len(encontrados) > 0:
        return True, " | ".join(encontrados)
    return False, ""


def detecta_cpf(texto):
    """
    Função responsável por detectar possíveis cpf
    
    :param texto: texto suspeito 
    """
    model_cpf = r'(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)'
    return re.findall(model_cpf, texto)

def detecta_email(texto):
    """
    Função responsável por detectar possíveis email
    
    :param texto: texto suspeito 
    """
    model_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(model_email, texto)

def detecta_telefone(texto):
    """
    Função responsável por detectar possíveis telefones
    
    :param texto: texto suspeito 
    """
    model_tel = r'(?:\(?\d{2}\)?\s?)(?:9\s?\d{4}|\d{4})[- ]?\d{4}'
    return re.findall(model_tel, texto)

def detecta_rg(texto):
    """
    Função responsável por detectar possíveis rg
    
    :param texto: texto suspeito 
    """
    model_rg = r'(?i)\brg\s*[:.]?\s*\d{1,2}\.?\d{3}\.?\d{3}-?\w{0,1}\b'
    return re.findall(model_rg, texto)

def detecta_cnh(texto):
    """
    Função responsável por detectar possíveis CNHs
    
    :param texto: texto suspeito 
    """
    model_cnh = r'(?i)cnh\s*[:.]?\s*\d{5,11}'
    return re.findall(model_cnh, texto)


def detecta_nomes(texto, data):
    """
    Função responsável por detectar possíveis nomes e retorna um conjunto de nomes que são
    
    :param texto: texto suspeito 
    :param data: A classe das bibliotecas que carregamos
    """
    if pd.isna(texto): return [] # Retorna lista vazia para somar depois
    texto = str(texto)
    
    doc = data.nlp(texto)
    encontrados = []

    for ent in doc.ents:
        if ent.label_ == "PER": # se o spacy identificou a palavra com a classe pessoa, vamos verificar
            nome_limpo, _ = ms.limpeza_do_nome(ent, data) 
            if ms.aplicar_filtros_basicos(nome_limpo): # se passou dos nossos filtro simples
                if ms.validar_com_ibge_offline(nome_limpo, data): # verificamos se há na base de dados do IBGE
                    encontrados.append(nome_limpo)
                elif(nome_limpo):# se não está na base de dados do IBGE e ainda temos alguma palavra depois de aplicarmos os filtros
                                # vamos analisar a palavra
                    if(not ms.e_palavra_de_dicionario(nome_limpo, data)): # se a palavra não é de dicionário, 
                        encontrados.append(nome_limpo)                  # vamos considerar nome na dúvida.
                        
    
    return list(set(encontrados))