# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
import gi
from jellyfin_apiclient_python import JellyfinClient

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/home_screen.ui")
class ElfinHomeScreen(Gtk.Box):
    __gtype_name__: str = "ElfinHomeScreen"

    my_media_list: Gtk.Box = cast(Gtk.Box, Gtk.Template.Child())

    def __init__(self, **kwargs) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]
        self.client: JellyfinClient

    def set_client(self, client: JellyfinClient):
        self.client = client

    def get_my_media(self): ...
