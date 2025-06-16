# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

from typing import NotRequired, TypedDict


class MetadataPerson(TypedDict):
    Name: str
    Id: str
    Role: str
    Type: str
    PrimaryImageTag: str


class MetadataResult(TypedDict):
    Name: str
    DateCreated: str
    SortName: str
    Path: str
    IsFolder: bool
    Overview: NotRequired[str]
    PremiereDate: NotRequired[str]
    MediaType: str
    ProductionYear: NotRequired[int]
    CommunityRating: NotRequired[float]
    CriticRating: NotRequired[float]
    Genres: NotRequired[list[str]]
    People: list[MetadataPerson]
