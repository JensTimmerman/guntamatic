# Heater parameter definitions per language

These files are dumps of the heater's internal parameter definitions
(`++Parameterdaten++` export), captured in every UI language supported by the
heater. Each line describes one parameter:

```
SYN_NAME;type;...;Label;OPTION1;OPTION2;...
```

The trailing fields enumerate the allowed values for enum parameters, which is
what `TRANSLATE_HC_PROGRAM` and `TRANSLATE_PUMP_MODE` in `guntamatic/heater.py`
are built from.

Files are encoded in Windows-1252 (`cp1252`), like all heater web responses.

| File | Language |
|------|----------|
| `par_en.cgi` | English |
| `par_es.cgi` | Spanish |
| `par_de.cgi` | German |
| `par_fr.cgi` | French |
| `par_it.cgi` | Italian |
| `par_cs.cgi` | Czech |
| `par_sl.cgi` | Slovenian |
| `par_hu.cgi` | Hungarian |
| `par_nl.cgi` | Dutch |

Captured from a Biostar running firmware V3.2a (serial 959103).
