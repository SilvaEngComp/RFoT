# Informacoes sobre arquivos e execução de experimentos

Pasta de trabalho:
/home/<user of system >/mininet_blockchain_ml

## Iniciar experimentos:
> sudo python2 sim.py

## Descricao dos arquivos:

### data_hosts.json
- Arquivo com informações no formato json dos hosts que irão compor a rede
### associantion_hosts.json
- Arquivo com informações sobre associações entre sensores e gateways, i.e, define o gateway que cada sensor irá se comunicar
### config.json
- Configs sobre os sensores/dispositivos virtuais, modificações no arquivo serão espelhadas
para todos os sensores do experimento.
- Informações como: ip do broker e dados do protocolo TATU (publish, collect).

> OBS: Porta do broker está hardcoding como 1883 (arquivos sim.py e call_main.py)
### main.py; sensors.py tatu.py
- Arquivos que criam os sensores/disp virtuais e implementam a lógica e interpretaçao do 
protocolo TATU
### utils_hosts.py
- Funções úteis para manipular informações que estão armazenadas no arquivo data_hosts.json
- Utilizado principalmente para criar o experimento e indicar informações dos hosts
### create_topo.py
- Cria os links, switches e constrói a topologia
- Basea-se nos dados obtidos em data_hosts.json
### sim.py
- Arquivo gerador do experimento
- Criação dos sensores virtuais: Função init_sensors, nela são ajustados qual tipo de sensor criado e o fluxo de comunicação e iniciado
- Criação do Flow entre sensores e Broker: Função init_flow
> OBS: sensor "soilmoistureSensor" gerou erro no Storage.

## Sobre o service-mix e fuseki

 | user  | password |
 | -- | -- |
 | `karaf` | `wiser2014` |


## Abrir terminal do host no CLI
Pra abrir um terminal no host use a sintax: 
> <xterm> <hostname>
> exemplo: exterm h1

> obs: Nome do browser: midori​

# Bibliotecas requeridas para fucionamento da aplicação

- Abaixo segue a lista de pacotes necesssários para funcionamento da aplicação
- é recomendado o uso do anaconda, instando as ferramentas dentro de um ambiente virtual,
pois seu gerenciamento de pacotes tende a ser mais eficiente e prático do que o pip


## Mininet
> Para instalar o mininet siga o passo a passo no link abaixo:
http://mininet.org/download/

## Anaconda
- guia de instalação: https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-20-04-pt

## paho-mqtt
> sudo pip3 install paho-mqtt


## moquitto
> sudo apt-get install mosquitto
> sudo apt-get install mosquitto-clients

## tensorflow
- guia de instalação: 
> https://www.tensorflow.org/install/pip?hl=pt-br

## scikit-learn
> sudo pip install -U scikit-learn

## keras model reference
> https://faroit.com/keras-docs/1.2.2/models/about-keras-models/

## Important notations
- Publish pahoo mqtt
    - publish(topic, message, qos, retain)
- Keras
    - > (https://keras.io/api/losses/probabilistic_losses/#categorical_crossentropy-function)
    - > (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
    - > (https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score)
    - > (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.zero_one_loss.html#sklearn.metrics.zero_one_loss)