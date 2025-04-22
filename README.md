# Galleri nettside
 
- Denne prosjektet er et slags bilde galleri, hvor den har et innloggingssystem for å kunne se innholdet. 
Når man kommer inn i landings siden, så må man enten logge inn eller registrere en bruker dersom man er ny. 
Når du kommer inn i hovedsiden, ser du bilder med litt undertekst. Dersom du er ferdig med å se på bildene, så kan du logge ut og evt logge inn på nytt hvis du vil se bildene på nytt.

- Målgruppen for nettsiden er jo folk som fotografere og kunstnere, sånn hvis de trenger å vise frem bilde/kunsten sin på en enkel nettside.
Jeg har brukt Flask, MariaDB (VM) og Docker for dennne prosjektet. Nedenfor forklarer jeg hvorfor jeg bruker disse verktøyene.

## Flask

Jeg bruker Flask fordi:
- Siden prosjektet mitt er en nettside, så er det en python fil som kjører meste parten av en kode.
- Jeg kan kjøre nettsiden med database
- Jeg kan være sikker på at logg inn og registrerings fungerer, fordi uten database vil det ikke fungere.

## MariaDB (VM)
Jeg bruker MariaDB (VM) fordi:
- Jeg trenger det for logge inn og registrerings siden
- Kan lagre nødvendig data for å kunne bruke nettsiden
- 

## Docker
