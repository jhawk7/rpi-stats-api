import subprocess

def generateStats():
	#stats.temp = runcmd("vcgencmd measure_temp").split("temp=")[1]
	temp = "n/a"
	cpu = str(runcmd("top -bn1 | grep load | awk \'{printf \"CPU Load: %.2f\", $(NF-2)}\'"))
	mem = str(runcmd("free -m | awk \'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }\'"))
	disk_space = str(runcmd("df -h | awk \'$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}\'"))
	ip = str(runcmd("hostname -I | cut -d\' \' -f1"))
	print(f"Temp: {temp} \nCPU: {cpu} \nMEM: {mem} \nSpace: {disk_space} \nIP: {ip}")

def runcmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')

def main():
	generateStats()

if __name__ == "__main__":
	main()