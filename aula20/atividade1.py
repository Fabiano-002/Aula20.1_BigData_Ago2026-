import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

try:
    print('Obtendo Dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # Correção: 'estelionato' ao invés de 'esteolinato'
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    
    df_estelionato = df_ocorrencias[['estelionato', 'mes_ano']]

    # Correção: 'groupby' ao invés de 'groupy'
    df_estelionato = df_estelionato.groupby('mes_ano', as_index=False)['estelionato'].sum()
    

    print("\n--- Estelionato por Mês ---")
    print(df_estelionato)

    
    
except Exception as e:
    print (f'Erro ao obter os dados - {e}')

try:


    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)

    distancia =abs(
        (media_estelionato - mediana_estelionato) / mediana_estelionato * 100

    )

    print(f'\nMedida de Tendência Central')
    print(f'\nMédia :{media_estelionato:.2f}')
    print(f'\nMediana; {(mediana_estelionato)}')
    print(f'Distância Média - Mediana:{distancia:.2f}%')

except Exception as e:
    print(f'Obtendo medidas - {e}')

try:
    q1 = np.quantile(array_estelionato, .25)
    q2 = np.quantile(array_estelionato, .50)
    q3 = np.quantile(array_estelionato, .75)

    # print('\nMedidas de Posição')
    # print(f'Q1: {q1}')
    # print(f'Q2: {q2}')
    # print(f'Q3: {q3}')


    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1 ]
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]



    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_estelionato_menores.sort_values(by='estelionato', ascending=True))
    df_estelionato_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1' )


    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_estelionato_maiores.sort_values(by='estelionato', ascending=True))
    df_estelionato_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1' )
    

except Exception as e:
    print(f'Erro ao analisar as distribuição {e}') 


try:
    print('\nCalculando a Amplitude Total')
    
    maximo = np.max(array_estelionato)
    minimo = np.min(array_estelionato)
    amplitude = maximo - minimo

except Exception as e:    
    print(f'Erro ao calcular a apmlitude {e}')


try:
    #Intervalo Interquartil:    
    # É amplitude dos dados mais centrais
    iqr = q3 - q1

    # Calculando os limites
    # Superior

    limite_superior = q3 + (1.5 * iqr)

    # Inferior 
    limite_inferior = q1 - (1.5 *iqr)

    print(f'limite_Superior: {limite_superior}')
    print(f'limite_Inferior: {limite_inferior}')


    # Filtrando os Outliers menores
    
    df_estelionato_outliers_menores = (
        df_estelionato[df_estelionato['estelionato']< limite_inferior]
    )

    print('\nEstelionato com outliers inferiores')
    print(30*'-')
    if len(df_estelionato_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_estelionato_outliers_menores)    

    df_estelionato_outliers_maiores = (
        df_estelionato[df_estelionato['estelionato'] > limite_superior]
    
    )  

    print('\nEstelionato com outliers Superiores')
    print(30*'-')
    if len(df_estelionato_outliers_menores) == 0:
             print('Não há outliers Superiores')
    else:
        print(df_estelionato_outliers_maiores) 


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

    print(f'Média: {media_estelionato:.2f}')
    print(f'Mediana: {mediana_estelionato}')
    print(f'Distância: {distancia:.2f}%')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')

except Exception as e:
    print(f'\nErro aos mostrar medidas {e}')

try:    
    print('\nInformações sobre Estelionato')
    plt.figure(figsize={16,10})
    # Posição 1 Boxplot

    plt.subplot(1, 2, 1)

    plt.boxplot(df_estelionato['estelionato'], orientation='horizontal',showmeans=True)
    plt.title('Distribuição dos Dados')
    plt.xlabel('Estelionato')
    plt.ylabel('Municípios')

    plt.subplot(1, 2, 2)
    plt.text(0.1, 0.95 , f'Limite Inferior: {limite_inferior}', fontsize=12 )
    plt.text(0.1, 0.90 , f'Mínimo: {minimo}',fontsize=12  )
    plt.text(0.1, 0.85 , f'Q1:{q1}' , fontsize=12 )
    plt.text(0.1, 0.80 , f'Q2:{q2}' , fontsize=12 )
    plt.text(0.1, 0.75 , f'Q3:{q3}' ,fontsize=12  )
    plt.text(0.1, 0.70 , f'Limite Superior: {limite_superior}',fontsize=12  )
    plt.text(0.1, 0.65 , f'Máximo: {maximo}', fontsize=12  )

    plt.text(0.1, 0.55, f'Mediana: {mediana_estelionato}', fontsize=12 )
    plt.text(0.1, 0.50, f'Média: {media_estelionato:.2f}',fontsize=12  )
    plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}',fontsize=12 )
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}',fontsize=12  )
    plt.text(0.1, 0.35, f'Distância Total: {distancia:.2f}%', fontsize=12 )
    plt.axis('off')

    plt.suptitle('Informações sobre Estelionato')

    plt.show()

except Exception as e:
    print (f'Erro ao plotar grafico: - {e}')       
