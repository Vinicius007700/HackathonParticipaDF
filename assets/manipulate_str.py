import unicodedata
def limpeza_do_nome(ent, data):
    """
    Aplica as estratégias de blacklist e deixa a palavra sem acentos e em minúsculo.
    Retorna: (nome_final, eh_valido)
    """
    tokens_limpos = []
    
    # Verificamos se a entidade inteira é proibida
    texto_completo_lower = ent.text.lower()
    texto_completo_lower = limpar_texto(texto_completo_lower)
    for termo in texto_completo_lower.split():
        if termo in data.BLACKLIST_INVALIDADORA:
            return "", False # Retorna inválido

   
    for token in ent:
        txt_lower = limpar_texto(token.text) 
        
        if token.pos_ in ["PUNCT", "SYM", "NUM"]:
            continue
            
        # se o termo é algum verbo, adjetivo, etc ou está na lista de cote
        if token.pos_ in ["VERB", "AUX", "SCONJ", "ADV"] or txt_lower in data.BLACKLIST_CORTE:
            # Se já pegamos algum nome antes, paramos aqui
            if len(tokens_limpos) > 0:
                break
            # Se foi a primeira palavra, só ignora ela
            continue
            
        # se o termo é algum título. EX: sr, sra, etc
        if txt_lower in data.BLACKLIST_LIMPEZA:
            continue # Pula a palavra, mas continua lendo o resto
            
        # Se passou por tudo é um nome
        tokens_limpos.append(token.text)
    
    #retorna o nome de volta a uma string
    return " ".join(tokens_limpos).strip(), True

def limpar_texto(texto):
    """
    Função responsável por pegar uma string, tirar os acentos e deixar tudo minúsculo.
    
    :param texto: texto analisado
    """
    if not isinstance(texto, str): return ""
    texto_normalizado = unicodedata.normalize('NFD', texto)
    sem_acentos = texto_normalizado.encode('ascii', 'ignore').decode('utf-8')
    return sem_acentos.lower()


def aplicar_filtros_basicos(texto):
    """
    checagem se há algum número no nome
    """
    if any(char.isdigit() for char in texto): return False
    return True

def e_palavra_de_dicionario(texto, data):
    """
    Verifica se a palavra é comum usando o vocabulário do SpaCy.
    Retorna True se for palavra comum (ex: Nitrogênio, Mesa).
    Retorna False se for desconhecida (ex: Jacksoswaldo).
    """
    if not texto: return False
    
    # Pega a primeira palavra, minúscula
    palavra = texto.split()[0].lower()
    
   
    #se a palavra está no dicionario 
    eh_desconhecida = data.nlp.vocab[palavra].is_oov
    
    #se a palavra é desconhecida e não está na lista do IBGE de nomes, pode ser um nome fictício
    if eh_desconhecida:
        return False #
    else:
        return True # É de dicionário 
    

def validar_com_ibge_offline(nome_completo, data):
    """
    Retorna verdadeiro se um nome está na lista do IBGE e falso se não.
    
    :param nome_completo: o nome da pessoa
    :param banco_nomes_set: o conjunto do banco de nomes do IBGE
    """
    if not nome_completo: return False
    
    lista_nomes = []
    for nome in nome_completo.split():
        lista_nomes.append(limpar_texto(nome).upper())
    
    for elemento in lista_nomes:
        if elemento in data.banco_ibge:
            return True
        
    return False


