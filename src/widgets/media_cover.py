# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
import gi
from jellyfin_apiclient_python import JellyfinClient
import requests

from ..types.jellyfin_metadata import MetadataResult
from .edit_metadata import ElfinMetadataDialog

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gtk, GObject, GLib, Gio


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

    item_id: str = ""
    client: JellyfinClient

    def __init__(self, client: JellyfinClient, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs, orientation=Gtk.Orientation.VERTICAL)  # pyright: ignore[reportUnknownArgumentType]
        action_group = Gio.SimpleActionGroup()
        self.client = client

        action = Gio.SimpleAction.new("metadata", None)
        action_group.add_action(action)
        _ = action.connect("activate", self.edit_metadata)

        self.insert_action_group("item", action_group)

    def edit_metadata(self, _action: Gio.SimpleAction, _: None):
        metadata = cast(
            MetadataResult,
            self.client.jellyfin.get_item(self.item_id),  # pyright: ignore[reportUnknownMemberType]
        )
        dialog = ElfinMetadataDialog(metadata, self.client)
        dialog.present(self.get_parent())
        pass

    def set_id(self, item_id: str):
        self.item_id = item_id

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
