# Projekt II — Gra w oszusta

## Opis

Projekt polega na napisaniu skryptu gracza w języku Python dla gry "Oszust". Jest to gra sekwencyjna, w której gracze
mają do wyboru dwie strategie: oszukać lub nie oszukać oraz sprawdzić lub nie sprawdzić. Celem gry jest pozbycie się
wszystkich kart z ręki.

Gracze otrzymują po 8 kart na początku gry i na przemian wykonują ruchy. Każdy gracz musi położyć na stosie kartę tej
samej wysokości lub wyższej niż górna karta ze stosu, jeśli nie zamierza oszukać, lub położyć jakąkolwiek kartę, jeśli
zamierza oszukać. Gracz może także zrezygnować z kładzenia karty na rzecz pobrania 3 kart ze stosu.

Jeśli gracz oszukał, a przeciwnik sprawdził, to bierze 3 karty ze stosu. Jeśli gracz nie oszukał, a przeciwnik
sprawdził, to przeciwnik zabiera 3 karty z góry stosu.

## Przestrzeń akcji

Przestrzeń akcji gracza składa się z 4 akcji:

* `play_card(card)` — położenie karty na stosie
* `take_cards(n)` — zabranie `n` kart ze stosu
* `cheat()` — oszustwo
* `check()` — sprawdzenie

## Ocenianie

Projekt zostanie oceniony na podstawie jakości kodu i strategii gracza. Kod powinien być czytelny i zgodny z konwencjami
języka Python. Strategia gracza powinna być możliwie jak najlepsza, a wynik powinien być jak najbliższy maksymalnej
możliwej liczbie punktów.

## Sposób gry

Gracze otrzymują po 8 kart na początku gry.
Gracze wykonują ruchy na przemian.
Każdy gracz musi położyć na stosie kartę tej samej wysokości lub wyższej niż górna karta ze stosu, jeśli nie zamierza
oszukać, lub położyć jakąkolwiek kartę, jeśli zamierza oszukać.
Gracz może także zrezygnować z kładzenia karty na rzecz pobrania 3 kart ze stosu.
Jeśli gracz oszukał, a przeciwnik sprawdził, to bierze 3 karty ze stosu. Jeśli gracz nie oszukał, a przeciwnik
sprawdził, to przeciwnik zabiera 3 karty z góry stosu.
Gra kończy się, gdy któryś z graczy pozbędzie się wszystkich kart z ręki.
