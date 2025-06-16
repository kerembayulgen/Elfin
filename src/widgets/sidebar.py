# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
from gi.repository import Gtk

from .library_folder import ElfinLibraryFolder


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/sidebar.ui")
class ElfinSidebar(Gtk.Box):
    __gtype_name__: str = "ElfinSidebar"

    library_text: Gtk.Label = cast(Gtk.Label, Gtk.Template.Child())
    library_list: Gtk.ListBox = cast(Gtk.ListBox, Gtk.Template.Child())

    playlist_text: Gtk.Label = cast(Gtk.Label, Gtk.Template.Child())
    playlist_list: Gtk.ListBox = cast(Gtk.ListBox, Gtk.Template.Child())

    def __init__(self, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]
        _ = self.library_list.connect("row-activated", self.on_library_changed)

    def on_library_changed(self, _: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        parent = row.get_child()
        if not parent:
            return
        window = row.get_root()
        if not window:
            return
        parent = cast(ElfinLibraryFolder, parent)
        items = parent.get_items()
        window.nav_page.set_title(parent.label.get_text())  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        window.grid_view.add_movies(items)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
