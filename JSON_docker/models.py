"""
Shared data models and enums for the Video Transcoding Service
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class Main:
    """Main model used in ReplyRef model"""
    cid: str
    uri: str
    py_type: str

@dataclass
class ReplyRef:
    """ReplyRef model used in DataModelRetrieved model"""
    parent: Main
    root: Main

@dataclass
class CommandMessage:
    """Mirrors CommandMessage in ContainerMuscleBot/MuscleBot/commands/Commands.cs"""
    message: str = "request"
    requestID: int = -1
    path: List[str] = None
    iterations: int = 1
    status: str = "requested"

    def __post_init__(self):
        if self.path is None:
            self.path = ["dataRequest"]

@dataclass
class DataModelRetrieved:
    """DataModelRetrieved taking out specify data from the documents"""
    display_name: str
    text: str
    created_at: str
    handle: str
    reply: ReplyRef #object  ReplyRef inside is a <class 'tuple'>
    tags: str  #could be int or string, None was the value compared
    indexed_at: str
    python_map: str
    # {
    #     "display_name": str,
    #     "text": str,
    #     "created_at": str,
    #     "handle": str,
    #     "reply": ReplyRef, #object  ReplyRef inside is a <class 'tuple'>
    #     "tags": str,  #could be int or string, None was the value compared
    #     "indexed_at": str,
    #     "python_map": str,
    # }