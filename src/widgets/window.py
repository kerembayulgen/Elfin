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
from .home_screen import ElfinHomeScreen
from .media_page import ElfinMediaPage


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/window.ui")
class ElfinWindow(Adw.ApplicationWindow):
    __gtype_name__: str = "ElfinWindow"

    nav_view: Adw.NavigationView = cast(Adw.NavigationView, Gtk.Template.Child())
    split: Adw.OverlaySplitView = cast(Adw.OverlaySplitView, Gtk.Template.Child())
    sidebar: ElfinSidebar = cast(ElfinSidebar, Gtk.Template.Child())
    content_stack: Gtk.Stack = cast(Gtk.Stack, Gtk.Template.Child())
    main_stack: Gtk.Stack = cast(Gtk.Stack, Gtk.Template.Child())
    nav_page: Adw.NavigationPage = cast(Adw.NavigationPage, Gtk.Template.Child())
    media_page: ElfinMediaPage = cast(ElfinMediaPage, Gtk.Template.Child())

    home_screen: ElfinHomeScreen = cast(ElfinHomeScreen, Gtk.Template.Child())
    grid_view: ElfinMediaGrid = cast(ElfinMediaGrid, Gtk.Template.Child())
    initial_setup: ElfinInitialSetup = cast(ElfinInitialSetup, Gtk.Template.Child())

    def __init__(self, **kwargs) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]
        self.client: JellyfinClient = JellyfinClient()
        self.on_connect_clicked(None)

        action = Gio.SimpleAction.new("open-home", None)
        _ = action.connect("activate", self.on_home)
        self.add_action(action)
        _ = self.initial_setup.connect_button.connect(
            "clicked", self.on_connect_clicked
        )

    def on_home(self, _: None, _x: None) -> None:
        self.content_stack.set_visible_child(self.home_screen)
        self.nav_page.set_title("Home")
        self.sidebar.library_list.unselect_all()
        self.sidebar.playlist_list.unselect_all()

    def on_connect_clicked(self, _: None) -> None:
        logged_in = self.initial_setup.on_connect_clicked(self.client)
        if logged_in:
            self.main_stack.set_visible_child(self.split)
            self.sidebar.library_text.set_visible(True)
            self.sidebar.playlist_text.set_visible(True)
            self.grid_view.setup_client(self.client)
            self.grid_view.populate_grid()
            self.content_stack.set_visible_child(self.home_screen)
            self.home_screen.set_client(self.client)
            self.home_screen.get_my_media()
            return
