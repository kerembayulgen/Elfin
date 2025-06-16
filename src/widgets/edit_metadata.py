# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
import gi
from gi.repository.Pango import EllipsizeMode
from jellyfin_apiclient_python import JellyfinClient
import requests

from ..types.jellyfin_metadata import MetadataPerson, MetadataResult

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gdk, Gtk, Adw, Gio


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/edit_metadata.ui")
class ElfinMetadataDialog(Adw.Dialog):
    __gtype_name__: str = "ElfinMetadataDialog"

    path: Adw.ActionRow = cast(Adw.ActionRow, Gtk.Template.Child())
    title: Adw.EntryRow = cast(Adw.EntryRow, Gtk.Template.Child())
    sort_title: Adw.EntryRow = cast(Adw.EntryRow, Gtk.Template.Child())
    overview: Adw.EntryRow = cast(Adw.EntryRow, Gtk.Template.Child())
    year: Adw.EntryRow = cast(Adw.EntryRow, Gtk.Template.Child())
    genre_group: Adw.PreferencesGroup = cast(Adw.PreferencesGroup, Gtk.Template.Child())
    genre_box: Gtk.Box = cast(Gtk.Box, Gtk.Template.Child())
    add_more: Gtk.Button = cast(Gtk.Button, Gtk.Template.Child())
    people_list: Gtk.ListBox = cast(Gtk.ListBox, Gtk.Template.Child())

    def __init__(self, metadata: MetadataResult, client: JellyfinClient, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]
        self.metadata: MetadataResult = metadata
        self.client: JellyfinClient = client
        self._init_metadata_fields(metadata)
        self._init_genres(metadata)
        self._load_people_list(metadata)

    def _init_metadata_fields(self, metadata: MetadataResult):
        self.path.set_subtitle(metadata["Path"])
        self.title.set_text(metadata["Name"])
        self.sort_title.set_text(metadata["SortName"])
        overview = metadata.get("Overview")
        if overview:
            self.overview.set_text(overview)
        production_year = metadata.get("ProductionYear")
        if production_year:
            self.year.set_text(str(production_year))

    def _load_people_list(self, metadata: MetadataResult):
        people = metadata.get("People", [])
        if people:
            _ = GLib.idle_add(self._start_loading_people, people)

    def _start_loading_people(self, people: list[MetadataPerson]) -> bool:
        for person in people:
            self._load_person_row(person)
        return False

    def _load_person_row(self, person: MetadataPerson):
        action_row = Adw.ActionRow()
        avatar = Adw.Avatar(size=40, text=person["Name"])
        action_row.add_prefix(avatar)
        action_row.set_title(person["Name"])
        action_row.set_subtitle(person["Role"])
        remove_button = Gtk.Button(icon_name="user-trash-symbolic")
        remove_button.set_css_classes(["flat", "circular"])
        action_row.add_suffix(remove_button)
        self.people_list.append(action_row)

        image_url: str = cast(
            str,
            self.client.jellyfin.artwork(  # pyright: ignore[reportUnknownMemberType]
                item_id=person["Id"], art="Primary", max_width=0
            ),
        )
        self._fetch_image_async(image_url, avatar, person["Name"])

    def _fetch_image_async(self, url: str, avatar: Adw.Avatar, person_name: str):
        cancellable = Gio.Cancellable()

        _ = GLib.Thread.new(
            None, self._fetch_image_thread, (url, avatar, person_name, cancellable)
        )

    def _fetch_image_thread(self, data: tuple[str, Adw.Avatar, str, Gio.Cancellable]):
        url: str = data[0]
        avatar: Adw.Avatar = data[1]
        person_name: str = data[2]
        cancellable = data[3]
        url, avatar, person_name, cancellable = data
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_bytes = response.content

            if not cancellable.is_cancelled():
                _ = GLib.idle_add(
                    self._update_avatar_with_image, avatar, image_bytes, person_name
                )
        except Exception:
            pass

    def _update_avatar_with_image(
        self, avatar: Adw.Avatar, image_bytes: bytes, person_name: str
    ) -> bool:
        try:
            texture = Gdk.Texture.new_from_bytes(GLib.Bytes.new(image_bytes))
            avatar.set_custom_image(texture)
        except Exception:
            avatar.set_text(person_name)
        return False

    def _init_genres(self, metadata: MetadataResult):
        genres = metadata.get("Genres")
        if genres:
            self.genre_box.remove(self.add_more)
            for genre in genres:
                container = self._create_genre_tag(genre)
                self.genre_box.append(container)
            self.genre_box.append(self.add_more)

    def _create_genre_tag(self, genre: str) -> Gtk.Box:
        container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        container.set_hexpand(False)
        container.set_css_classes(["tag"])

        label = Gtk.Label(label=genre)
        label.set_xalign(0.0)
        label.set_ellipsize(EllipsizeMode.END)
        container.append(label)

        button = Gtk.Button(icon_name="window-close-symbolic")
        _ = button.connect("clicked", self.remove_button)
        button.set_css_classes(["flat", "circular"])
        container.append(button)
        return container

    def remove_button(self, button: Gtk.Button):
        parent = button.get_parent()
        if parent:
            parent = cast(Gtk.Box, parent)
            wrap_box = parent.get_parent()
            if wrap_box:
                wrap_box = cast(Gtk.Box, wrap_box)
                wrap_box.remove(parent)
