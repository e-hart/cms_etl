"""CMS Meta Response Model."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ContactPoint(BaseModel):
    """Contact Point."""

    field_type: str = Field(..., alias="@type")
    fn: str
    hasEmail: str


class Publisher(BaseModel):
    """Publisher."""

    field_type: str = Field(..., alias="@type")
    name: str


class DistributionItem(BaseModel):
    """Distribution Item."""

    field_type: str = Field(..., alias="@type")
    downloadURL: str
    mediaType: str


class CMSMetaResponse(BaseModel):
    """CMS Meta Response."""

    accessLevel: str
    landingPage: str
    bureauCode: List[str]
    issued: str
    field_type: str = Field(..., alias="@type")
    modified: str
    released: str
    keyword: List[str]
    contactPoint: ContactPoint
    publisher: Publisher
    identifier: str
    description: str
    title: str
    programCode: List[str]
    distribution: List[DistributionItem]
    theme: List[str]
