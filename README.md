# API für den Stundenplan OTH. 
Liest Json-Dateien von https://github.com/ruebe5w/StundenplanOTHParser ein und gibt .ics Kalenderdateien per REST-API zurück

Die API funktioniert folgendermaßen: 
https://<ip-adresse>/api/ ist die Adresse, alle weiteren Pfade sind hinter api/

## timetable
/timetable/<str:timetable_name> kannst du .ics Dateien zu allen Stundenplänen der Fakultät EMI mit dem Studiengangkürzel+Semester abfragen (also z.B. https://<ip-adresse>/api/timetable/EDU oder http://178.254.35.250/api/timetable/MI%203). Leerzeichen musst du leider durch %20 ersetzen, also eigentlich MI 3, aber in der URL dann halt MI%203.

## module
Das gleiche geht auch mit Modulen:
/modules/<str:module_names>  Ja, Mehrzahl, du kannst entweder ein Modul, oder beliebig viele mit + Zeichen Verknüpft dahinter hängen. Z.B. 
https://<ip-adresse>/api/modules/GDS+INTT
Das geht auch Studiengangsübergreifend. Was passiert, wenn Module im mehren Stundenplänen gleich heißen? Keine Ahnung, das habe ich bisher ignoriert.

## list
Und dann gibt es noch /list
mit /list/courses (Listet alle verfügbaren Studiengänge)
/list/timetables/<str:course_name> (Listet alle Stundenpläne für den Studiengang, für MI wäre das MI 1, MI 3 und MI 7, für EDU nur EDU, weil es da nur einen Stundenplan gibt, der genauso heißt)
Und natürlich /list/modules/<str:timetable_name> (Listet alle Module eines Stundenplans, also z.B. list/modules/MI%207 listet alle Module vom Stundenplan MI 7)

Achso, falls du die Kalenderdateien anguckst, die Termine liegen alle in der ersten Januarwoche 2024. Auch noch so ein Ding, was ich ändern muss😅🙈
