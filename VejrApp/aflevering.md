# Aflevering – din egen luftkvalitets-app

Her står alt, hvad du skal lave og aflevere i projektet: opgaverne, kravene til hvert projekttrin og kravene til den endelige aflevering. Undervisningsmaterialet med gennemgang og øvelser står i [readme.md](readme.md).

Projektet består af seks projekttrin. Hvert trin har en liste med krav. Trinnet er færdigt, når du kan sætte hak ved alle krav, og du har lavet et commit i dit GitHub-repository.

Lav et commit efter hvert trin med en besked som `Trin 2: data fra API`. Så kan både du og din lærer se, hvordan appen har udviklet sig.

| Projekttrin | Hører til |
|---|---|
| [Trin 1: App med kunstige data](#trin-1-app-med-kunstige-data) | [Modul 1: NiceGUI basis](readme.md#modul-1-nicegui-basis) |
| [Trin 2: Rigtige data](#trin-2-rigtige-data) | [Modul 2, del 1: Data fra et API](readme.md#del-1-data-fra-et-api) |
| [Trin 3: State og valg](#trin-3-state-og-valg) | [Modul 2, del 2: State, binding og events](readme.md#del-2-state-binding-og-events) |
| [Trin 4: En robust app](#trin-4-en-robust-app) | [Modul 2, del 3: Refresh og fejlhåndtering](readme.md#del-3-refresh-og-fejlhåndtering) |
| [Trin 5: Pakke og flere sider](#trin-5-pakke-og-flere-sider) | [Modul 3: Pakker og navigation](readme.md#modul-3-pakker-og-navigation) |
| [Trin 6: Appen gemmer brugerens valg](#trin-6-appen-gemmer-brugerens-valg) | [Modul 4: Udvidelse](readme.md#modul-4-udvidelse) |
| [Den endelige aflevering](#den-endelige-aflevering) | Hele forløbet |

---

## Trin 1: App med kunstige data

Hører til [Modul 1: NiceGUI basis](readme.md#modul-1-nicegui-basis).

I første version bruger du kunstige data. Du skal altså endnu ikke hente data fra internettet.

### Startdata

Opret en ny mappe til dit projekt og en fil `main.py`. Start med denne funktion:

```python
def make_co2_table() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "time": ["08:00", "10:00", "12:00", "14:00", "16:00"],
            "carbon_dioxide": [421.2, 422.5, 424.1, 423.6, 422.8],
        }
    )
```

CO₂-koncentrationen angives i enheden ppm, som betyder "parts per million".

### Opgave 1: Vis appens titel

Opret følgende elementer:

- en overskrift med teksten `CO₂ Forecast App` (https://nicegui.io/documentation/label)
- en mindre tekst med teksten `Model data for Copenhagen`
- en knap med teksten `Show CO₂` (https://nicegui.io/documentation/button)

### Opgave 2: Fremstil en graf

Skriv funktionen:

```python
def make_co2_plot(df: pd.DataFrame):
    ...
```

Funktionen skal returnere et plot med:

- `time` på x-aksen
- `carbon_dioxide` på y-aksen
- markører på datapunkterne
- titlen `CO₂ forecast`
- akseteksten `CO₂ (ppm)` på y-aksen

https://plotly.com/python/plotly-express/

### Opgave 3: Vis grafen i NiceGUI

Brug `ui.plotly()` til at vise figuren i appen. Grafen skal fylde hele den tilgængelige bredde. Det kan gøres med `.classes("w-full")`.

https://nicegui.io/documentation/plotly

### Opgave 4: Tilføj interaktion

Skriv en callback-funktion med navnet:

```python
def update_plot() -> None:
    ...
```

Når brugeren trykker på knappen, skal funktionen:

1. fremstille en ny Plotly-figur
2. gemme figuren i plotkomponenten
3. kalde `plot.update()`

Forbind derefter knappen med funktionen ved hjælp af `on_click`.

### Opgave 5: Vis en besked

Når grafen bliver opdateret, skal appen vise en kort besked:

```python
ui.notify("CO₂ forecast updated")
```

### Opgave 6: Tilføj luftkvalitet

Tilføj en dataserie med et luftkvalitetsindeks (AQI) til din DataFrame:

```python
"european_aqi": [37, 41, 45, 43, 38]
```

Tilføj to knapper, `CO₂` og `AQI`. Når brugeren trykker på en knap, skal grafen vise den valgte parameter med den rigtige titel og aksetekst.

Overvej, hvordan `make_co2_plot()` kan ændres, så den modtager navnet på den valgte parameter som argument.

### Krav til trin 1

- [ ] Appen har en overskrift og en undertekst.
- [ ] Data ligger i en DataFrame, som en funktion returnerer.
- [ ] Appen viser en Plotly-graf i fuld bredde.
- [ ] Der er mindst to knapper, som skifter mellem CO₂ og AQI.
- [ ] Grafen opdateres af en callback-funktion.
- [ ] Appen viser en besked med `ui.notify`, når grafen opdateres.
- [ ] Layoutet bruger mindst én `ui.row` eller `ui.card`.

---

## Trin 2: Rigtige data

Hører til [Modul 2, del 1: Data fra et API](readme.md#del-1-data-fra-et-api).

Nu skal din app vise rigtige data. Brug Open-Meteos Air Quality API:

- Adresse: `https://air-quality-api.open-meteo.com/v1/air-quality`
- Dokumentation: https://open-meteo.com/en/docs/air-quality-api
- Parametre, du skal bruge under `hourly`: `carbon_dioxide` og `european_aqi`

### Krav til trin 2

- [ ] Projektet har en fil `model.py` med en funktion `fetch_air_quality(latitude, longitude)`, som returnerer en DataFrame.
- [ ] DataFramen har kolonnerne `date`, `carbon_dioxide` og `european_aqi`, og `date` er en rigtig dato-kolonne.
- [ ] `model.py` indeholder ingen NiceGUI-kode og kan køres alene med `python model.py`, så de første rækker udskrives.
- [ ] Projektet har en fil `options.py` med en dictionary `STATIONS` med mindst tre byer og deres koordinater.
- [ ] Appen fra trin 1 viser nu de hentede data i stedet for de kunstige.

**Vis din makker:** et kald af `fetch_air_quality()` uden NiceGUI og de første rækker af resultatet.

---

## Trin 3: State og valg

Hører til [Modul 2, del 2: State, binding og events](readme.md#del-2-state-binding-og-events).

### Krav til trin 3

- [ ] Projektet har en fil `viewmodel.py` med en dataclass til state og en ViewModel-klasse.
- [ ] State indeholder som minimum valgt by, valgt parameter og de hentede data.
- [ ] ViewModel har en metode, der henter data gennem `fetch_air_quality()` og lægger dem i state.
- [ ] `viewmodel.py` indeholder ingen NiceGUI-kode.
- [ ] Projektet har en fil `view.py`, som opretter alle UI-elementer.
- [ ] Brugeren kan vælge by i et `ui.select`, som er bundet til state.
- [ ] Brugeren kan vælge mellem CO₂ og AQI, og valget er bundet til state.
- [ ] Der er ingen globale variable, der gemmer den samme oplysning som state.
- [ ] Grafens titel og enhed passer til den valgte parameter.

**Undersøg:** Kræver et skift mellem CO₂ og AQI en ny forespørgsel, eller er data allerede hentet?

---

## Trin 4: En robust app

Hører til [Modul 2, del 3: Refresh og fejlhåndtering](readme.md#del-3-refresh-og-fejlhåndtering).

### Krav til trin 4

- [ ] Grafen ligger i en `@ui.refreshable` funktion, som læser fra state.
- [ ] Appen viser også en tabel i en `@ui.refreshable` funktion. Tabellen formaterer en kopi af data.
- [ ] Når brugeren skifter by eller parameter, opdateres både graf og tabel.
- [ ] State har et felt `error_message`.
- [ ] `model.py` bruger `raise_for_status()` og `timeout`, og den rejser en fejl med en klar besked, hvis svaret ikke indeholder data.
- [ ] ViewModel fanger fejl med `try`/`except` og skriver en besked til brugeren i state.
- [ ] View viser beskeden i stedet for grafen, når der er en fejl, og en anden besked, når der ingen data er.
- [ ] Efter en fejl kan appen hente data igen uden at blive genstartet.
- [ ] Gamle data bliver ikke vist som data for et nyt valg.

**Test din app:** Simulér en fejl som i øvelse 2.14 i [readme.md](readme.md#øvelser-til-del-3), og sluk for netværket på din computer. Viser appen en forståelig besked begge gange?

**Ekstra:** Tilføj feltet `is_loading` til state, og vis en `ui.spinner()`, mens data hentes. Bind spinnerens synlighed til state med `bind_visibility_from`. Du får brug for `run.io_bound`, så appen ikke fryser, mens den venter: https://nicegui.io/documentation/section_action_events#running_i_o-bound_tasks

---

## Trin 5: Pakke og flere sider

Hører til [Modul 3: Pakker og navigation](readme.md#modul-3-pakker-og-navigation).

Trinnet har to dele. Lav et commit efter hver del.

### Del A: Lav din app om til en pakke

Appen skal kunne præcis det samme som efter trin 4, men koden skal ligge i en pakke.

1. Opret en mappe `src` og i den en pakke med et navn, du selv vælger, for eksempel `air_app`. Navnet skal skrives med små bogstaver og uden mellemrum og bindestreger.
2. Opret underpakkerne `models` og `views`.
3. Flyt dine filer:

   | Fra trin 4 | Til pakken |
   |---|---|
   | `options.py` | `models/models.py` |
   | `model.py` | `models/services.py` |
   | `viewmodel.py` | `views/forecast_viewmodel.py` |
   | `view.py` | `views/forecast.py` |

4. Ret alle importer, så de starter med pakkens navn.
5. Flyt `ui.run()` fra dit View til en ny `main.py`, og sæt den under `if __name__ == "__main__":`.
6. Start appen fra `src` med `python -m <dit_pakkenavn>.main`.

### Krav til del A

- [ ] Projektet har strukturen `src/<pakkenavn>/` med `main.py`, `models/` og `views/`.
- [ ] Hver pakke har en `__init__.py`.
- [ ] Alle importer mellem dine egne filer er absolutte og starter med pakkens navn.
- [ ] Ingen fil i `models` importerer fra `views` eller fra `nicegui`.
- [ ] Ingen ViewModel importerer `nicegui`.
- [ ] `ui.run()` står kun i `main.py` og kun under `if __name__ == "__main__":`.
- [ ] Appen startes med `python -m <pakkenavn>.main` og virker som efter trin 4.

### Del B: Flere sider

Din app skal nu have mindst to sider. Den første er den, du allerede har bygget. Den anden skal vise historiske data: Air Quality API'et kan levere data bagud i tid med parameteren `past_days` (op til 92 dage).

### Krav til del B

- [ ] `main.py` har en `root()` med en header med appens navn og en menu med links.
- [ ] Appen har en prognoseside med funktionerne fra trin 4.
- [ ] Appen har en historikside, hvor brugeren kan vælge, hvor mange dage tilbage grafen skal vise.
- [ ] Hver side har sit eget View-modul og sit eget ViewModel-modul i pakken `views`.
- [ ] De to sider bruger det samme modellag. API-adressen står kun ét sted i projektet.
- [ ] Historiksiden håndterer fejl på samme måde som prognosesiden.

**Ekstra:** Tilføj en tredje side, der sammenligner to byer i samme graf.

---

## Trin 6: Appen gemmer brugerens valg

Hører til [Modul 4: Udvidelse](readme.md#modul-4-udvidelse).

### Krav til trin 6

- [ ] Appen husker den senest valgte by og parameter, når siden genindlæses, og når appen genstartes.
- [ ] Brugeren kan gemme en by som favorit og fjerne den igen.
- [ ] Favoritterne vises i appen, og et klik på en favorit vælger byen.
- [ ] Al læsning og skrivning af gemte data ligger i en repository-klasse i modellaget.
- [ ] Hverken View eller ViewModel bruger `app.storage` direkte.
- [ ] `.nicegui` står i `.gitignore`.

**Ekstra:** Lad brugeren skrive navnet på en vilkårlig dansk by i stedet for at vælge fra en fast liste. Brug Open-Meteos geocoding API til at finde koordinaterne, ligesom `fetch_coordinates()` i lærerens `model.py`, og vis en fejlbesked, hvis byen ikke findes.

---

## Den endelige aflevering

Projektet afleveres som et GitHub-repository. Det skal indeholde:

- **Koden** til din app, organiseret efter MVVM som i trin 5.
- **En `readme.md`**, der forklarer, hvad din app kan, hvordan man installerer og starter den, og hvilke features den har. Indsæt gerne et skærmbillede.
- **En kort refleksion** (ca. en side) i din readme, hvor du:
  - tegner eller beskriver, hvordan et byskift rejser gennem View, ViewModel og Model i din app
  - forklarer, hvor din apps single source of truth ligger, og giver et eksempel på, hvad der kunne gå galt uden
  - forklarer, hvordan din app håndterer en fejl, og hvilket lag der gør hvad
  - begrunder dine valg af UI-elementer
  - beskriver én ting, du ville lave anderledes, hvis du skulle starte forfra
- **En commit-historik**, der viser, at appen er bygget trin for trin.

Tjekliste før aflevering:

- [ ] Alle krav i trin 1-6 er opfyldt.
- [ ] Appen kan startes efter anvisningen i din readme på en anden computer.
- [ ] Der står ingen `ui.` i modellaget eller i dine ViewModels.
- [ ] Der er ingen adgangskoder eller API-nøgler i dit repository.
