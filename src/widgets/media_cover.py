# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
import gi
import requests

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gtk, GObject, GLib


class MediaItem(GObject.GObject):
    name: str = ""
    cover_art: str = ""
    item_id: str = ""
    year: int = 0

    def __init__(self, name: str, cover_art: str, item_id: str, year: int):
        super().__init__()
        self.name = name
        self.cover_art = cover_art
        self.item_id = item_id
        self.year = year


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/media_cover.ui")
class ElfinMediaCover(Gtk.Box):
    __gtype_name__: str = "ElfinMediaCover"

    label: Gtk.Label = cast(Gtk.Label, Gtk.Template.Child())
    pic: Gtk.Picture = cast(Gtk.Picture, Gtk.Template.Child())
    year: Gtk.Label = cast(Gtk.Label, Gtk.Template.Child())

    def __init__(self, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs, orientation=Gtk.Orientation.VERTICAL)  # pyright: ignore[reportUnknownArgumentType]

    def set_label(self, name: str):
        self.label.set_text(name)

    def set_year(self, year: int):
        self.year.set_text(str(year))

    def set_cover(self, cover_art: str):
        url = requests.get(cover_art)
        try:
            tex = Gdk.Texture.new_from_bytes(GLib.Bytes.new(url.content))
            self.pic.set_paintable(tex)
        except BaseException as e:
            print(f"DEBUG: {e}")
