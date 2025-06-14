# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2025 Kerem Bayülgen

# pyright: reportMissingModuleSource=false, reportMissingTypeStubs=false
# ruff: noqa: E402
from typing import cast

import gi


gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Secret", "1")

from gi.repository import Adw, Gio, Gtk, Secret
from jellyfin_apiclient_python import JellyfinClient

SCHEMA_ID = "com.kerembayulgen.elfin"
PASSWORD_SCHEMA = Secret.Schema.new(
    f"{SCHEMA_ID}.Store",
    Secret.SchemaFlags.NONE,
    {
        "username": Secret.SchemaAttributeType.STRING,
        "server": Secret.SchemaAttributeType.STRING,
    },
)


@Gtk.Template(resource_path="/com/kerembayulgen/elfin/gtk/initial_setup.ui")
class ElfinInitialSetup(Gtk.Box):
    __gtype_name__: str = "ElfinInitialSetup"

    serveraddress: Adw.EntryRow = cast(Adw.EntryRow, Gtk.Template.Child())
    username: Adw.EntryRow = cast(Adw.EntryRow, Gtk.Template.Child())
    password: Adw.PasswordEntryRow = cast(Adw.PasswordEntryRow, Gtk.Template.Child())
    connect_button: Gtk.Button = cast(Gtk.Button, Gtk.Template.Child())
    toast_overlay: Adw.ToastOverlay = cast(Adw.ToastOverlay, Gtk.Template.Child())

    def __init__(self, **kwargs) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]
        flags = Gio.SettingsBindFlags.DEFAULT

        self.settings: Gio.Settings = Gio.Settings(schema_id=SCHEMA_ID)
        self.settings.bind("serveraddress", self.serveraddress, "text", flags)
        self.settings.bind("username", self.username, "text", flags)

        self.is_logged_in: bool = False
        self._load_existing_password()

    def on_connect_clicked(self, client: JellyfinClient) -> bool:
        if self.is_logged_in:
            return False
        self.login(client)
        if not self.is_logged_in:
            return False
        return True

    def login(self, client: JellyfinClient) -> None:
        _ = self.store_password()
        client.config.app("Elfin", "0.0.1", "ElfinMachine", "ElfinDevice")  # pyright: ignore[reportUnknownMemberType]
        client.config.data["auth.ssl"] = True  # pyright: ignore[reportUnknownMemberType]

        username = self.username.get_text()
        password = self.get_password()
        server_address = self.serveraddress.get_text()

        _ = client.auth.connect_to_address(server_address)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        status = client.auth.login(f"http://{server_address}", username, password)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        if status != {}:
            self.is_logged_in = True
        else:
            self.toast_overlay.add_toast(Adw.Toast(title="Unable to open log in!"))

    def _load_existing_password(self) -> None:
        username = self.username.get_text()
        server = self.serveraddress.get_text()

        if username and server:
            stored_password = self.get_password()
            if stored_password:
                self.password.set_text(stored_password)

    def get_password(self) -> str:
        password = Secret.password_lookup_sync(
            PASSWORD_SCHEMA,
            {
                "username": self.username.get_text(),
                "server": self.serveraddress.get_text(),
            },
        )
        return password

    def store_password(self) -> bool:
        username = self.username.get_text()
        server = self.serveraddress.get_text()
        password = self.password.get_text()

        success = Secret.password_store_sync(
            PASSWORD_SCHEMA,
            {"username": username, "server": server},
            Secret.COLLECTION_DEFAULT,
            f"Elfin Password for {username}@{server}",
            password,
        )
        return success
