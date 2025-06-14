# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
import gi
from jellyfin_apiclient_python import JellyfinClient

from ..types.jellyfin_letter_search import JellyfinSearchResult

from .media_cover import ElfinMediaCover, MediaItem

from .library_folder import ElfinLibraryFolder

from ..types.jellyfin_media_folders import MediaLibrarySearch

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/media_grid.ui")
class ElfinMediaGrid(Gtk.ScrolledWindow):
    __gtype_name__: str = "ElfinMediaGrid"

    movie_grid: Gtk.GridView = cast(Gtk.GridView, Gtk.Template.Child())
    movies: Gio.ListStore
    grid_factory: Gtk.SignalListItemFactory
    client: JellyfinClient = JellyfinClient()

    def __init__(self, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        _ = self.movie_grid.connect("activate", self.on_movie_clicked)
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]

    def setup_client(self, client: JellyfinClient):
        self.client = client

    def populate_grid(self) -> None:
        media_folders: MediaLibrarySearch = cast(
            MediaLibrarySearch,
            self.client.jellyfin.get_media_folders(),  # pyright: ignore[reportUnknownMemberType]
        )
        root = self.get_root()
        if not root:
            return
        for folder in media_folders["Items"]:
            item_definition = cast(
                JellyfinSearchResult,
                self.client.jellyfin.get_items_by_letter(parent_id=folder["Id"]),  # pyright: ignore[reportUnknownMemberType]
            )
            if folder["CollectionType"] == "playlists":
                for playlist in item_definition["Items"]:
                    item = ElfinLibraryFolder(playlist["Id"])
                    item.set_label(playlist["Name"])
                    item.set_icon("playlist")
                    item.label.set_halign(Gtk.Align.START)
                    row = Gtk.ListBoxRow()
                    row.set_child(item)
                    root.sidebar.playlist_list.append(row)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

                continue
            lib_folder = ElfinLibraryFolder(folder["Id"])
            lib_folder.set_label(folder["Name"])
            lib_folder.set_icon(folder["CollectionType"])
            lib_folder.label.set_halign(Gtk.Align.START)
            row = Gtk.ListBoxRow()
            row.set_child(lib_folder)
            root.sidebar.library_list.append(row)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            self.movies = Gio.ListStore.new(MediaItem)
            self.grid_factory = Gtk.SignalListItemFactory()
            _ = self.grid_factory.connect("setup", self.on_grid_item_setup)
            _ = self.grid_factory.connect("bind", self.on_grid_item_bind)
            root.grid_view.movie_grid.set_factory(self.grid_factory)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    def on_grid_item_setup(self, _: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        movie_widget = ElfinMediaCover()
        list_item.set_child(movie_widget)

    def on_grid_item_bind(self, _: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        movie_data = list_item.get_item()
        movie_widget = list_item.get_child()
        if movie_widget and movie_data:
            movie_data = cast(MediaItem, movie_data)
            movie_widget = cast(ElfinMediaCover, movie_widget)
            movie_widget.set_label(movie_data.name)
            movie_widget.set_year(movie_data.year)
            movie_widget.set_cover(movie_data.cover_art)

    def add_movies(self, children: JellyfinSearchResult):
        while self.movies.get_n_items() > 0:
            self.movies.remove(0)
        for child in children["Items"]:
            cover = cast(str, self.client.jellyfin.artwork(child["Id"], "Primary", 350))  # pyright: ignore[reportUnknownMemberType]
            production_year = 0
            if child.get("ProductionYear"):
                production_year = child["ProductionYear"]
            self.movies.append(
                MediaItem(child["Name"], cover, child["Id"], production_year)
            )
        self.get_root().content_stack.set_visible_child(self)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportOptionalMemberAccess]
        self.movie_grid.set_model(Gtk.NoSelection.new(self.movies))

    def on_movie_clicked(self, _: Gtk.GridView, _i: int):
        selection_model = self.movie_grid.get_model()
        if not selection_model:
            return
        selection_model = cast(Gtk.NoSelection, selection_model)
        list_model = selection_model.get_model()
        if not list_model:
            return
        print("TODO: Handle Movie Clicked")
