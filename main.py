from fastapi import FastAPI, Response
import os
import subprocess
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Stats(BaseModel):
	temp: str
	cpu: str
	mem: str
	disk_space: str
	ip: str

@app.get("/healthcheck")
async def healthcheck():
	return {"message": "ok"}


@app.get("/stats", response_model=Stats)
async def getStats():
	return generateStats()


@app.post("/kill", status_code=204)
async def kill():
	os.system("sudo shutdown now")
	return Response(status_code=204)


@app.post("/update", status_code=204)
async def update():
	os.system("sudo apt-get update && sudo apt-get upgrade -y")
	return Response(status_code=204)


@app.post("/reboot", status_code=204)
async def reboot():
	os.system("sudo shutdown -r")
	return Response(status_code=204)


def generateStats():
	#stats.temp = runcmd("vcgencmd measure_temp").split("temp=")[1]
	temp = "n/a"
	cpu = str(runcmd("top -bn1 | grep load | awk \'{printf \"CPU Load: %.2f\", $(NF-2)}\'"))
	mem = str(runcmd("free -m | awk \'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }\'"))
	space = str(runcmd("df -h | awk \'$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}\'"))
	ip = str(runcmd("hostname -I | cut -d\' \' -f1"))
	#return {"temp": stats.temp, "cpu": status.cpu, "mem": stats.mem, "disk_space": stats.disk_space, "ip": stats.ip}
	stats = Stats(temp=temp, cpu=cpu, mem=mem, disk_space=space, ip=ip)
	return stats


def runcmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)

	