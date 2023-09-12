from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional, ForwardRef

#
# class ConfigClientFieldsValue(BaseModel):
#     configClientFieldValueId: Optional[str] = None
#     configClientFieldId: str
#     clientField: Optional[ForwardRef('ClientField')]
#     configClientId: str
#     value: str
#
#
# class SyncOptions(BaseModel):
#     syncOptionsId: str = None
#     configId: str
#     collections: bool
#     playlists: bool
#     lovedTracks: bool
#     topLists: bool
#     watched: bool
#     ratings: bool
#     trakt: bool
#     libraries: bool
#
#
# class ConfigClient(BaseModel):
#     configClientId: str = None
#     label: str
#     client: Optional[ForwardRef('Client')]
#     clientId: str
#     configId: str
#     clientFields: Optional[List[ForwardRef('ClientField')]]
#     clientFieldValues: Optional[List[ForwardRef('ConfigClientFieldsValue')]]
