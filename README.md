# BirdEars 

[![Build Status](https://travis-ci.org/iacchus/birdears.svg?branch=master)](https://travis-ci.org/iacchus/birdears) 
[![Coverage Status](https://coveralls.io/repos/github/iacchus/birdears/badge.svg)](https://coveralls.io/github/iacchus/birdears)


## Functional Ear Training for Musicians

In current development though functional

## Usage 

### 1. Install the Dependencies

Install `sox` and `python3` (see [below](https://github.com/iacchus/birdears#installing--dependencies)) and, 

### 2. clone the repository 

```
git clone https://github.com/iacchus/birdears.git
```

### 3. and just run the script:

```
python3 birdears.py
```

#### or

```
chmod +x birdears.py
./birdears.py
```

## Keybindings for intervals

**MAJOR keyboard keys** (with *chromatics*)

Key Index for major and chromatic major context


```
  keyboard              would represent

 s d   g h j        IIb  IIIb       Vb VIb  VIIb
z x c v b n m  <-  I   II   III  IV   V   VI   VII
```

*(**SHIFT** key meaning an octave higher)*

**MINOR keyboard keys** (with *chromatics*)

Key index for minor and chromatic minor context

```
   keyboard                 would represent
                           in chromatics in
                            'a' minor context

 s   f g   j k   eg.:      a#   c# d#    f# g#
z x c v b n m    -------  a  b c  d  e  f  g
```

### Screenshot or didn't happen

*(development version)* 

![birsears screenshot](https://i.imgur.com/PSZCL2a.png)

### Other keys

**q** to quit.

**r** to repeat the tonic/interval.

## Installing  Dependencies

Submit your distro's too..

### Arch Linux

```
sudo pacman -S python sox
```
