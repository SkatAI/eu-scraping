# Extracting content from EU parliament debates

content from pages like this one

https://www.europarl.europa.eu/doceo/document/TA-9-2023-0236_EN.html


2 scripts:

## extract_urls.py:

builds the url data in `data/extracted_links.csv`

Given
```python
BASE_URL = "https://www.europarl.europa.eu"
# Initial URL
# most recent available verbatims TOC at time of writing
start_url = "/doceo/document/CRE-10-2024-11-27-TOC_EN.html"
```
navigates the web sites and extract urls for previous pages more recent than '2024-01-01' (cf while in code)

## parse_debates.py

- reads the urls from `./data/extracted_links.csv`
- extracts and formats content into a debates.json file
- saves each page results into a data/tmp folder in case the script fails

# data

- ./data/extracted_links.csv: 1767 urls
- ./data/debates.json.zip and ./data/debates_1478.json.zip extrated content

## sample

```json
    {
        "parent": "\/doceo\/document\/CRE-10-2024-11-27-TOC_EN.html",
        "page_idx": 17,
        "page": "CRE-10-2024-11-27-ITM-003_EN.html",
        "title": "Verbatim report of proceedings - Presentation by the Commission President-elect of the College of Commissioners and its programme (debate) - Wednesday, 27 November 2024",
        "name": "Diana Riba i Giner",
        "party": "Verts\/ALE",
        "text": "Señoras presidentas, señoras comisarias, ¿era posible tener una Comisión sin la presencia de la extrema derecha? Ciertamente, probablemente, no lo era. Si hay Estados gobernados por la extrema derecha, sabemos que habrá comisarios de la extrema derecha. Pero lo que sí estaba en sus manos, presidenta von der Leyen, era decidir qué papel iban a jugar estos comisarios. Y, ante esta elección, usted ha decidido dar una vicepresidencia —con grandes responsabilidades— al enviado de Meloni, ni más ni menos que las políticas de cohesión que, a través de sus fondos, gestionan un tercio del presupuesto europeo. Y por ahí no podemos pasar. No podemos dar apoyo a lo que, a todas luces, implica la normalización de la extrema derecha.\nSabemos que, en su Comisión, hay personas que están tan incómodas como nosotros con esta decisión. A ellas les decimos que haremos una oposición constructiva y que siempre, siempre, nos encontrarán dispuestos a trabajar por una Europa de derechos y libertades. No son tiempos fáciles para la democracia, pero tampoco son tiempos para bajar los brazos.\n(La oradora se niega a que Stefano Cavedagna le formule una pregunta con arreglo al procedimiento de la «tarjeta azul»)"
    },

```

