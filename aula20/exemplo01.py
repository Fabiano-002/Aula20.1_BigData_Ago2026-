import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


subprocess.run('cls', shell=True)
# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
   # utf-8, iso-8859-1, latin1, cp1252 

    # print(df_ocorrencias)
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.head(30))
    # print(df_roubo_veiculo.tail(30))

    # PREPARANDO OS DADOS

    # Totalizando os Roubos por Cidade (Var Qualitativa 'munic' e Var Quant 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    # print(df_roubo_veiculo)

    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False

    )
    print(df_roubo_veiculo.head(10))
    # print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

try:
    print(f'\nObtendo informações acerca dos roubos dos veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    #Distância da média para mediana 
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
        )

    print('\nMedida de Tendência Central')
    print(f'Média: {(media_roubo_veiculo)}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média - Mediana:{distancia:.2f}%')


    
except Exception as e:
    print(f'Obtendo medidas - {e}')

try:

    q1 = np.quantile(array_roubo_veiculo, .25) # method='weibull'
    q2 = np.quantile(array_roubo_veiculo, .50) # method='weibull'
    q3 = np.quantile(array_roubo_veiculo, .75) # method='weibull'

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades com menores ocorrências de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades com maiores ocorrências de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]
    # Menores
    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';',encoding='iso-8859-1' )

    #Maiores
    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=True))
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';',encoding='iso-8859-1')
    

except Exception as e:
    print(f'Erro ao analisar as distribuição {e}')

# Medidas de Posição e Dispersão  


try:
    print('\nCalculando a Amplitude Total')
    # Amplitude Total = maior valor - menor valor
    # Quanto mais próximo do 0, mais homogêneos são os dados do conjunto.
    # Quanto mais próximo do maior valor, mais heterogêneo são os dados do conjunto.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

except Exception as e:    
    print(f'Erro ao calcular a apmlitude {e}')


# Achando os Outliers

try:
    #Intervalo Interquartil:  (IQR)  
    # É amplitude dos dados mais centrais
    # Ignora o maior e menor valor 
    # Não sofre interferência dos extremos 
    # Quanto mais próximo do 0, mais homogêneos são os dados mais centrais
    # Quanto mais próximo do Q3, mais heterogêneo são os dadosdos 50% mais centrais
    # 970.75

    iqr = q3 - q1
    print(iqr)

    # Calculando os limites
    # Superior 
    limite_superior = q3 + (1.5 * iqr)
    
    # Inferior
    limite_inferior = q1 - (1.5 * iqr)

    print(f'\nlimite_Superior: {limite_superior}')
    print(f'\nlimite_Inferior:{limite_inferior}')

    # Filtrando os Outliers menores

    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']< limite_inferior]

    )

    print('\nMunicípios com outliers inferiores')
    print(30*'-')      
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há  outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)  

    # Filtrando os outliers maiores

    df_roubo_veiculo_outliers_maiores = (
            df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    
        )  
    print('\nMunicípios com outliers Superiores')
    print(30*'-')      
    if len(df_roubo_veiculo_outliers_maiores) == 0:
             print('Não há  outliers Superiores')
    else:
         print(df_roubo_veiculo_outliers_maiores)  

except Exception as e:
    print(f'Erro ao calcular os outliers {e}')   

try:
    print('\nMostrando Medidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior:{limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')

    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância: {distancia:.2f}%')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')

except Exception as e:
    print(f'\nErro aos mostrar medidas {e}')


# Plotando Gráfico

#try:
    #print('Plotando Boxplot')
    # pip install matplotlib
    # import matplotlib.pyplot as plt 

    # Boxplot
    #plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation= 'horizontal', showmeans= True)

    # plt.show()

# except Exception as e:
    # print (f'Erro ao plotar grafico: {e}')

try:
    print('\nInformações de Roubos de Veículos')
    plt.figure(figsize={16,10})
    # Posição 1 Boxplot

    plt.subplot(1, 2, 1)
    

    plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation='horizontal',showmeans=True)
    plt.title('Distribuição dos Dados')
    plt.xlabel('Roubo de Veículos')
    plt.ylabel('Municípios')

    plt.subplot(1, 2, 2)
    plt.text(0.1, 0.95 , f'Limite Inferior: {limite_inferior}', fontsize=12 )
    plt.text(0.1, 0.90 , f'Mínimo: {minimo}',fontsize=12  )
    plt.text(0.1, 0.85 , f'Q1:{q1}' , fontsize=12 )
    plt.text(0.1, 0.80 , f'Q2:{q2}' , fontsize=12 )
    plt.text(0.1, 0.75 , f'Q3:{q3}' ,fontsize=12  )
    plt.text(0.1, 0.70 , f'Limite Superior: {limite_superior}',fontsize=12  )
    plt.text(0.1, 0.65 , f'Máximo: {maximo}', fontsize=12  )

    plt.text(0.1, 0.55, f'Mediana: {mediana_roubo_veiculo}', fontsize=12 )
    plt.text(0.1, 0.50, f'Média: {media_roubo_veiculo}',fontsize=12  )
    plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}',fontsize=12 )
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}',fontsize=12  )
    plt.text(0.1, 0.35, f'Distância Total: {distancia}', fontsize=12 )
    plt.axis('off')

    plt.suptitle('Informações sobre Roubo de Veículos')


    plt.show

except Exception as e:
    print (f'Erro ao plotar grafico: - {e}')