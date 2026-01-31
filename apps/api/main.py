from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import auth, mail, localdrop, media
from database import create_db_and_tables
from services.localdrop_service import announce_self


app = FastAPI(title="OpenMail Hub API")

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    announce_self(8000)
    from workers.sync_worker import start_sync_worker
    start_sync_worker()

app.mount("/static", StaticFiles(directory="media_vault"), name="static")

app.include_router(auth.router)
app.include_router(mail.router)
app.include_router(localdrop.router)
app.include_router(media.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "OpenMail Hub API is running"}
