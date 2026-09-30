from pydantic import BaseModel


class HealthResponse(BaseModel):

    status: str

    service: str


class ProcessingResponse(BaseModel):

    job_id: str

    status: str

    message: str