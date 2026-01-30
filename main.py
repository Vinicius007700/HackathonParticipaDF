import assets.LoadData as ld
import pandas as pd
import assets.private_data as pv
def main():
    data = ld.LoadData('amostra') # A nossa entrada esperada é do mesmo formato da entrada
                                # de exemplo que nos foi fornecida e adicione na pasta data

    coluna_texto = 'Texto Mascarado'  # o nome da coluna do arquivo de entrada. Troque se 
                                     # na entrada for outro
    if coluna_texto not in data.df.columns:
        print("Coluna não encontrada. Verifique o nome da coluna na entrada e se possível coloque como Texto Mascarado.")
        return
    
    # uma extração de dados da coluna do texto, transformando em um data frame
    resultado = data.df[coluna_texto].apply(lambda x: pd.Series(pv.detecta_dados_sensiveis(x, data )))
    data.df['Contendo Dados Pessoais'] = resultado[0]
    data.df['quais_dados'] = resultado[1]
    
    data.df.to_excel('gabarito.xlsx', index=False)
  

if __name__ == "__main__":
    main()