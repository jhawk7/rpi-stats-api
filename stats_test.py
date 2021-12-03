import subprocess

def generateStats():
	#stats.temp = runcmd("vcgencmd measure_temp").split("temp=")[1]
	temp = "n/a"
	cpu = str(runcmd("top -bn1 | grep load | awk \'{printf \"%.2f\", $(NF-2)}\'"))
	mem = str(runcmd("free -m | awk \'NR==2{printf \"%s/%s MB %.2f%%\", $3,$2,$3*100/$2 }\'"))
	disk_space = str(runcmd("df -h | awk \'$NF==\"/\"{printf \"%d/%d GB %s\", $3,$2,$5}\'"))
	ip = str(runcmd("hostname -I | cut -d\' \' -f1")).split('\n')[0]
	desc = str(runcmd("cat ~/about.txt")).split('\n')[0]
	print(f"Temp: {temp} \nCPU: {cpu} \nMEM: {mem} \nSPACE: {disk_space} \nIP: {ip}DESC: {desc}")

def runcmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')

def main():
	generateStats()

if __name__ == "__main__":
	main()