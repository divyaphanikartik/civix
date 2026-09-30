from fastapi import FastAPI

from app.api.whatsapp import router as whatsapp_router
from app.api.hotspots import router as hotspots_router
from app.api.grievances import router as grievances_router
from app.api.projects import router as projects_router
from app.api.datasets import router as datasets_router
from app.db.database import Base, engine

# Import models so SQLAlchemy registers their tables with Base.
from app.models.grievance import Grievance  # noqa: F401,E402
from app.models.hotspot import Hotspot  # noqa: F401,E402
from app.models.project import ProjectConceptNote  # noqa: F401,E402
from app.models.whatsapp import WhatsAppMessage  # noqa: F401,E402


app = FastAPI(
    title="Civix API",
    description="Citizen-driven infrastructure intelligence platform",
    version="1.0.0",
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(whatsapp_router, prefix="/api")
app.include_router(hotspots_router, prefix="/api")
app.include_router(grievances_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(datasets_router, prefix="/api")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "civix-backend",
    }
