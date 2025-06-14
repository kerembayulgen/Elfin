pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'elfin'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/window.blp',
    'gtk/help_overlay.blp',
    'gtk/media_cover.blp',
    'gtk/library_folder.blp',
    'gtk/sidebar.blp',
    'gtk/initial_setup.blp',
    'gtk/media_grid.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)


gnome.compile_resources('elfin',
  'elfin.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: [blueprints, appstream_file],
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'elfin.in',
  output: 'elfin',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

elfin_sources = [
  '__init__.py',
  'main.py',
  'widgets/window.py',
  'widgets/__init__.py',
  'widgets/library_folder.py',
  'widgets/media_cover.py',
  'widgets/sidebar.py',
  'widgets/initial_setup.py',
  'widgets/media_grid.py',
  'types/__init__.py',
  'types/jellyfin_letter_search.py',
  'types/jellyfin_media_folders.py'
]

install_subdir('widgets', install_dir: moduledir)
install_subdir('types', install_dir: moduledir)
install_data(elfin_sources, install_dir: moduledir)
