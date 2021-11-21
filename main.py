from fastapi import FastAPI
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


@app.post("/kill", status_code=204)
async def kill():
	os.system("sudo shutdown now")
	return {"message", "kill received"}


@app.get("/stats", response_model=Stats)
async def getStats():
	stats = Stats()
	stats.temp = runcmd("vcgencmd measure_temp").split("temp=")[1]
	stats.cpu = runcmd("top -bn1 | grep load | awk \'{printf \"CPU Load: %.2f\", $(NF-2)}\'")
	stats.mem = runcmd("free -m | awk \'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }\'")
	stats.disk_space = runcmd("df -h | awk \'$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}\'")
	stats.ip = runcmd("hostname -I | cut -d\' \' -f1")


def runcmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)

	