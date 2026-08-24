# Guntamatic Biostar (BS controller) fault messages

The tables below are the fault message texts ("Störmeldungen") from the
official Guntamatic Biostar operating manuals for the BS controller,
chapter 10/11.

They are display texts only: the web API fields `Störung 1/2` /
`Interuption 1/2` — mapped by this library to `interruption_1` /
`interruption_2` — are believed to carry similar text, but this is **not**
yet verified against a live fault capture. The API field contents are
localized free text following the language set on the heater, which is why
they cannot be enumerated as enum options.

## Source manuals

| Language | Manual | Source |
|----------|--------|--------|
| German | BA_BS_DE-B30-003-V26-0526 | guntamatic.com |
| English | BA_BS_EN-B30-003-V22-0422 | guntamatic.com |
| French | BA_BS_FR-B30-003-V22-0422 | guntamatic.com |
| Italian | BA_BS_IT-B30-003-V17-0412 (2012) | guntamatic.com |
| Czech | distributor translation of V16-0411 (2011) | guntamatic.esel.cz |

## Fault message table

Message texts are reproduced verbatim from the manuals, including typos.
Missing entries are marked with `—`.

| Code | German | English | French | Italian (2012) | Czech (2011) |
|------|--------|---------|--------|----------------|--------------|
| F01 | Aschelade offen (F01) | Firebox door or ash box open (F01) | Cendrier ouvert (F01) | Porta cassetto ceneri aperto (F01) | Otevřený popelník (F01) |
| F02 | Kipprost kann Position nicht erreichen Rostkontrolle (F02) | Clipgrate could´nt reach gratecontroll (F02) | La grille basculante ne peut pas atteindre la position - Contrôle de la grille (F02) | La griglia non riesce a raggiungere la posizione Controllo griglia (F02) | Sklopný rošt nemůže dosáhnout polohy Kontrola roštu (F02) |
| F03 | Lambdasondenwert im Start zu hoch Lambdasondentest (F03) | Lambdasondenvalue in the Start to high Lambdasondtest! (F03) | Valeur de la sonde lambda au démarrage trop élevée - Test de la sonde lambda (F03) | — | — |
| F04 | Kesseltemperatur zu hoch! Kaminzug und Kesselfühler prüfen! (F04) | Boiler temperature too high. Check flue draught and boiler sensor. (F04) | Température de la chaudière trop élevée ! Contrôler le tirage de la cheminée ou la sonde de chaudière ! (F04) | Temperatura caldaia troppo alta! Controllare tiraggio camino e caldaia! (F04) | Teplota kotle moc vysoká! Zkontrolovat komínový tah a kotel! (F04) |
| F05 | Verbrennungsstörung, Rost, Fallschacht und Pellets kontrollieren (F05) | burningfail fuel, grate, sir slider Controll (F05) | Contrôler le défaut de combustion, la grille, la rampe d'alimentation et les granulés (F05) | (left in German:) Verbrennungsstörung, Rost, Fallschacht und Pellets kontr. (F05) | Porucha spalování Zkontrolovat rošt, propadávací šachtu a pelety (F05) |
| F06 | Brennraum Überfüllung Rost, Fallschacht und Pellets kontrollieren (F06) | burning chamber, rust, drophole, hackchips controll! (F06) | Remplissage de la chambre de combustion, contrôler la grille, la rampe d'alimentation et les granulés (F06) | Camera di combustione troppo carica, controllare griglia condotto di carico e pellets. (F06) | Přeplnění ohniště Zkontrolovat rošt, propadávací šachtu a pelety (F06) |
| F07 | Zündung nicht möglich Rost u. Pellestvorrat kontrollieren (F07) | Ignition not possible. Check fuel and grate (F07) | Allumage impossible - Contrôler la grille et le silo de granulés (F07) | Accensione impossibile Controllare griglia e presenza pellets (F07) | Nelze zapálit Zkontrolovat rošt a zásobu paliva (F07) |
| F08 | Füllstandsensor reagiert nicht! (F08) | Filler levels doesn´t react (F08) | Le capteur de niveau ne réagit pas ! (F08) | Il sensore di carica non reagisce! (F08) | Čidlo stavu naplnění nereaguje! (F08) |
| F09 | — | — | — | Livello sotto (F09) | Pokles zásoby paliva pod minimální stav! Doplnit pelety! (F09) |
| F12 | Getriebemotor G1 blockiert (F12) | Drive motor G1 jammed (F12) | Motoréducteur G1 bloqué (F12) | Motore G1 bloccato! (F12) | Převodov.motor G1 blokován! (F12) |
| F16 | Achtung Übertemperatur STB gefallen (F16) | Warning STL high-temperature limiter tripped (F16) | Attention surchauffe STB déclenché (F16) | Attenzione STB attivato per sovratemperatura (F16) | Pozor přehřátí BT vypadl (F16) |
| F19 | Lambdasondenwert über den Grenzen! Kontrolle (F19) | lambda sond readings above limits. Test oxygen sensor (F19) | Valeur sonde lambda au-delà des limites ! Contrôle (F19) | Valori sonda lambda oltre i limiti! Controllare (F19) | Hodnota sondy lambda překročena! Kontrola (F19) |
| F20 | — | — | — | Contenitore ceneri pieno o pulizia automatica Bloccata (F20) | Popelník plný nebo automat. čištění blokováno (F20) |
| F21 | Rauchgasstörung durch Lambda Stop Lambdasondentest! (F21) | Oxygen sensor pause timeout. Test oxygen sensor. (F21) | Défaut gaz de fumées due à l'arrêt lambda - Test sonde lambda ! (F21) | Disturbo gas di scarico - Test sonda lambda! (F21) | Porucha spalin vlivem Lambdastop Test sondy lambda! (F21) |
| F22 | Füllstand nicht erreicht! Sauganlage kontrollieren (F22) | Fill level not reached.Check vacuum system (F22) | Niveau de remplissage pas atteint ! Contrôler l'installation d'aspiration (F22) | Riempimento non avvenuto! Controllare impianto di aspirazione (F22) | Naplnění nebylo dosaženo! Zkontrolovat PDP (F22) |
| F23 | Aschebehälter entleeren (F23) | Empty ash box (F23) | Vider cendrier (F23) | Svuotare il cassetto ceneri (F23) | Popelník vysypat (F23) |
| F40 | Saugzug (F40) | Saugzug (F40) (untranslated in the English manual) | Tirage (F40) | — | — |
| F44 | Fotosensorwert im Start zu tief (F44–Fotosensor prüfen) | Photo sensor reading too low at takeoff (F44–Check photo sensor) | Valeur de la cellule photoélectrique au démarrage trop basse (F44) | — | — |

## Notes

- F03/F40/F44 only exist in the newer manuals (DE V26 / EN V22 / FR V22).
- F09/F20 only appear in the older IT 2012 / CS 2011 manuals.
- The official English manual contains rough translations; the sic examples
  above ("Clipgrate could´nt reach gratecontroll", "burningfail fuel, grate,
  sir slider Controll") are preserved intentionally.
- The Italian and Czech columns come from older distributor translations and
  leave some cells in German.
