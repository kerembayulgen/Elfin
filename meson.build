project('elfin',
          version: '0.1.0',
    meson_version: '>= 1.0.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')

# Generate the metainfo file that will be used in both data and src
appstream_file = i18n.merge_file(
  input: 'data/com.kerembayulgen.elfin.metainfo.xml.in',
  output: 'com.kerembayulgen.elfin.metainfo.xml',
  po_dir: 'po',
  install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
