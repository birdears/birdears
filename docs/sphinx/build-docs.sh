#!/usr/bin/env bash

make clean

make html

make text

#make latex
#cd _build/latex
#xelatex birdears.tex

make latexpdf

git add .
git commit -a -m 'auto commit from docs/sphinx/build-docs.sh'
git push
