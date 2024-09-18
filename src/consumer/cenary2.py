import subprocess
import os


subprocess.call("xterm -e sudo python3 local_training_gateway.py --name h3  --solution 2 &",shell=True)
subprocess.call("xterm -e sudo python3 local_training_gateway.py --name h4  --solution 2 &",shell=True)
subprocess.call("xterm -e sudo python3 local_training_gateway.py --name h5  --solution 2 &",shell=True)
subprocess.call("xterm -e sudo python3 local_training_gateway.py --name h6  --solution 2 &",shell=True)
subprocess.call("xterm -e sudo python3 local_training_gateway.py --name h7  --solution 2 &",shell=True)
subprocess.call("xterm -e sudo python3 integrator_gateway_ml.py --name h2 --clients 5 --solution 2", shell=True)
#15