from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class OutboxMessagesS(BaseModel):
    id: int
    data: str
    routing_key: str
    broker_name: str
    sent_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OutboxMessagesCreateS(BaseModel):
    data: str
    routing_key: str
    broker_name: str