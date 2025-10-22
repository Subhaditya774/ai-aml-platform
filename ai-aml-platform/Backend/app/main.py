from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transactions, alerts

app = FastAPI(
    title="AI AML Platform",
    description="Backend API for AI-powered Anti-Money Laundering (AML) dashboard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to AI AML Platform Backend!"}
