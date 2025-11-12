# oidcheck/models.py
from pydantic import BaseModel, HttpUrl, model_validator
from typing import Optional, List


class AppConfig(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None
    authority: Optional[str] = None
    redirect_uri: Optional[HttpUrl] = None
    scope: Optional[List[str]] = None
    log_level: str = "INFO"

    @model_validator(mode="before")
    def split_scope(cls, values):
        if "scope" in values and isinstance(values["scope"], str):
            values["scope"] = values["scope"].split()
        elif "scope" not in values or values["scope"] is None:
            values["scope"] = []
        return values
