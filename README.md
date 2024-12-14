# Detector de curgere a cafelei în moka pot

## Descriere

Prietenul meu își face cafea la moka pot. După ce pune moka potul pe foc,
pleacă din bucătărie și începe să facă altceva până începe cafeaua să curgă.
Nu îl avertizează nimic atunci când curge cafeaua, iar el uită că a pus
cafeaua pe foc. Așa că în multe dimineți fuge disperat de la birou în bucătărie
ca să oprească focul. În multe dimineți face cafeaua de două ori. Proiectul
acesta ar presupune instalarea unui senzor în/lângă moka pot pentru a detecta
momentul în care începe să curgă cafeaua și a îl notifica pe prietenul meu.
Va primi o notificare pe laptop/telefon și un semnal sonor. La fiecare utilizare
poate introduce informații despre momentul când a fost notificat
(prea devreme/prea târziu/la timp), astfel încât sistemul să se ajusteze în timp.

## Implementare (software)

- Server Flask (în `src`)
- Comunicare cu senzorii (în `sketches`)
