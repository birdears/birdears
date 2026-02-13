# birdears 🎵

<video src="https://raw.githubusercontent.com/birdears/birdears/refs/heads/master/birdears-logo.png" width="100%"></video>

[![Maintenance](https://img.shields.io/maintenance/yes/2026.svg?style=flat-square)](https://github.com/iacchus/birdears/issues/new?title=Is+birdears+still+maintained&body=Please+file+an+issue+if+the+maintained+button+says+no)
[![Build Status](https://api.cirrus-ci.com/github/iacchus/birdears.svg)](https://cirrus-ci.com/github/iacchus/birdears)
[![PyPI Version](https://img.shields.io/pypi/v/birdears.svg?style=flat-square)](https://pypi.python.org/pypi/birdears)
[![Documentation Status](https://img.shields.io/badge/readthedocs-latest-orange.svg?style=flat-square)](https://birdears.readthedocs.io/en/latest/)

**birdears** is a functional ear training tool for musicians. It helps you develop your musical ear by teaching you to recognize notes by their function within a key, rather than just by interval distance.

Inspired by the [Functional Ear Trainer](https://play.google.com/store/apps/details?id=com.kaizen9.fet.android) method, `birdears` is designed to build a strong internal sense of tonality, essential for transcription, improvisation, and composition.

---

## 🚀 Quick Start

### Installation

`birdears` requires **Python 3.7+** and **Sox**.

**Linux (Debian/Ubuntu)**:
```sh
sudo apt install python3 python3-pip sox && pip install --user birdears
```

**Termux (Android)**:
```sh
pkg install python sox && pip install birdears
```

For detailed installation instructions (Arch, Fedora, virtual environments), see [INSTALL.md](docs/INSTALL.md).

### Usage

Once installed, simply run:

```sh
birdears
```

Or for specific modes:

```sh
birdears melodic
birdears harmonic
birdears notename
```

For a full list of options: `birdears --help`

---

## 🎹 Keybindings

`birdears` uses your computer keyboard as a musical instrument.

**Standard Layout (Major Scale / Ionian)**:
-   **Natural notes** are on the lower row (`z` to `,`).
-   **Chromatic notes** are on the upper row (`s` to `l`).
-   **Shift** accesses the higher octave.

![birdears - ionian(major) keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/ionian.png)

<details>
<summary><strong>Click to see Keybindings for other Modes</strong></summary>

### Dorian
![birdears - dorian keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/dorian.png)

### Phrygian
![birdears - phryigian keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/phrygian.png)

### Lydian
![birdears - lydian keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/lydian.png)

### Mixolydian
![birdears - mixolydian keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/mixolydian.png)

### Aeolian (Minor)
![birdears - aeolian keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/minor.png)

### Locrian
![birdears - locrian(minor) keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/locrian.png)

### Advanced / Chromatic
![birdears - advanced keybindings](https://github.com/iacchus/birdears/raw/master/docs/_static/img/keybindings/keyboard-layout.png)

</details>

---

## 🧠 The Method

Unlike traditional interval trainers, `birdears` emphasizes **resolution to the tonic**. When you hear a note, you also hear (or imagine) it resolving to the home note of the key. This trains your brain to instantly recognize the "color" or function of each scale degree.

👉 **Read more about the method in [METHOD.md](docs/METHOD.md).**

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

Licensed under the [GNU AGPLv3](LICENSE.txt).
