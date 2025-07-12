# oidcheck/models.py
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class AppConfig(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None
    authority: Optional[str] = None
    redirect_uri: Optional[HttpUrl] = None
    scope: List[str] = []
    log_level: str = "INFO"

    def __init__(self, **data):
        if "scope" in data and isinstance(data["scope"], str):
            data["scope"] = data["scope"].split()
        super().__init__(**data)
