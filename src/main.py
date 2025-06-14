# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false
# ruff: noqa: E402

import sys
from typing import Callable, override
import gi
from .widgets.window import ElfinWindow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw


class ElfinApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.kerembayulgen.elfin",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
            resource_base_path="/com/kerembayulgen/elfin",
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)

    @override
    def do_activate(self) -> None:
        win = self.props.active_window
        if not win:
            win = ElfinWindow(application=self)
        self.set_accels_for_action("win.open-home", ["<Alt>h"])
        win.present()

    def on_about_action(self, _: None, _x: None) -> None:
        about = Adw.AboutDialog.new_from_appdata(
            "/com/kerembayulgen/elfin/com.kerembayulgen.elfin.metainfo.xml"
        )
        about.present(self.props.active_window)

    def on_preferences_action(self, _: None, _x: None) -> None:
        print("app.preferences action activated")

    def create_action(
        self,
        name: str,
        callback: Callable[(...), None],
        shortcuts: list[str] | None = None,
    ):
        action = Gio.SimpleAction.new(name, None)
        _ = action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(_: str):
    app = ElfinApplication()
    return app.run(sys.argv)
