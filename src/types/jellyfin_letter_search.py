# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

from typing import TypedDict


class JellyfinSearchItem(TypedDict):
    Name: str
    Id: str
    PremiereDate: str
    ProductionYear: int
    Overview: str
    Taglines: list[str]
    Genres: list[str]
    MediaType: str


class JellyfinSearchResult(TypedDict):
    Items: list[JellyfinSearchItem]
