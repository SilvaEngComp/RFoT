#!/usr/bin/python

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import lg

if __name__ == '__main__':
	lg.setLogLevel( 'info')
	#root = Node('root', inNamespace=False)
	#root.cmd('sudo mn -c')
	import network_init as ni
	net = Mininet(link=TCLink)
	#criar switches, hosts e topologia
	import create_topo
	create_topo.create(net)
	
	# Configurar e iniciar comunicacao externa
	rootnode = ni.connectToInternet( net )
	
	ni.initGateways(net)
	
	#Iniciar sensores virtuais
	ni.initSensors(net)
	
	#Iniciar fluxo de comunicacao
	ni.initFlow(net)

	CLI( net )
	
	# Iniciar inscricao dos subscribers
	#set_subscribers(net)
	# Shut down NAT
	ni.stopNAT( rootnode )
	#stop_gateways(net)
	#time.sleep(15)
	net.stop()
