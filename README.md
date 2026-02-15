# birdears 🎵

[![Maintenance](https://img.shields.io/maintenance/yes/2026.svg?style=flat-square)](https://github.com/iacchus/birdears/issues/new?title=Is+birdears+still+maintained&body=Please+file+an+issue+if+the+maintained+button+says+no)
[![Build Status](https://api.cirrus-ci.com/github/iacchus/birdears.svg)](https://cirrus-ci.com/github/iacchus/birdears)
[![PyPI Version](https://img.shields.io/pypi/v/birdears.svg?style=flat-square)](https://pypi.python.org/pypi/birdears)
[![Documentation Status](https://img.shields.io/badge/readthedocs-latest-orange.svg?style=flat-square)](https://birdears.readthedocs.io/en/latest/)
<!-- [![Coveralls](https://img.shields.io/coveralls/birdears/birdears.svg?style=flat-square&label=coverage)](https://coveralls.io/github/birdears/birdears) -->

<!-- [![GitHub (pre-)release](https://img.shields.io/github/release/iacchus/birdears/all.svg?style=flat-square)](https://github.com/iacchus/birdears/releases) -->
<!-- [![Travis Build Status](https://img.shields.io/travis/iacchus/birdears.svg?style=flat-square&label=build)](https://travis-ci.org/iacchus/birdears) -->
<!-- [![Coveralls](https://img.shields.io/coveralls/birdears/birdears.svg?style=flat-square&label=coverage)](https://coveralls.io/github/birdears/birdears) -->
<!-- [![Awesome Sheet Music](https://img.shields.io/badge/awesome-sheet%20music-blue.svg?style=flat-square&logoWidth=14;&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA%2FwD%2FAP%2BgvaeTAAAACXBIWXMAAD2EAAA9hAHVrK90AAAAB3RJTUUH4QYVEQ4dGSq4mgAAAuVJREFUKM8FwUtoHGUAB%2FD%2F983s7CSb7s6%2BsrtJtqbEJA21llgQi4VaCL5QRKXQg6JXEUTqrfQi9CTozYPeUgrtxceh1kbEEEtBeslzTbdrup109r2zMzvZ2Xl8s9%2F4%2B5Hvfg4vOGpzqJf3aCpY%2FfTMi5OvE%2B6mdx%2Fud0YjP5PNxpiuh6X9%2F3I%2F6mzcScvT%2BvjYCUucknhkYSnvNYTvr5169YNLCEMAHKfPvZxwrBZaqoaGWn%2BNBNWlJ4dzn3147n2totckelwZhdr%2B9U%2FOvnnx0kRSgTJdhOBpIPYzSMyE7DaQJEcoFOO5lFK%2BeszcjxblGU%2BUzHosO5%2B6Ek2kQUYuupt3cXxxEoTIYN0WFDGHNnGwvVFGLJ1eXqv%2B8dzJPK%2FRhvbLKwtnzoI7BvyBjqBzCGEiC5ougAgCCJUAymHZPuYWc8J27cGV3c76jOgM9FlwjpE7APMZAscHH%2FYQsBgAhqBvYCyeREgRbm%2FV3aXixLwf6DFxqpCIDpqPQMQIjNoTBLaN9uYO7v30T9h72sHlL1fIV1%2Bvh0mBsp16na6czmUuJM5XaM%2Fo5UEp9JqGeGEO7tBHfGYW73x8kay8%2FTwRvADL02PIClw6shkxbd8sxl%2Fo0yghVl%2FvIyoL0DY30G8ZcKt7kDnDVDGHQbOFNAFZzlC4ozDiub6SofGAWsNIZWh10X7WwtODNsyeh15ZhfVYw6M%2Ft9Do%2B1jdMsPAC%2BEEHCyAy5WCT5VE%2FqDyr4rh0IZlu%2BygZg%2FdaAw2O0KTUWh%2FVXBe4kT1KVgIeAPh1rHxJBdufHsnKJXvXK7slIV61SodNI7iswVRDgnB%2FEuz8IiDvs1xs2yH1Q099oaZfyj5lkRVf4Ta4%2B69vuF6ajeodkRJ2tzroVRq4%2F5v2xiTFahd115ITn5eu23L5on3mBn5O0UNTxB2m%2FIDdZD5hiUW7qcyhd%2B%2F%2BHUNc2%2B9i8OBwFfXDo11Hfjho2t3I4tRIRoYNBAV738fRoHSSCa2GwAAAABJRU5ErkJggg%3D%3D)](https://iacchus.github.io/awesome-sheet-music/) -->

<!-- [![GitHub (pre-)release](https://img.shields.io/github/release/iacchus/birdears/all.svg?style=flat-square)](https://github.com/iacchus/birdears/releases) -->
<!-- [![PyPI Python Versions](https://img.shields.io/pypi/pyversions/birdears.svg?style=flat-square)](https://pypi.python.org/pypi/birdears) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/birdears/birdears/refs/heads/master/birdears-logo.png" width="256px" height="256px" />
</div>

**birdears** is a functional ear training tool for musicians. It helps you develop your musical ear by teaching you to recognize notes by their function within a key, rather than just by interval distance.

Inspired by the [Functional Ear Trainer](https://play.google.com/store/apps/details?id=com.kaizen9.fet.android) method, `birdears` is designed to build a strong internal sense of tonality, essential for transcription, improvisation, and composition.

---

https://github.com/user-attachments/assets/9743b9d3-e138-49fd-8862-a79537873a81

### chromatic, progression I-IV-V-I

[Screen_Recording_20260213_083515_Termux.webm](https://github.com/user-attachments/assets/7dfd2438-26a5-4262-91d7-0812c85bb00f)

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
