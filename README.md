# Steam Headless Plugin Launcher

## Features
- Display a tray icon in your task bar

## Install
(TBD)

## Develop

You can also just install the module natively in your home directory in "develop" mode.

Start by installing the dependencies.
```
# Install all required build tools
./.github/scripts/install-linux-build-tools.sh

# Setup venv 
./.github/scripts/setup-dev-venv.sh

# Set launcher version
./.github/scripts/set-version.sh
```

Then install the module:

```
python3 ./setup.py develop
```

This creates an egg symlink to the venv python lib directory for development.

To later uninstall the development symlink:

```
python3 ./setup.py develop --uninstall
```

You should now be able to run shp from the commandline:
```
shp --version
```

