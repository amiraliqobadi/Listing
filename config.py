from fastapi.middleware.cors import CORSMiddleware
import logging.config
import yaml
from fastapi import FastAPI, Request, Depends, HTTPException
from datetime import datetime, timedelta
from routers import auth, listing
from fastapi import FastAPI
from routers.auth import limiter


app = FastAPI()
app.state.limiter = limiter

app.include_router(auth.router)
app.include_router(listing.router)

# Only accept requests from localhost:3000
origins = [
	"http://localhost:3000/",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Logger implementation
logger = logging.getLogger(__name__)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
	start_time = datetime.now()
	response = await call_next(request)
	process_time = (datetime.now() - start_time).total_seconds()
	ip = request.client.host
	logger.info(
		f"{request.method} {request.url} - {ip} - {process_time}s",
		extra={"request": request, "response": response},
	)
	return response


with open("logging.yaml", "r") as f:
	log_cfg = yaml.safe_load(f.read())
	log_cfg["handlers"]["fileHandler"]["filename"] = "application.log"
	logging.config.dictConfig(log_cfg)
	
	
	
