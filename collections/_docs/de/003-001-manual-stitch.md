---
title: "Manuelle Stichplatzierung"
permalink: /de/docs/stitches/manual-stitch/
excerpt: ""
last_modified_at: 2023-01-16
toc: true
---
## Beschreibung
[![Manual Stitch Flowers](/assets/images/docs/manual-stitch.jpg){: width="200x"}](/assets/images/docs/manual-stitch.svg){: title="Download SVG File" .align-left download="manual-stitch.svg" }
Im manuellen Stichmodus stellt jeder Knoten des Pfades einen Nadeleinstich dar. So ist es möglich jeden Stich genau zu planen.

## Funktionsweise

1. Erstelle einen Pfad mit mehreren Knoten. Breite und Strichlinien-Einstellung haben keine Auswirkungen im manuellen Stichmodus.
2. Öffne `Erweiterungen > Ink/Stitch  > Parameter`.
3. Aktiviere `Manuelle Stichpositionierung`. Alle anderen Einstellungen wirken sich in diesem Modus nicht auf das Endergebnis aus.

   ![Params Stroke](/assets/images/docs/de/params-manual-stitch.jpg)

Jeder Knoten repräsentiert einen Nadeleinstich. Kurven werden dementsprechend nicht berechnet.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

Für eine genaue Planung macht es deshalb Sinn, schon beim Zeichnen Kurven direkt ganz zu vermeiden, oder den Pfad vor dem Sticken entsprechend zu bearbeiten:
1. Wähle alle Knotenpunkte an (`F2` dann `Ctrl`+`A`)
2. Klicke auf ![Die gewählten Knoten in Ecken umwandeln](/assets/images/docs/tool-controls-corner.jpg){: title="Die gewählten Knoten in Ecken umwandeln" } in der `Werkzeugeinstellungsleiste`.g

## Params

Einstellung|Beschreibung
---|---
Geradstich                            | Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Methode                               | Geradstich auswählen
Manuelle Stichpositionierung          | Aktiviert den **manuellen Stichmodus**
Wiederholungen                        | Diese Einstellung hat keine Auswirkung auf manuelle Stichpositionierung
Bean stitch Anzahl der Wiederholungen | Diese Einstellung hat keine Auswirkung auf manuelle Stichpositionierung
Stichlänge                            | Diese Einstellung hat keine Auswirkung auf manuelle Stichpositionierung
Zick-Zack Abstand (Spitze zu Spitze)  | Diese Einstellung hat keine Auswirkung auf manuelle Stichpositionierung
Vernähen erlauben                     | Diese Einstellung hat keine Auswirkung auf manuelle Stichpositionierung
Vernähen erzwingen                    | Diese Einstellung hat keine Auswirkung auf manuelle Stichpositionierung
Fadenschnitt                          | Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                                 | Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

## Tipps

### Faden vernähen

Im manuellen Modus muss auch das Vernähen von Hand angelegt werden. Wenn du den Faden vernähen willst, plane den Pfad entsprechend.

## Beispieldateien die den manuellen Stichmodus beinhalten
{: style="clear: both;" }
{% include tutorials/tutorial_list key="stichart" value="Manueller Stich" %}
