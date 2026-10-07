"""نقطة تشغيل الباك إند — FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth_router, dashboard_router, homepage_router, orders_router, products_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Electronics Store API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(orders_router.router)
app.include_router(dashboard_router.router)
app.include_router(homepage_router.router)


@app.get("/")
def root():
    return {"ok": True, "service": "Electronics Store API", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"ok": True}
