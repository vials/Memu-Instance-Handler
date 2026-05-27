***MEmu Instance Handler***

Written in python3, as a fun project... Manage, control and automate MEmu instances + OCR! 
This project supports grabbing strings from UI hierchary along with OCR for a wider support to automate tasks.
Some apps dont allow dumping strings from the display, so thats where OCR comes into play. This allows for users
to pull strings by taking screenshots, turning the pictures to black and white and with a little tweaking of 
tesseract params... grab strings from the active regions of the screen. With the OCR support, you can limit
regions, include other language packs, and filter out undesired background noise to grab the text only.

This project has been used to automate many tasks and has been tested on many platforms to ensure functionality.
Granted, I have never tested against italicized fonts, this should work on many basic android fonts that even 
your grandparents can read.

I will add an example script and update this repo in the upcoming days.


Downloads:

MEmu Download
https://www.memuplay.com/

Tesseract Download:
https://github.com/UB-Mannheim/tesseract/wiki
