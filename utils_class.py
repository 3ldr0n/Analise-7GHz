# -*- coding: utf-8 -*-

import os
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.dates import num2date
from scipy.io import readsav

class Utils(object):
    """Funcoes uteis nas analises.

    Args:
        filename (str):  Nome do arquivo.

    Attrubutes:
        filename (str):  Nome do arquivo.
        CAMINHO_ABSOLUTO (str):  Caminho usado para salvar as images,
            e procurar arquivos.
        df (DataFrame): aa.
        diretorio (str): aa.
    """
    posicao = []

    def __init__(self, filename):
        self.filename = filename
        # Caminho para todos os arquivos salvos.
        self.CAMINHO_ABSOLUTO = str(os.getcwd()) + "\Analise 7 GHz\\"


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
    def get_diretorio(self):
    def get_time(self):
        return self.time


    @property
    def get_diretorio(self):
    def get_caminho_absoluto(self):
        return self.CAMINHO_ABSOLUTO


    def calculo_de_indice(self, ponto_escolhido):
        # TODO
        # Documentar essa função.
        n = self.df.iloc[np.argmin(np.abs(self.df.index.to_pydatetime() - ponto_escolhido))]
        n1 = np.argmin(np.abs(self.df.index.to_pydatetime() - ponto_escolhido))
        return n, n1


    @classmethod
    def onclick(cls, event):
        # Anexa os dados do clique na list posicao.
        posicao.append([event.xdata,event.ydata])
        # Imprime uma linha no local clicado.
        plt.plot([cls.posicao[-1][0], cls.posicao[-1][0]], [-150,150])


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
        path = 'C:/Users/Andre/Desktop/Lucas/Savef/' + str(ano) + '/'
        dados = readsav(path + self.filename)

        data = dia_mes_ano_filename(filename)

        # O nome do diretório segue o formato aaaa-mm-dd. Essa linha cria
        # o nome nesse formato.
        diretorio = str(dt.date(data['ano'], data['mes'], data['dia']))

        # Confere se o diretorio já existe.
        if os.path.exists(self.CAMINHO_ABSOLUTO + diretorio):
            print("O diretorio já existe.")
        else:
            # Cria o diretório.
            os.mkdir(CAMINHO_ABSOLUTO + diretorio)

        # dt.date(ano, dia, mes) Formata a data no formato aaaa-dd-mm.
        # .toordinal formata no formato gregoriano.
        data_gregoriano = dt.date(data['ano'], data['mes'], data['dia']).toordinal()

        time = num2date(data_gregoriano + dados.time/3600./24.)

        # Dados transpostos.
        transposed_data = np.transpose([
            dados.fr.clip(-1000, 1000),
            dados.fl.clip(-1000, 1000)])

        df = pd.DataFrame(transposed_data, index=time, columns=['R','L'])

        self.df = df
        self.time = time
        self.diretorio = diretorio


    def calculo_da_media(self, final=False):
        """
        Essa função calcula a media entre dois pontos selecionados,
        tanto no R quanto no L. E calcula o tamanho do gráfico para se
        plotar as médias.
        """
        # Ponto antes e depois do evento, e dois pontos antes para a média.(LFA)

        # Usados para selecionar uma parte específica do gráfico.
        posicao_grafico1 = num2date(posicao[-4][0])
        posicao_grafico2 = num2date(posicao[-3][0])

        # Usados para calcular a média entre os pontos selecionados.
        tempo1 = num2date(posicao[-1][0])
        tempo2 = num2date(posicao[-2][0])

        indice_de_y1 = calculo_de_indice(self.df, tempo1)
        indice_de_y2 = calculo_de_indice(self.df, tempo2)

        # Calcula os indices dos gráficos 1 e 2.
        indice_ig1, tempo1_flare = calculo_de_indice(self.df, posicao_grafico1)
        indice_ig2, tempo2_flare = calculo_de_indice(self.df, posicao_grafico2)

        # Pega todos os pontos entre os pontos selecionados em t1 e t2.
        media_r = np.array(self.df["R"][indice_de_y2[1]:indice_de_y1[1]])
        media_l = np.array(self.df["L"][indice_de_y2[1]:indice_de_y1[1]])

        # Médias calculadas.
        media_final_r = np.median(media_r)
        media_final_l = np.median(media_l)

        if final:
            # Se for a ultima vez chamando essa função, será criado duas colunas
            # no dataframe. As quais vão ser todos os valores menos as medias R e L,
            # criando assim R e L normalizados.
            self.df["R_normalizado"] = self.df["R"] - media_final_r
            self.df["L_normalizado"] = self.df["L"] - media_final_l

            return indice_ig1, indice_ig2, media_final_r, media_final_l, tempo1_flare, tempo2_flare

        else:
            return indice_ig1, indice_ig2, media_final_r, media_final_l, tempo1_flare, tempo2_flare


    def ponto_mais_proximo(self, lista, numero):
        """
        Essa função pega o número mais próximo, de um certo número dentro
        de uma lista.
        """
        return min(lista, key=lambda n: abs(n - (numero)))
