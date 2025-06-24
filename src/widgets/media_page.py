# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, Gdk


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/media_page.ui")
class ElfinMediaPage(Adw.NavigationPage):
    __gtype_name__: str = "ElfinMediaPage"

    blurred_cover: Gtk.Picture = cast(Gtk.Picture, Gtk.Template.Child())
    banner_image: Gtk.Picture = cast(Gtk.Picture, Gtk.Template.Child())

    def __init__(self, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]

    def set_background(self, texture: Gdk.Texture):
        self.blurred_cover.set_paintable(texture)
        self.blurred_cover.set_opacity(0.4)
