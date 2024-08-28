
from mininet.net import Mininet

from mininet.log import lg
from mininet.node import Node, RemoteController, Controller, OVSKernelSwitch
from mininet.topolib import TreeNet
import time
import argparse
import utils_hosts
import json
import random

nat = None
#seed usados 10, 11 e 12
random.seed(12)
service_mix_path= '/home/openflow/service-mix'
fuseki_path='/home/openflow/fuseki/apache-jena-fuseki-3.11.0'

	#################################
def startNAT( root, inetIntf='eth0', subnet='10.0/8' ):
	"""Start NAT/forwarding between Mininet and external network
	root: node to access iptables from
	inetIntf: interface for internet access
	subnet: Mininet subnet (default 10.0/8)="""

	# Identify the interface connecting to the mininet network
	localIntf = root.defaultIntf()

	# Flush any currently active rules
	root.cmd( 'iptables -F' )
	root.cmd( 'iptables -t nat -F' )

	# Create default entries for unmatched traffic
	root.cmd( 'iptables -P INPUT ACCEPT' )
	root.cmd( 'iptables -P OUTPUT ACCEPT' )
	root.cmd( 'iptables -P FORWARD DROP' )

	# Configure NAT
	root.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet, '-j DROP' )
	root.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet, '-j ACCEPT' )
	root.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet, '-j ACCEPT' )
	root.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )

	# Instruct the kernel to perform forwarding
	root.cmd( 'sysctl net.ipv4.ip_forward=1' )


#def getNAT():
	
def stopNAT( root ):
	"""Stop NAT/forwarding between Mininet and external network"""
	# Flush any currently active rules
	root.cmd( 'iptables -F' )
	root.cmd( 'iptables -t nat -F' )

	# Instruct the kernel to stop forwarding
	root.cmd( 'sysctl net.ipv4.ip_forward=0' )

def fixNetworkManager( root, intf ):
	"""Prevent network-manager from messing with our interface,
	   by specifying manual configuration in /etc/network/interfaces
	   root: a node in the root namespace (for running commands)
	   intf: interface name"""
	cfile = '/etc/network/interfaces'
	line = '\niface %s inet manual\n' % intf
	config=''
	try:
		config = open( cfile ).read()
	except:
		cfile = '/etc/netplan'
		config = open( cfile ).read()
	if line not in config:
		print ('*** Adding', line.strip(), 'to', cfile)
		with open( cfile, 'a' ) as f:
			f.write( line )
		# Probably need to restart network-manager to be safe -
		# hopefully this won't disconnect you
		root.cmd( 'service network-manager restart' )

def connectToInternet( network, switch='s1', rootip='10.254', subnet='10.0/8'):
	"""Connect the network to the internet
	   switch: switch to connect to root namespace
	   rootip: address for interface in root namespace
	   subnet: Mininet subnet"""
	switch = network.get( switch )
	prefixLen = subnet.split( '/' )[ 1 ]

	# Create a node in root namespace
	root = Node( 'root', inNamespace=False )

	# Prevent network-manager from interfering with our interface
	fixNetworkManager( root, 'root-eth0' )

	# Create link between root NS and switch
	link = network.addLink( root, switch )
	link.intf1.setIP( rootip, prefixLen )

	# Start network that now includes link to root namespace
	network.start()

	# Start NAT and establish forwarding
	startNAT( root )

	# Establish routes from end hosts
	for host in network.hosts:
		host.cmd( 'ip route flush root 0/0' )
		host.cmd( 'route add -net', subnet, 'dev', host.defaultIntf() )
		host.cmd( 'route add default gw', rootip )

	return root


		
def initGateways(net):
	print("Init Gateways")
	g=utils_hosts.return_hosts_per_type('gateway')
	for i in range(0,len(g)):
		print(g[i].name)
		net.get(g[i].name).cmdPrint('mosquitto &')
		#net.get('h6').cmd('python3 servico.py &')
	time.sleep(5)
			
	
def stop_gateways(net):
	g=utils_hosts.return_hosts_per_type('gateway')
	
	for i in range(0,len(g)):
		if((i+1)<10):
			net.get(g[i].name).cmdPrint('cd '+service_mix_path+'/0'+str(i+1)+'/bin; ./stop &')
		else:
			net.get(g[i].name).cmdPrint('cd '+service_mix_path+'/'+str(i+1)+'/bin; ./stop &')
		time.sleep(5)

	

def initSensors(net):
	print("\n\n......Init Sensors....\n")
	#tipos de sensores no arquivo sensors.py, ex: temperatureSensor, soilmoistureSensor, solarradiationSensor, ledActuator
	s=utils_hosts.return_hosts_per_type('sensor')
	ass=utils_hosts.return_association()
	for i in range(0,len(ass)):
		name = 'sc0' if i+1<10 else 'sc'
		name +=  str(i+1)
		print('initting: ',name)
		net.get(s[i].name).cmdPrint('python3 paho_init.py --name '+name+' --broker '+str(ass[i].gateway)+' &')
		time.sleep(0.2)

def initFlow(net):
	print ("Temp: Init Flow")
	g=utils_hosts.return_hosts_per_type('gateway')
	ass=utils_hosts.return_association()
	#10seg
	col=10
	pub=10
	#ind=0
	valid_gatways = []
	for i in range(0,len(g)):
		valid_gatways.append(g[i].name)
	for j in range(0,len(ass)):
		if ass[j].name_gateway in valid_gatways:
			topic = 'dev/'+ass[j].name
			print("mosquitto_pub -t '"+topic+"' -m '{\"method\":\"flow\", \"sensor\":\""+ass[j].type+"\", \"time\":{\"collect\":"+str(col)+",\"publish\":"+str(pub)+"}}'")
			net.get(ass[j].name_gateway).cmd("mosquitto_pub -t '"+topic+"' -m '{\"method\":\"flow\", \"sensor\":\""+ass[j].type+"\", \"time\":{\"collect\":"+str(col)+",\"publish\":"+str(pub)+"}}'")
			time.sleep(0.5)
def executeCenare1(net):
    print('execution scenare 1')
    net.get('h3').cmdPrint("cd current_model/ ")
    net.get('h3').cmdPrint("sudo python3 collector_gateway.py --name h1 --size 20")
			
