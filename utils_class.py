# -*- coding: utf-8 -*-

import os
import platform
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.dates import num2date
from scipy.io import readsav


class Utils:
    """Funções úteis nas analises.

    Args:
        filename (str):  Nome do arquivo.

    Attrubutes:
        filename (str):  Nome do arquivo.
        CAMINHO_ABSOLUTO (str):  Caminho usado para salvar as images,
            e procurar arquivos.
        df (DataFrame): Dataframe com os dados do dia.
        diretorio (str): diretório em que os dados serão alvos.
    """

    # posiçáo começa vazio e vai acrescentando o clique conforme
    # o gráfico e clicado.
    posicao = []

    def __init__(self, filename):
        self.filename = filename
        # Caminho para todos os arquivos salvos.
        if platform.system() == "Linux":
            self.CAMINHO_ABSOLUTO = os.path.dirname(
                    os.path.abspath(__file__)) + "/dados_7 GHz/"
        else:
            self.CAMINHO_ABSOLUTO = os.path.dirname(
                    os.path.abspath(__file__)) + "\\dados_7 GHz\\"

    @property
    def get_df(self):
        return self.df

    @property
    def get_filename(self):
        return self.filename

    @property
    def get_diretorio(self):
        return self.diretorio

    @property
    def get_time(self):
        return self.time

    @property
    def get_caminho_absoluto(self):
        return self.CAMINHO_ABSOLUTO

    def calculo_de_indice(self, ponto_escolhido):
        n = self.df.iloc[np.argmin(np.abs(
            self.df.index.to_pydatetime() - ponto_escolhido))]
        # Retorna o tempo no formato datetime.
        # O tempo e usado como posicao, pois se trata do eixo x.
        n1 = np.argmin(np.abs(self.df.index.to_pydatetime() - ponto_escolhido))
        return n, n1

    def onclick(self, event):
        # Anexa os dados do clique na list posicao.
        self.posicao.append([event.xdata, event.ydata])
        # Imprime uma linha no local clicado.
        plt.plot([self.posicao[-1][0], self.posicao[-1][0]], [-150, 150])

    def dia_mes_ano_filename(self, load_dados=True):
        # Adiciona 20 no inicio do ano, já que o ano está no formato AA.
        ano = int('20' + self.filename[4:6])
        dia = int(self.filename[0:2])
        mes = int(self.filename[2:4])

        # Coloca a data em um dicionário.
        data = {
            'ano': ano,
            'mes': mes,
            'dia': dia
        }

        if load_dados:
            return data

        return dia + mes + ano

    def load_dados(self, ano):
        if platform.system() == "Linux":
            path = os.path.dirname(os.path.abspath(__file__)) + \
                "/Savef/" + str(ano) + "/"
        else:
            path = os.path.dirname(os.path.abspath(__file__)) + \
                "\\Savef\\" + str(ano) + "\\"

        dados = readsav(path + self.filename)

        data = self.dia_mes_ano_filename(self.filename)

        # O nome do diretório segue o formato aaaa-mm-dd. Essa linha cria
        # o nome nesse formato.
        diretorio = str(dt.date(data['ano'], data['mes'], data['dia']))

        # Confere se o diretorio já existe.
        if os.path.exists(self.CAMINHO_ABSOLUTO + diretorio):
            print("O diretorio já existe.")
        else:
            # Cria o diretório.
            os.mkdir(self.CAMINHO_ABSOLUTO + diretorio)

        # dt.date(ano, dia, mes) Formata a data no formato aaaa-dd-mm.
        # .toordinal formata no formato gregoriano.
        data_gregoriano = dt.date(
                data['ano'], data['mes'], data['dia']).toordinal()

        time = num2date(data_gregoriano + dados.time/3600./24.)

        # Dados transpostos.
        transposed_data = np.transpose([
            dados.fr.clip(-1000, 1000),
            dados.fl.clip(-1000, 1000)])

        df = pd.DataFrame(transposed_data, index=time, columns=['R', 'L'])

        self.df = df
        self.time = time
        self.diretorio = diretorio

    def calculo_da_media(self, rstn=False):
        """
        Faz um calculo da media de todos os itens dentro de um dataframe,
        criando uma coluna com os dados ja com a media, chamada
        "nome_da_coluna_original" mais "_nomalizado", ja que usamos essa
        funcao para normalizar os graficos.
        Exemplo de uso:
            Calcular a media de um grafico a partir de dois pontos selecionados
            de um grafico.
        """
        # Ponto antes e depois do evento,
        # e dois pontos antes para a média.(LFA)

        # Usados para selecionar uma parte específica do gráfico.
        posicao_grafico1 = num2date(self.posicao[-4][0])
        posicao_grafico2 = num2date(self.posicao[-3][0])

        # Usados para calcular a média entre os pontos selecionados.
        tempo1 = num2date(self.posicao[-1][0])
        tempo2 = num2date(self.posicao[-2][0])

        indice_de_y1 = self.calculo_de_indice(self.df, tempo1)
        indice_de_y2 = self.calculo_de_indice(self.df, tempo2)

        # Calcula os indices dos gráficos 1 e 2.
        indice_grafico1, tempo1_flare = self.calculo_de_indice(
                self.df, posicao_grafico1)
        indice_grafico2, tempo2_flare = self.calculo_de_indice(
                self.df, posicao_grafico2)

        # Inicializa um dicionario que vai guardar os dados, normais
        # e normalizados.
        todas_medias = {'L': 0, 'R': 0}
        # Esse for passa por cada coluna do dataframe e calcula a media de seus
        # respectivos dados.
        for column in self.df.columns:
            # Pega todos os pontos entre os pontos selecionados em t1 e t2.
            media = np.array(self.df[column][indice_de_y2[1]:indice_de_y1[1]])

            # Medias calculadas.
            media_final = np.median(media)

            # Se for a ultima vez chamando essa função, será criado duas
            # colunas no dataframe. As quais vão ser todos os valores
            # menos as medias R e L, criando assim R e L normalizados.

            coluna = column + "_normalizado"
            self.df[coluna] = self.df[column] - media_final
            todas_medias[column] = media_final

            # Pega todos os pontos entre os pontos selecionados em t1 e t2.
            media_r = np.array(self.df["R"][indice_de_y2[1]:indice_de_y1[1]])
            media_l = np.array(self.df["L"][indice_de_y2[1]:indice_de_y1[1]])

            # Médias calculadas.
            media_final_r = np.median(media_r)
            media_final_l = np.median(media_l)

        if rstn is True:
            return todas_medias

        dados_finais = [
            indice_grafico1, indice_grafico2, todas_medias,
            tempo1_flare, tempo2_flare
        ]
        return dados_finais

    @staticmethod
    def ponto_mais_proximo(lista, numero):
        """
        Essa função pega o número mais próximo, de um certo número dentro
        de uma lista.
        """
        return min(lista, key=lambda n: abs(n - (numero)))
