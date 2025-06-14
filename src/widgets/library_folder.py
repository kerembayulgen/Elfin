# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
import gi
from jellyfin_apiclient_python import JellyfinClient

from ..types.jellyfin_letter_search import JellyfinSearchResult

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/library_folder.ui")
class ElfinLibraryFolder(Gtk.Box):
    __gtype_name__: str = "ElfinLibraryFolder"

    category_name: str = ""
    search_category: str = ""
    library_id: str = ""
    icon: Gtk.Image = cast(Gtk.Image, Gtk.Template.Child())
    label: Gtk.Label = cast(Gtk.Label, Gtk.Template.Child())

    def __init__(self, library_id: str, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs, spacing=6)  # pyright: ignore[reportUnknownArgumentType]
        self.library_id = library_id
        action_group = Gio.SimpleActionGroup()

        action = Gio.SimpleAction.new("metadata", None)
        action_group.add_action(action)
        _ = action.connect("activate", self.edit_metadata)

        action = Gio.SimpleAction.new("images", None)
        action_group.add_action(action)
        _ = action.connect("activate", self.edit_images)

        action = Gio.SimpleAction.new("refresh", None)
        action_group.add_action(action)
        _ = action.connect("activate", self.refresh)

        self.insert_action_group("movie", action_group)

    def edit_metadata(self, _action: Gio.SimpleAction, _: None):
        # TODO
        print("TODO: Handle editing metadata")
        pass

    def edit_images(self, _action: Gio.SimpleAction, _: None):
        # TODO
        print("TODO: Handle editing images")
        pass

    def refresh(self, _action: Gio.SimpleAction, _: None):
        # TODO
        print("TODO: Handle refresh metadata")

    def set_label(self, thing: str):
        self.label.set_label(thing)

    def set_icon(self, collection: str):
        self.category_name = collection
        match collection:
            case "movies":
                self.icon.set_from_icon_name("video-reel-symbolic")
                self.search_category = "Movie"
            case "music":
                self.icon.set_from_icon_name("audio-x-generic-symbolic")
                self.search_category = "MusicAlbum"
            case "books":
                self.icon.set_from_icon_name("open-book-symbolic")
                self.search_category = "Book"
            case "tvshows":
                self.icon.set_from_icon_name("tv-symbolic")
                self.search_category = "Series"
            case "playlist":
                self.icon.set_from_icon_name("playlist-symbolic")
            case _:
                print(f"Unhandled collection format: {collection}")

    def get_items(self, client: JellyfinClient) -> JellyfinSearchResult:
        m: JellyfinSearchResult = cast(
            JellyfinSearchResult,
            client.jellyfin.get_items_by_letter(  # pyright: ignore[reportUnknownMemberType]
                parent_id=self.library_id, media=self.search_category
            ),
        )
        return m
