from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class EntityContext(BaseModel):
    ip: Optional[str] = None
    host_id: Optional[str] = None
    user_id: Optional[str] = None


class ActivityContext(BaseModel):
    action: str
    process_name: Optional[str] = None
    cmd_line: Optional[str] = None
    parent_process: Optional[str] = None


class NormalizedEvent(BaseModel):
    event_id: str
    timestamp: datetime
    telemetry_type: str
    source_entity: EntityContext
    destination_entity: Optional[EntityContext] = None
    activity: ActivityContext
    raw_log_ref: str
    metadata: Optional[Dict[str, Any]] = None
