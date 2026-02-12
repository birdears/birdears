# Installation Instructions

## Prerequisites

`birdears` requires **Python 3.7+** and **Sox**.

Sox (Sound eXchange) is a command-line audio processing tool that `birdears` uses to play sounds.

### Linux

Most Linux distributions have `sox` available in their package repositories.

#### Debian / Ubuntu

```sh
sudo apt update
sudo apt install python3 python3-pip python3-venv sox
```

#### Arch Linux

```sh
sudo pacman -Syu python python-pip sox
```

#### Fedora

```sh
sudo dnf install python3 python3-pip sox
```

### Termux (Android)

If you are using Termux on Android:

```sh
pkg update && pkg upgrade
pkg install python sox
```

---

## Installing birdears

### Quick Install (User)

The easiest way to install `birdears` is using `pip`:

```sh
pip install --user birdears
```

Ensure your user binary directory is in your `PATH`. If you cannot run `birdears` after installation, add this to your shell configuration (`.bashrc`, `.zshrc`, etc.):

```sh
export PATH="$(python3 -m site --user-base)/bin:${PATH}"
```

### Installation with Virtual Environment

Using a virtual environment keeps your system Python clean and avoids dependency conflicts.

1.  **Create a virtual environment**:

    ```sh
    python3 -m venv ~/.venv
    ```

2.  **Activate the environment**:

    ```sh
    source ~/.venv/bin/activate
    ```

    (By installing it inside a virtualenv you will need to run this command every time you want to use `birdears` in a new terminal session).

3.  **Install birdears**:

    ```sh
    pip install birdears
    ```

4.  **Run birdears**:

    ```sh
    birdears --help
    ```

### Upgrading

To upgrade to the latest version:

```sh
pip install --upgrade --no-cache-dir birdears
```

### Troubleshooting

If you encounter audio issues, ensure `sox` is correctly installed and that your audio drivers (ALSA, PulseAudio, PipeWire) are configured properly.
