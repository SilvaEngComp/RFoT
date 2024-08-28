#!/usr/bin/python

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import lg
import os
import create_topo
import network_init as ni

if __name__ == '__main__':
    lg.setLogLevel( 'info')
    if os.path.exists('devices_running.json') is True:
        os.remove('devices_running.json')
    
    net = Mininet(link=TCLink)
    #criar switches, hosts e topologia
    create_topo.create(net)
    # Configurar e iniciar comunicacao externa
    rootnode = ni.connectToInternet( net )
    ni.initGateways(net)
    #Iniciar sensores virtuais
    ni.initSensors(net)
    #Iniciar fluxo de comunicacao
    ni.initFlow(net)
    # ni.executeCenare1(net)
    CLI( net )
    
    # Shut down NAT
    ni.stopNAT( rootnode )
    net.stop()
