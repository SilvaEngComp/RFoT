import json
import fileinput
from operator import itemgetter

class to_object(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
			

def return_hosts():
    f=open('data_hosts.json','r')
    st=[]
    st=f.readlines()
    f.close()
    lines = len(st)
    hosts=[]
    for i in range(0,(lines)):
        hosts.append(to_object(st[i]))
    return hosts

def return_association():
	f=open('association_hosts.json','r')
	st=[]
	st=f.readlines()
	f.close()
	lines = len(st)
	devices=[]
	for i in range(0,(lines)):
		obj = to_object(st[i])		
		if(obj.name_gateway!='cloud'):
				devices.append(obj)
	return devices


	
def return_hosts_per_type(type_host):
	hosts=return_hosts()
	re = []
	for i in range(0,len(hosts)):
		if (hosts[i].type==type_host) :
			re.append(hosts[i])
	return re

	
def write_host(st):
	x=open('data hosts.json','a')
	x.write(st+"\n")
	x.close()


def write_hosts(h):
	for i in range(0,len(h)):
		write_host(json.dumps(h[i]))


def return_host_per_name(name_host):
	#print("utils")
	h=return_hosts()
	#print("utils2")
	for i in range(0,len(h)):
		if(str(h[i].name)==name_host or str(h[i].name_iot)==name_host):
			#print(h[i].name)
			return h[i]


def update_flow(value):
	a_file = open("config.json", "r")
	json_object = json.load(a_file)
	a_file.close()
	if(json_object["publish"]!=value):
		json_object["publish"] = int(value)
		json_object["collect"] = int(value)
		a_file = open("config.json", "w")
		json.dump(json_object, a_file)
		a_file.close()

def get_pub():
	with open('config.json') as f:
		data = json.load(f)
	pub=data["publish"]
	return pub
