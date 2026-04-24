import traceback
import sys

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from database import init_db
    from routes import router
except Exception as e:
    print("IMPORT ERROR:", e)
    traceback.print_exc()
    sys.exit(1)

app = FastAPI(title="SkillBid API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router, prefix="/api")