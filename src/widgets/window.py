# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402

from typing import cast
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, Gio
from jellyfin_apiclient_python import JellyfinClient

from .media_grid import ElfinMediaGrid
from .initial_setup import ElfinInitialSetup
from .sidebar import ElfinSidebar


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/window.ui")
class ElfinWindow(Adw.ApplicationWindow):
    __gtype_name__: str = "ElfinWindow"

    split: Adw.OverlaySplitView = cast(Adw.OverlaySplitView, Gtk.Template.Child())
    sidebar: ElfinSidebar = cast(ElfinSidebar, Gtk.Template.Child())
    content_stack: Gtk.Stack = cast(Gtk.Stack, Gtk.Template.Child())

    grid_view: ElfinMediaGrid = cast(ElfinMediaGrid, Gtk.Template.Child())
    initial_setup: ElfinInitialSetup = cast(ElfinInitialSetup, Gtk.Template.Child())

    def __init__(self, **kwargs) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]
        self.client: JellyfinClient = JellyfinClient()
        action = Gio.SimpleAction.new("open-home", None)
        _ = action.connect("activate", self.on_about)
        self.add_action(action)
        _ = self.initial_setup.connect_button.connect(
            "clicked", self.on_connect_clicked
        )

    def on_about(self, _: None, _x: None) -> None:
        self.content_stack.set_visible_child(self.initial_setup)

    def on_connect_clicked(self, _: None) -> None:
        logged_in = self.initial_setup.on_connect_clicked(self.client)
        if logged_in:
            self.sidebar.library_text.set_visible(True)
            self.sidebar.playlist_text.set_visible(True)
            self.grid_view.setup_client(self.client)
            self.grid_view.populate_grid()
            return
