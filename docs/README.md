# Documentação

## Análise

### 01ª célula

Imports de bibliotecas/arquivos internos e externos.

### 02ª célula

Seleciona o dia para ser analisado, e carrega os dados desse dia.

### 03ª célula

Carrega o gráfico

Ordem de seleção do gráfico:

- A primeira coisa que deve ser selecionada são os pontos para selecionar a área do gráfico que será salva.
- A segunda coisa são os pontos para remover o background.

### 04ª célula

Faz todos os cálculos necessário.

### 05ª célula

Faz o plot do evento (R e L separados) depois de ter tirado as médias.

### 06ª célula

Faz o plot do evento (R e L juntos), do I e do V.

### 07ª célula

Baixa o arquivo do RSTN do dia, e cria um dataframe.

### 08ª célula

Apaga os dados das frequências que não serão utilizadas.

### 09ª célula

Gera o gráfico do RSTN, para remover o background.

### 10ª célula

Faz o plot dos dados depois da remoção do background.

### 11ª célula

Pega o ponto no RSTN que é o pico no 7GHz.

### 12ª célula

"Monta" o espectro rádio.

### 13ª célula

Cria um objeto do tipo TimeRange do comeco ao fim do evento, para pegar os dados do goes nesse período.

### 14ª célula

Faz o plot dos dados do GOES.

### 15ª célula

Faz o plot dos dados do GOES (pelo sunpy), e salva a imagem.

### 16ª célula

Lê o arquivo do report do noaa e procura por regiões ativas no timerange.

### 17ª célula

"Seta" a o código da região ativa, ou None(string).

### 18ª célula

Gera o gráfico do evento para selecionar o ponto de início do evento.

### 19ª célula

Faz os cálculos dos pontos e pega o horário exato do pico.

### 20ª célula

Faz os cálculos do I e V.

### 21ª célula

Calcula o grau de polarização;.

### 22ª célula

Gera o gráfico final do evento em 7GHz, do evento pelo GOES e o espectro. E salva a imagem.

### 23ª célula

Salva todos os dados no arquivo dados_finais/dados.csv
