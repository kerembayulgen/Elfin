# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

from typing import TypedDict


class MediaLibraryResult(TypedDict):
    Name: str
    Id: str
    Type: str
    IsFolder: bool
    MediaType: str
    CollectionType: str


class MediaLibrarySearch(TypedDict):
    Items: list[MediaLibraryResult]
