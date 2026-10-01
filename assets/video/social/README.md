# Clips aus den eigenen Kanaelen (@skiavelo)

Hier liegen die Web-Fassungen der Instagram- und TikTok-Clips, plus je ein Poster-JPG.

## Warum hier und nicht per Embed

Instagram- und TikTok-Embeds laden Skripte der Plattformen nach und senden IP und
Cookies an Meta bzw. ByteDance, bevor jemand zugestimmt hat. Die Seite kommt sonst
ohne einen einzigen externen Request aus - das soll so bleiben. Dieser Content
gehoert Saskia selbst, es gibt also keinen Grund, ihn fremd ausliefern zu lassen.

## Dateien hinzufuegen

1. Clips aus den eigenen Accounts exportieren
   (TikTok: Video speichern; Instagram: Einstellungen -> Deine Aktivitaeten ->
   Informationen herunterladen).
2. Nach `material/videos-social/` legen - dort, nicht hier: dieser Ordner
   enthaelt nur die fertigen Web-Fassungen.
3. Encoder laufen lassen (derselbe wie fuer die Projektvideos):
   max 720 breit, H.264, 30 fps, CRF 26, faststart, plus Poster bei Sekunde 1.
4. In `build.py` beim Beitrag eintragen:

   clips=[("hook-test", "Hook-Variante A, 3 Sekunden"),
          ("format-b",  "Was nicht funktioniert hat")]

   Der Dateiname ohne Endung, dazu die Bildunterschrift. Ohne Eintrag
   rendert der Block nichts.
