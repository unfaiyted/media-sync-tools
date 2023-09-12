from __future__ import annotations  # Use this to enable postponed evaluation of type annotations

from pydantic import BaseModel, validator
from typing import List, Optional, ForwardRef, Tuple
# from .media_lists import MediaList

# class User(BaseModel):
#     userId: str
#     email: str
#     name: str
#     password: str  # Remember to hash passwords before storing
#     lists: Optional[List[ForwardRef('MediaList')]]
#     relatedConfig: Optional[List[ForwardRef('Config')]]
#     configId: Optional[str]
#
