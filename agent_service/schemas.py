from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class Alert(BaseModel):
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    startsAt: datetime
    endsAt: datetime
    generatorURL: str
    fingerprint: str

class AlertmanagerWebhook(BaseModel):
    version: str
    groupKey: str
    status: str
    receiver: str
    groupLabels: Dict[str, str]
    commonLabels: Dict[str, str]
    commonAnnotations: Dict[str, str]
    externalURL: str
    alerts: List[Alert]
