# -*- coding: utf-8 -*-

import os
import datetime as dt
import platform

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.dates import num2date
from scipy.io import readsav

# Caminho para todos os arquivos salvos.
if platform.system() == "Linux":
    CAMINHO_ABSOLUTO = os.path.dirname(
        os.path.abspath(__file__)) + "/dados_7GHz/"
else:
    CAMINHO_ABSOLUTO = os.path.dirname(
        os.path.abspath(__file__)) + "\\dados_7GHz\\"


def calculo_de_indice(df, ponto_escolhido):
    """Retorna os dados do dataframe de um certo instante, dado o horário.
    O index do dataframe deve ser um horário.

    Arguments:
        df {dataframe} -- Dataframe com os dados.
        ponto_escolhido {datetime} -- O horário de que se quer pegar os dados.

    Returns:
        n {pandas.Series} -- Os dados do exato momento.
        n1 {int} -- O indice do momento.
    """

    n = df.iloc[np.argmin(np.abs(df.index.to_pydatetime() - ponto_escolhido))]
    # O tempo é usado como posição, pois se trata do eixo x.
    n1 = np.argmin(np.abs(df.index.to_pydatetime() - ponto_escolhido))
    return n, n1


# posicao comeca vazio e vai acrescentando
# o clique conforme o grafico e clicado.
posicao = []


def onclick(event):
    """Pega a posição clicada em um gráfico.

    Arguments:
        event {[type]} -- [description]
    """

    # Anexa os dados do clique na list posição.
    posicao.append([event.xdata, event.ydata])
    # Imprime uma linha no local clicado.
    plt.plot([posicao[-1][0], posicao[-1][0]], [-20, 100])


def mes_upper(mes):
    """Dado um mes (número), retorna o mes no formato dos arquivos do
    RSTN com as letras maiúsculas.

    Arguments:
        mes {int or str} -- O número do mês.

    Returns:
        {str} -- O mês no formato dos arquivos do RSTN.
    """

    months = [
        "JAN", "FEV", "MAR", "APR", "MAY", "JUN",
        "JUL", "AUG", "SEP", "OUT", "NOV", "DEC"
    ]

    # Returns the corresponding month to dowload the file.
    index = int(mes) - 1
    return months[index]


def mes_lower(mes):
    """Dado um mes (número), retorna o mes no formato dos arquivos do
    RSTN com as letras minúsculas.

    Arguments:
        mes {int or str} -- O número do mês.

    Returns:
        {str} -- O mês no formato dos arquivos do RSTN.
    """

    months = [
        "jan", "fev", "mar", "apr", "may", "jun",
        "jul", "aug", "sep", "out", "nov", "dec"
    ]

    # Returns the corresponding month to dowload the file.
    index = int(mes) - 1
    return months[index]


def arquivo_existe(caminho, mes):
    """Confirma se o arquivo do RSTN existe.

    Arguments:
        caminho {str} -- O caminho para o arquivo.
        mes {str} -- O mês do arquivo.

    Returns:
        {bool} -- True se o arquivo existe.
    """


    lista_de_arquivos = os.listdir(caminho)

    for arquivo in lista_de_arquivos:
        if mes in arquivo:
            return True

    return False


def caminho_rstn(ano, mes, dia):
    """Retorna o caminho para o arquivo do RSTN.

    Arguments:
        ano {str or int} -- Ano do arquivo.
        mes {str or int} -- Mês do arquivo.
        dia {str or int} -- Dia do arquivo.

    Returns:
        {str} -- O caminho relativo para os arquivos.
    """


    if platform.system() == "Linux":
        caminho = "dados_rstn/" + str(ano) + "/0" + str(mes) + "/"
    else:
        caminho = "dados_rstn\\" + str(ano) + "\\0" + str(mes) + "\\"
    # upper.
    if dia < 10:
        dia = "0" + str(dia)
    else:
        dia = str(dia)

    arquivo = dia + mes_lower(mes) + str(ano)[2:] + ".k7o"

    if arquivo_existe(caminho, mes_lower(mes)):
        print(arquivo)
        return caminho + arquivo
    else:
        # lower.
        arquivo = dia + mes_upper(mes) + str(ano)[2:] + ".K7O"
        print(arquivo)
        return caminho + arquivo


def load_dados(dia, mes, ano):
    """Carrega os dados do 7 giga em um dataframe.

    Arguments:
        dia {str} -- Dia do evento.
        mes {str} -- Mes do evento.
        ano {str} -- Ano do evento.

    Returns:
        df {Dataframe} -- Os dados lidos do arquivo sav.
        time {datetime} -- Os horários registrados no dataframe.
        diretorio {str} -- O diretório em que os dados serão salvos.
    """

    if platform.system() == "Linux":
        path = os.path.dirname(os.path.abspath(__file__)) + \
            "/Savef/" + str(ano) + "/"
    else:
        path = os.path.dirname(os.path.abspath(__file__)) + \
            "\\Savef\\" + str(ano) + "\\"

    filename = mes + dia + ano[2:]
    files = os.listdir(path)
    for file in files:
        if filename in file:
            filename = file

    dados = readsav(path + filename)
    data = dt.date(int(ano), int(mes), int(dia))

    # O nome do diretorio segue o formato aaaa-mm-dd. Essa linha cria
    # o nome nesse formato.
    diretorio = str(data)

    # Confere se o diretório já existe.
    if os.path.exists(CAMINHO_ABSOLUTO + diretorio):
        print("O diretorio já existe")
    else:
        # Cria o diretorio.
        os.mkdir(CAMINHO_ABSOLUTO + diretorio)

    # dt.date(ano, dia, mes) Formata a data no formato aaaa-dd-mm.
    # .toordinal formata no formato gregoriano.
    data_gregoriano = data.toordinal()

    time = num2date(data_gregoriano + dados.time / 3600. / 24.)

    # Dados transpostos.
    transposed_data = np.transpose([
        dados.fr.clip(-1000, 1000),
        dados.fl.clip(-1000, 1000)])

    df = pd.DataFrame(transposed_data, index=time, columns=['R', 'L'])

    return df, time, diretorio


def calculo_da_media(df, rstn=False):
    """Faz um calculo da media de todos os itens dentro de um dataframe,
    criando uma coluna com os dados ja com a media, chamada
    "nome_da_coluna_original" mais "_nomalizado", ja que usamos essa funcao
    para normalizar os graficos.

    Exemplo de uso:
        Calcular a media de um grafico a partir de dois pontos selecionados de
        um grafico.

    Arguments:
        df {DataFrame} -- Dataframe com os dados.

    Keyword Arguments:
        rstn {bool} -- Define se está fazendo esse calculos para os dados do
                        rstn (default: {False})

    Returns:
        {list} -- Contém os indícies e as médias.
    """

    # Ponto antes e depois do evento, e dois pontos antes para a media.(LFA)

    # Usados para selecionar uma parte especifica do grafico.
    posicao_grafico1 = num2date(posicao[-4][0])
    posicao_grafico2 = num2date(posicao[-3][0])

    # Usados para calcular a média entre os pontos selecionados.
    tempo1 = num2date(posicao[-1][0])
    tempo2 = num2date(posicao[-2][0])

    indice_de_y1 = calculo_de_indice(df, tempo1)
    indice_de_y2 = calculo_de_indice(df, tempo2)

    # Calcula os indices dos gráficos 1 e 2.
    indice_grafico1, tempo1_flare = calculo_de_indice(df, posicao_grafico1)
    indice_grafico2, tempo2_flare = calculo_de_indice(df, posicao_grafico2)

    # Inicializa um dicionario que vai guardar os dados,
    # normais e normalizados.
    todas_medias = {'L': 0, 'R': 0}
    # Esse for passa por cada coluna do dataframe e calcula a media de seus
    # respectivos dados.
    for column in df.columns:
        # Pega todos os pontos entre os pontos selecionados em t1 e t2.
        media = np.array(df[column][indice_de_y2[1]:indice_de_y1[1]])

        # Medias calculadas.
        media_final = np.median(media)

        # Se for a ultima vez chamando essa função, serão criadas duas colunas
        # no dataframe. As quais vão ser todos os valores menos as medias
        # R e L, criando assim R e L normalizados.

        coluna = column + "_normalizado"
        df[coluna] = df[column] - media_final
        todas_medias[column] = media_final

    if rstn is True:
        return todas_medias

    dados_finais = [
        indice_grafico1, indice_grafico2, todas_medias,
        tempo1_flare, tempo2_flare
    ]
    return dados_finais


def ponto_mais_proximo(lista, numero):
    """
    Essa funcao pega o número mais próximo, de um certo número dentro
    de uma lista.
    """
    return min(lista, key=lambda n: abs(n - (numero)))
