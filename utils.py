# -*- coding: utf-8 -*-

import os
import datetime as dt
import platform

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path

from matplotlib.dates import num2date
from scipy.io import readsav

# Caminho para todos os arquivos salvos.
CAMINHO_ABSOLUTO = Path(os.path.dirname(
    os.path.abspath(__file__)) + "/dados_7GHz/")


def calculo_de_indice(df, ponto_escolhido):
    """Retorna os dados do dataframe de um certo instante, dado o horário.
    O index do dataframe deve ser um horário.

    Parameters
    ----------
    df: dataframe
        Dataframe com os dados.
    ponto_escolhido: datetime
        O horário de que se quer pegar os dados.

    Returns
    -------
    n: pandas.Series
        Os dados do exato momento.
    n1: int
        O indice do momento.

    """

    dado = df.iloc[np.argmin(
        np.abs(df.index.to_pydatetime() - ponto_escolhido))]
    # O tempo é usado como posição, pois se trata do eixo x.
    indice = np.argmin(np.abs(df.index.to_pydatetime() - ponto_escolhido))
    return dado, indice


# posicao comeca vazio e vai acrescentando
# o clique conforme o grafico e clicado.
posicao = []


def onclick(event):
    """Pega a posição clicada em um gráfico.

    Parameters
    ----------
    event: matplotlib.backend_bases.Event
        Evento de clique no canvas.

    """

    print(event)
    # Anexa os dados do clique na list posição.
    posicao.append([event.xdata, event.ydata])
    # Imprime uma linha no local clicado.
    plt.plot([posicao[-1][0], posicao[-1][0]], [-20, 100])


def load_dados(dia, mes, ano):
    """Carrega os dados do 7 giga em um dataframe.

    Parameters
    ----------
    dia: str
        Dia do evento.
    mes: str
        Mes do evento.
    ano: str
        Ano do evento.

    Returns
    -------
    df: Dataframe
        Os dados lidos do arquivo sav.
    time: datetime:
        Os horários registrados no dataframe.
    diretorio: str
        O diretório em que os dados serão salvos.

    """

    path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath("Savef")
    path = path.joinpath(str(ano))

    filename = mes + dia + ano[2:]
    files = os.listdir(path)
    for file in files:
        if filename in file:
            filename = file

    dados = readsav(path.joinpath(filename))

    # Formata a data no formato aaaa-dd-mm.
    data = dt.date(int(ano), int(mes), int(dia))

    # O nome do diretorio segue o formato aaaa-mm-dd. Essa linha cria
    # o nome nesse formato.
    diretorio = str(data)

    # Confere se o diretório já existe.
    if CAMINHO_ABSOLUTO.joinpath(diretorio).exists():
        print("O diretorio já existe")
    else:
        CAMINHO_ABSOLUTO.joinpath(diretorio).mkdir()

    # .toordinal formata no formato gregoriano.
    data_gregoriano = data.toordinal()

    time = num2date(data_gregoriano + dados.time / 3600. / 24.,
                    tz=dt.timezone.utc)

    # Dados transpostos.
    transposed_data = np.transpose([
        dados.fr.clip(-1000, 1000),
        dados.fl.clip(-1000, 1000)])

    df = pd.DataFrame(transposed_data, index=time, columns=['R', 'L'])

    return df, time, diretorio


def remove_background(df, rstn=False):
    """Faz um calculo da media de todos os itens dentro de um dataframe,
    criando uma coluna com os dados ja com a media, chamada
    "nome_da_coluna_original" mais "_nomalizado", ja que usamos essa funcao
    para normalizar os graficos.


    Parameters
    ----------
    df: DataFrame
        Dataframe com os dados.
    rstn: bool, optional
        Define se está fazendo esse calculos para os dados do rstn

    Returns
    -------
    list
        Os indícies e as médias.

    Example
    -------
        Calcular a media de um grafico a partir de dois pontos selecionados
        de um grafico.

    """

    # Ponto antes e depois do evento, e dois pontos antes para a media.(LFA)

    # Usados para selecionar uma parte especifica do grafico.
    posicao_grafico1 = num2date(posicao[-4][0])
    posicao_grafico2 = num2date(posicao[-3][0])

    # Usados para calcular a média entre os pontos selecionados.
    tempo_background_inicio = num2date(posicao[-1][0])
    tempo_background_fim = num2date(posicao[-2][0])

    indice_do_tempo_background_inicio = calculo_de_indice(
        df, tempo_background_inicio)
    indice_do_tempo_background_fim = calculo_de_indice(
        df, tempo_background_fim)

    # Calcula os indices dos gráficos 1 e 2.
    indice_inicio_evento, tempo1_flare = calculo_de_indice(
        df, posicao_grafico1)
    indice_fim_evento, tempo2_flare = calculo_de_indice(
        df, posicao_grafico2)

    # Inicializa um dicionario que vai guardar os dados,
    # normais e normalizados.
    todas_medias = {'L': 0, 'R': 0}
    # Esse for passa por cada coluna do dataframe e calcula a media de seus
    # respectivos dados.
    for column in df.columns:
        # Pega todos os pontos entre os pontos selecionados.
        media = np.array(df[column][indice_do_tempo_background_fim[1]:
                                    indice_do_tempo_background_inicio[1]])

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

    dict_dados_finais = {
        "indice_inicio_evento": indice_inicio_evento,
        "indice_fim_evento": indice_fim_evento,
        "medias": todas_medias,
        "inicio_flare": tempo1_flare,
        "fim_flare": tempo2_flare,
    }

    return dict_dados_finais


def ponto_mais_proximo(lista, numero):
    """Essa funcao pega o número mais próximo, de um certo número dentro
    de uma lista.
    """
    return min(lista, key=lambda n: abs(n - numero))


def get_datetime(time):
    """Sets a GOES formatted date(string) to a datetime object.

    Arguments:
        time {str} -- GOES formatted date.

    Returns:
        {datetime} -- The date formatted in datetime.
    """
    year = int(time[0:4])
    month = int(time[5:7])
    day = int(time[8:10])
    hour = int(time[11:13])
    minute = int(time[14:16])
    second = int(time[17:19])
    return dt.datetime(year, month, day, hour, minute, second)


def get_correct_goes_index(goes_index, begin, end):
    """Get begin and end indexes set from a timerange.

    Arguments:
        goes_index {pandas.Index} -- GOES dataframe's index.
        begin {str} -- GOES formatted date of the begging point.
        end {str} -- GOES formatted date of the ending point.

    Returns:
        begin, end {str} -- begin and and indexes from the dataframe.
    """
    difference = dt.timedelta(seconds=1)
    begin = get_datetime(begin)
    end = get_datetime(end)
    found_begin = False
    found_end = False

    for index in goes_index:
        new_index = get_datetime(str(index)[0:19])

        if ((new_index == begin or new_index == begin-difference or
                new_index == begin-2*difference) and not found_begin):
            found_begin = True
            begin = index
            continue

        if ((new_index == end or new_index == end+difference or
                new_index == end+2*difference) and not found_end):
            found_end = True
            end = index
            continue

    return begin, end
