# VejrApp – webapps med NiceGUI og MVVM

I dette forløb lærer du at bygge en webapp i Python med NiceGUI, og du lærer at strukturere koden, så den er til at overskue, rette og udvide.

Forløbet varer 4-5 uger og er projektbaseret. Det betyder, at du bygger **din egen app** ved siden af undervisningen og forbedrer den trin for trin, hver gang du har lært noget nyt.

## Sådan arbejder vi

Hvert modul har de samme tre dele:

| Del | Hvad sker der? | Hvilken kode? |
|---|---|---|
| **Gennemgang** | Læreren viser nyt stof med små kodeeksempler | Vejrappen i `src/app_1`, `src/app_2` og `src/app_3` |
| **Øvelser** | Du afprøver det nye stof i små opgaver | Små filer, du selv opretter, eller vejrappen |
| **Projekt** | Du bygger videre på din egen app | Din egen luftkvalitets-app |

Vejrappen er altså lærerens eksempel. Du skal ikke kopiere den, men bruge den som opslagsværk, når du bygger din egen app.

## Oversigt over forløbet

| Uge | Modul | Nyt stof | Projekttrin |
|---|---|---|---|
| 1 | [Modul 1: NiceGUI basis](#modul-1-nicegui-basis) | UI-elementer, layout, callbacks, Plotly | [Trin 1: app med kunstige data](aflevering.md#trin-1-app-med-kunstige-data) |
| 2 | [Modul 2, del 1: Data fra et API](#del-1-data-fra-et-api) | HTTP, API, JSON, DataFrame, MVVM-lagene | [Trin 2: rigtige data](aflevering.md#trin-2-rigtige-data) |
| 2-3 | [Modul 2, del 2: State, binding og events](#del-2-state-binding-og-events) | `@dataclass`, single source of truth, ViewModel, `bind_value` | [Trin 3: state og valg](aflevering.md#trin-3-state-og-valg) |
| 3 | [Modul 2, del 3: Refresh og fejlhåndtering](#del-3-refresh-og-fejlhåndtering) | `@ui.refreshable`, `try`/`except`/`finally` | [Trin 4: robust app](aflevering.md#trin-4-en-robust-app) |
| 4 | [Modul 3: Pakker og navigation](#modul-3-pakker-og-navigation) | Moduler, pakker, import, flere sider, header, menu | [Trin 5: pakke og flere sider](aflevering.md#trin-5-pakke-og-flere-sider) |
| 5 | [Modul 4: Udvidelse](#modul-4-udvidelse) | NiceGUI storage, repository pattern | [Trin 6: appen gemmer brugerens valg](aflevering.md#trin-6-appen-gemmer-brugerens-valg) |

## Faglige mål og fokus

- redegøre for arkitekturen af programmer på forskellige abstraktionsniveauer, herunder relationen mellem brug og funktion
- rette, tilpasse og udvide avancerede programmer
- arbejde inkrementelt og systematisk i programmeringsprocessen.

## Fagligt indhold

- arkitekturen for programmers interaktion med omgivelserne med henblik på hændelsestyret interaktion og interaktion mellem systemer.

## Kom i gang

Vi bruger PyCharm som editor. Vejledningen gælder både Windows og Mac.


### Installer bibliotekerne

```text
python -m pip install nicegui pandas plotly requests openmeteo-requests requests-cache retry-requests
```

### Kør lærerens eksempler

**Modul 1 og 2** kan startes direkte i PyCharm. Højreklik på filen i projektoversigten, og vælg **Run**:

- Modul 1: `src/app_1/main.py`
- Modul 2: `src/app_2/view.py`

Appen åbner i browseren på `http://localhost:8080`. Stop den med den røde stopknap i PyCharm.

**Modul 3** er en pakke og skal startes fra mappen `src` i terminalen:

```text
cd src
python -m app_3.main
```

Stop appen ved at klikke i terminalen og trykke `Ctrl+C` (også på Mac). Skriv `cd ..` for at gå én mappe tilbage.

Du kan også starte et program fra terminalen i stedet for at højreklikke, for eksempel `python src/app_1/main.py`.


## Projektet: din egen luftkvalitets-app

Du skal bygge en app, der viser CO₂-koncentration og luftkvalitet (AQI) for danske byer. Data kommer fra Open-Meteos Air Quality API, som er gratis og ikke kræver en nøgle.

Når forløbet er slut, kan din app:

- vise en graf og en tabel med data hentet fra internettet
- lade brugeren vælge by og parameter
- vise en forståelig besked, når noget går galt
- have flere sider med en menu
- huske brugerens valg, også når appen genstartes

Du når dertil gennem seks projekttrin. Opgaverne, kravene til hvert trin og kravene til den endelige aflevering står samlet i [aflevering.md](aflevering.md).

---

## Modul 1: NiceGUI basis

**Mål:** Du kan bygge en lille app med tekst, knapper og en graf, og du kan forklare, hvad en callback-funktion er.

**Fagligt fokus:**

- **Brugerflade som kode:** UI-elementer og layout med `ui.row`, `ui.column` og `ui.card`
- **Hændelsesstyret programmering:** programmet venter på brugeren, og en callback-funktion bliver kaldt, når der sker noget
- **Visualisering:** fra data til graf med Plotly
- **Opdatering af brugerfladen:** en callback ændrer det, brugeren ser

**Lærerens eksempel:** `src/app_1/main.py`

### Din første app

En NiceGUI-app er et Python-program. Hver linje med `ui.` opretter et element på siden, og `ui.run()` starter appen.

```python
from nicegui import ui

ui.label("Weather App")
ui.button("Klik her")

ui.run()
```

Elementerne vises i den rækkefølge, de står i koden.

### Udseende med `.classes()`

Du ændrer et elements udseende ved at tilføje klasser. Klasserne adskilles med mellemrum.

```python
ui.label("Weather App").classes("text-2xl font-bold")
ui.label("Version 1").classes("text-gray-500")
```

### Layout med `with`

Layout-elementer som `ui.row`, `ui.column` og `ui.card` er beholdere. Alt, der er indrykket under `with`, havner inde i beholderen.

```python
with ui.row():
    ui.button("Temperature")
    ui.button("Rain")

with ui.card():
    ui.label("Dette står inde i et kort")
```

`ui.row` lægger elementerne ved siden af hinanden, og `ui.column` lægger dem under hinanden.

### Hændelser og callback-funktioner

En app venter på, at brugeren gør noget. Det kaldes en hændelse (event). En callback-funktion er en funktion, som NiceGUI kalder, når hændelsen sker.

```python
def say_hello() -> None:
    ui.notify("Hej!")

ui.button("Sig hej", on_click=say_hello)
```

Læg mærke til, at der står `say_hello` uden parenteser. Du giver funktionen til knappen, så den kan kaldes senere.

| Du skriver | Det betyder |
|---|---|
| `on_click=say_hello` | Kald funktionen, når brugeren klikker |
| `on_click=say_hello()` | Kald funktionen med det samme, mens siden bygges (forkert) |

Andre elementer har tilsvarende hændelser, for eksempel `ui.checkbox("Rain", on_change=update_plot)`.

### En graf med Plotly

Data ligger i en pandas DataFrame, Plotly laver figuren, og `ui.plotly` viser den i appen.

```python
import pandas as pd
import plotly.express as px
from nicegui import ui


def make_weather_table() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "day": ["Monday", "Tuesday", "Wednesday"],
            "temperature": [12, 14, 13],
            "rain": [0.0, 1.5, 0.2],
        }
    )


def make_plot(df: pd.DataFrame, column: str):
    return px.line(df, x="day", y=column, markers=True, title=column)


weather_data = make_weather_table()
plot = ui.plotly(make_plot(weather_data, "temperature")).classes("w-full")

ui.run()
```

### Opdater grafen fra en callback

En figur, der allerede er vist, ændrer sig ikke af sig selv. Du skal give plotkomponenten en ny figur og bede den om at opdatere.

```python
def show_rain() -> None:
    plot.figure = make_plot(weather_data, "rain")
    plot.update()
    ui.notify("Viser nedbør")

ui.button("Rain", on_click=show_rain)
```

### Øvelser til modul 1

**Øvelse 1.1 – Forudsig rækkefølgen.** Læs koden, og skriv ned, hvordan siden kommer til at se ud. Kør den derefter, og sammenlign.

```python
ui.label("A")
with ui.row():
    ui.label("B")
    with ui.column():
        ui.label("C")
        ui.label("D")
    ui.label("E")
```

**Øvelse 1.2 – Tæller.** Lav en app med en label, der viser `0`, og en knap. Hver gang brugeren klikker, skal tallet blive én større. Tip: en label har metoden `set_text()`.

**Øvelse 1.3 – Find fejlen.** Denne knap viser beskeden, før brugeren har klikket, og bagefter sker der ingenting. Forklar hvorfor, og ret koden.

```python
ui.button("Gem", on_click=ui.notify("Gemt"))
```

Tip: en lambda-funktion er en lille funktion uden navn, som skrives på én linje. `lambda: print("Hej")` kalder ikke `print` med det samme, men laver en funktion, der kan kaldes senere. Læs mere i [Pythons tutorial om lambda-udtryk](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions).

**Øvelse 1.4 – Læs lærerens kode.** Åbn `src/app_1/main.py`, og svar på spørgsmålene:

1. Hvilken funktion kører, når brugeren sætter hak i en checkbox?
2. Hvilke variable bruger `update_plot()`, som ikke er oprettet inde i funktionen?
3. Hvad sker der, hvis du fjerner linjen `plot.update()`?

### Projekt trin 1: CO₂ Forecast App med kunstige data

Opgaver og krav til trin 1 står i [aflevering.md](aflevering.md#trin-1-app-med-kunstige-data).

---

## Modul 2: API og MVVM-arkitektur

**Mål:** Du kan hente data fra et API, dele din kode op i Model, View og ViewModel, og du kan forklare, hvordan et valg i brugerfladen bliver til nye data på skærmen.

**Fagligt fokus:**

- **MVVM-arkitektur:** Model, View og ViewModel som tre lag med hver sin opgave
- **Adskillelse af ansvar (separation of concerns):** hvert stykke kode har ét ansvar, så en ændring ét sted ikke ødelægger noget et andet sted
- **Interaktion mellem systemer:** data fra et API med HTTP og JSON, og modellen som en funktion med en aftale
- **Single source of truth (SSOT):** hver oplysning har ét hjem i state, og alt andet beregnes ud fra den
- **State og binding:** state som `@dataclass`, og forskellen på binding og event-handler
- **Robusthed:** `@ui.refreshable` og fejlhåndtering med `try`/`except`/`finally`, hvor hvert lag har sin opgave ved fejl

**Lærerens eksempel:** `src/app_2/`

Modulet er delt i tre dele, og der hører et projekttrin til hver del.

### Hvorfor en arkitektur?

I `app_1` ligger alt i én fil: data, graf, knapper og callbacks. Det fungerer til 75 linjer. Men forestil dig, at appen også skal hente data fra internettet, håndtere fejl og have flere sider. Så bliver det svært at finde ud af, hvor en fejl kommer fra, og hvad der går i stykker, når du ændrer noget.

En arkitektur er en aftale om, hvor de forskellige slags kode skal ligge. Vi bruger MVVM, som står for **M**odel, **V**iew, **V**iew**M**odel.

| Lag | Ansvar | Fil i `app_2` | Kender NiceGUI? |
|---|---|---|---|
| **Model** | Henter data og laver dem om til DataFrames | `model.py` | Nej |
| **ViewModel** | Holder appens tilstand (state) og udfører handlinger | `viewmodel.py` | Nej |
| **View** | Viser elementer og reagerer på brugeren | `view.py` | Ja |

Derudover indeholder `options.py` de faste valgmuligheder, som flere lag bruger.

Lagene står på række, og hvert lag taler kun med sin nabo. Figuren viser, hvad der sker i `app_2`, når brugeren vælger en ny by:

```text
    bruger                                                                   internettet
      │ 1. vælger en by                                                         ▲ │ 4. henter
      ▼                                                                         │ ▼    data
┌────────────┐  2. load_forecast()   ┌──────────────┐  3. fetch_forecast()  ┌────────────┐
│    View    │ ────────────────────► │  ViewModel   │ ────────────────────► │   Model    │
│  view.py   │ ◄──────────────────── │ viewmodel.py │ ◄──────────────────── │  model.py  │
└────────────┘  6. læser vm.state    └──────────────┘  5. returnerer data   └────────────┘
```

De øverste pile peger mod højre og er **funktionskald**: et lag beder det næste lag om at gøre noget. De nederste pile peger mod venstre og er **svar**: data, der kommer tilbage.

1. Brugeren vælger en by i View.
2. View kalder `vm.load_forecast()` i ViewModel. View beder altså om nye data, men henter dem ikke selv.
3. ViewModel kalder `fetch_forecast()` i Model.
4. Model henter data fra internettet: den sender en forespørgsel til API'et og får et svar.
5. Model returnerer data som DataFrames til ViewModel, som gemmer dem i sin state.
6. View læser `vm.state` og tegner graf og tabel.

**Reglen er: et lag må kun kalde laget til højre for sig.**

| Lag | Må | Må ikke |
|---|---|---|
| **View** | kalde ViewModels metoder og læse dens state | hente data selv. Der står aldrig `fetch_forecast()` eller `requests` i `view.py` |
| **ViewModel** | kalde Models funktioner | bruge `ui.`. Den ved ikke, om data ender i en graf eller en tabel |
| **Model** | hente data og returnere dem | kalde de andre lag. Den ved ikke, at der findes en app |

Du kan kontrollere reglen ved at læse import-linjerne øverst i hver fil:

```python
# view.py
from viewmodel import WeatherViewModel

# viewmodel.py
from model import fetch_forecast

# model.py importerer hverken view eller viewmodel
```

Reglen gør, at du ved, hvor du skal lede, når noget skal ændres:

- Skal grafen have andre farver, retter du kun i `view.py`.
- Skal data komme fra et andet API, retter du kun i `model.py`.
- Virker datahentningen ikke, kan du køre `model.py` alene og finde fejlen uden at starte appen.

Vil du læse mere om arkitektur og MVVM?

- [Model-View-Controller på dansk Wikipedia](https://da.wikipedia.org/wiki/Model-View-Controller) er en kort introduktion på dansk til MVC, som MVVM bygger videre på.
- [Separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) forklarer princippet bag: hver del af koden har ét ansvar.
- [Model–view–viewmodel på Wikipedia](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel) beskriver de tre lag og historien bag mønstret.
- [Microsofts guide til MVVM](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm) går mere i dybden. Eksemplerne er skrevet i C#, men idéerne er de samme.

Flere links står under [Materialer](#materialer).

### Del 1: Data fra et API

#### HTTP, API og JSON

- **HTTP** er den protokol, som browsere og programmer bruger til at sende forespørgsler og modtage svar.
- Et **API** er en aftale om, hvilke data du kan bede en server om, og hvordan du skal spørge.
- **JSON** er det tekstformat, som svaret kommer i. I Python bliver JSON til dictionaries og lister.

En GET-forespørgsel består af en adresse og nogle parametre:

```python
import requests

URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 55.68,
    "longitude": 12.57,
    "hourly": "temperature_2m",
    "forecast_days": 3,
    "timezone": "Europe/Copenhagen",
}

response = requests.get(URL, params=params, timeout=10)
print(response.status_code)   # 200 betyder, at det gik godt
response.raise_for_status()   # stopper med en fejl, hvis det ikke gik godt
data = response.json()
print(data.keys())
```

`response` er hele HTTP-svaret med statuskode. `data` er indholdet lavet om til Python-objekter.

| Statuskode | Betydning |
|---|---|
| 200 | Alt gik godt |
| 400 | Din forespørgsel er forkert, fx en ugyldig parameter |
| 404 | Adressen findes ikke |
| 500 | Serveren har en fejl |

#### Fra JSON til DataFrame

Svaret indeholder en dictionary under nøglen `"hourly"`, hvor hver nøgle er en liste. Det passer præcis til en DataFrame, hvor hver nøgle bliver en kolonne.

```python
import pandas as pd

df = pd.DataFrame(data["hourly"])
df = df.rename(columns={"time": "date"})
df["date"] = pd.to_datetime(df["date"])
print(df.head())
```

#### Modellen er en funktion med en aftale

I modellaget pakker vi det hele ind i en funktion. Resten af appen behøver kun at kende funktionens aftale: hvad den får ind, og hvad den giver tilbage.

```python
def fetch_forecast(latitude: float, longitude: float) -> pd.DataFrame:
    # 1. byg params
    # 2. send GET, kontrollér status, læs JSON
    # 3. lav en DataFrame med kolonnerne "date" og "temperature_2m"
    return df
```

Der må ikke stå `ui.` noget sted i modellen.

I `src/app_2/model.py` kan du se lærerens version. Den bruger biblioteket `openmeteo_requests`, som er en færdig klient til Open-Meteo. Princippet er det samme: en forespørgsel med parametre ind, DataFrames ud. Filen indeholder også `fetch_coordinates()`, som slår en bys koordinater op.

#### Øvelser til del 1

**Øvelse 2.1 – Undersøg et svar.** Kør GET-eksemplet ovenfor i en ny fil. Udskriv `data["hourly_units"]`. Hvilken enhed har temperaturen?

**Øvelse 2.2 – Fremprovokér en fejl.** Sæt `"latitude"` til `999`, og fjern linjen med `raise_for_status()`. Udskriv `response.status_code` og `response.text`. Sæt derefter linjen ind igen. Hvad er forskellen?

**Øvelse 2.3 – En ny parameter.** Ændr forespørgslen, så den også henter `wind_speed_10m`. Hvor mange kolonner får din DataFrame nu?

**Øvelse 2.4 – Læs lærerens kode.** Åbn `src/app_2/model.py`:

1. Kør `python model.py`. Hvad returnerer `fetch_coordinates("Copenhagen")`? Ændr byen til Aarhus nederst i filen, og kør igen.
2. Hvad returnerer `fetch_forecast()`? Hvilke kolonner har de to DataFrames?
3. Findes der nogen linje med `ui.` i filen? Hvorfor ikke?

#### Projekt trin 2: Rigtige data

Opgaver og krav til trin 2 står i [aflevering.md](aflevering.md#trin-2-rigtige-data).

### Del 2: State, binding og events

#### Problemet med globale variable

I `app_1` ligger `weather_data`, `fig`, `plot` og de to checkboxe som globale variable, og `update_plot()` bruger dem alle. Når appen vokser, giver det to problemer:

- Enhver funktion kan ændre enhver variabel. Det bliver svært at se, hvem der ændrede hvad.
- Den samme oplysning ender let flere steder. Hvis den valgte by både ligger i `selected_city`, i `current_city` og i en dropdown, hvilken en gælder så?

#### Single source of truth

Princippet om **single source of truth** (SSOT) siger, at hver oplysning skal ligge ét sted, og at alle andre læser den derfra.

**Et eksempel uden SSOT.** Denne lille app har en titel, et byvalg og en knap:

```python
from nicegui import ui

CITIES = ["Copenhagen", "Aarhus", "Odense"]
graph_city = "Copenhagen"


def change_city(e) -> None:
    global graph_city
    graph_city = e.value


def show_graph() -> None:
    ui.notify(f"Henter data for {graph_city}")


ui.label("Vejret i Copenhagen").classes("text-2xl font-bold")
ui.select(CITIES, value="Copenhagen", on_change=change_city)
ui.button("Vis graf", on_click=show_graph)

ui.run()
```

Vælg Aarhus, og tryk på knappen. Beskeden siger Aarhus, men titlen siger stadig Copenhagen. Appen modsiger sig selv.

Årsagen er, at oplysningen "den valgte by" ligger tre steder: i teksten på titlen, i dropdownens værdi og i variablen `graph_city`. Hver gang byen ændres, skal programmøren huske at opdatere alle tre. Her blev titlen glemt.

**Det samme eksempel med SSOT.** Nu ligger den valgte by ét sted, nemlig i `state.station`. Alle elementer læser derfra:

```python
from dataclasses import dataclass
from nicegui import ui

CITIES = ["Copenhagen", "Aarhus", "Odense"]


@dataclass
class AppState:
    station: str = "Copenhagen"


state = AppState()


def show_graph() -> None:
    ui.notify(f"Henter data for {state.station}")


def reset() -> None:
    state.station = "Copenhagen"


ui.label().bind_text_from(
    state, "station", backward=lambda s: f"Vejret i {s}"
).classes("text-2xl font-bold")
ui.select(CITIES).bind_value(state, "station")
ui.button("Vis graf", on_click=show_graph)
ui.button("Nulstil", on_click=reset)

ui.run()
```

Titlen, dropdownen og beskeden kan ikke længere være uenige, for de har ingen egen kopi. Knappen `Nulstil` ændrer kun `state.station`, og alligevel følger både titlen og dropdownen med. (`@dataclass` og `bind` bliver forklaret i de næste afsnit.)

**SSOT gælder tre slags oplysninger i vores app:**

| Oplysning | Uden SSOT | Med SSOT |
|---|---|---|
| Brugerens valg | Byen ligger i flere variable og elementer | Byen ligger i `vm.state.station` |
| Faste værdier | Listen af byer er skrevet både i view og i model | `STATIONS` står i `options.py` og importeres |
| Beregnede værdier | `max_temperature` gemmes ved siden af data | Maksimum beregnes ud fra data, når det skal bruges |

Den sidste række er den, man lettest overser. Hvis du gemmer noget, der kan beregnes, har du to sandheder:

```python
# Uden SSOT: to felter, der skal holdes ens
state.hourly_forecast = new_data
state.max_temperature = 18.4      # passer kun, indtil data ændres igen

# Med SSOT: data er sandheden, resten beregnes
max_temperature = state.hourly_forecast["temperature_2m"].max()
```

En kopi, som view laver for at formatere data, er ikke et brud på princippet. Kopien bruges kun til visning og smides væk bagefter. Sandheden ligger stadig i state.

I vejrappen er state altså det fælles udgangspunkt. Grafen, tabellen og fejlbeskeden læser alle fra den samme state, og ingen af dem har deres egen kopi af, hvilken by der er valgt.

#### State som `@dataclass`

En dataclass er en klasse, der kun skal holde på data. Du skriver felterne med type og startværdi, og Python laver selv `__init__`.

```python
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class WeatherState:
    station: str = "Copenhagen"
    parameter: str = "temperature"
    is_loading: bool = False
    error_message: str = ""
    hourly_forecast: pd.DataFrame = field(default_factory=pd.DataFrame)
```

`field(default_factory=pd.DataFrame)` betyder, at hver ny state får sin egen tomme DataFrame.

```python
state = WeatherState()
print(state.station)      # Copenhagen
state.station = "Aarhus"
print(state)              # en pæn udskrift af alle felter
```

#### ViewModel udfører handlinger

ViewModel ejer state og har metoder, der ændrer den. View må gerne læse state, men det er ViewModel, der henter data og lægger dem ind.

```python
from model import fetch_forecast
from options import STATIONS


class WeatherViewModel:
    def __init__(self) -> None:
        self.state = WeatherState()

    def load_forecast(self) -> None:
        latitude, longitude = STATIONS[self.state.station]
        self.state.hourly_forecast = fetch_forecast(latitude, longitude)
```

ViewModel opretter ingen UI-elementer. Derfor kan du afprøve den i en almindelig Python-fil:

```python
vm = WeatherViewModel()
vm.load_forecast()
print(vm.state.hourly_forecast.head())
```

#### Binding forbinder et element med state

Binding holder et elements værdi og et felt i state synkroniseret, uden at du skriver en callback.

| Metode | Retning |
|---|---|
| `bind_value_to(vm.state, "station")` | Fra elementet til state |
| `bind_value_from(vm.state, "station")` | Fra state til elementet |
| `bind_value(vm.state, "station")` | Begge veje |

```python
vm = WeatherViewModel()

station_selection = ui.select(
    options=list(STATIONS.keys()),
    value=vm.state.station,
    label="Station",
)
station_selection.bind_value_to(vm.state, "station")

ui.label().bind_text_from(vm.state, "station", backward=lambda s: f"Valgt by: {s}")
```

Når brugeren vælger en by, ændres `vm.state.station`, og labelen følger med. Du har ikke skrevet nogen callback. Elementer, der reagerer på ændringer i state på denne måde, kaldes reaktive.

#### Binding og event-handler er to forskellige ting

Binding flytter en værdi. Den starter ikke noget arbejde. Hvis appen skal hente nye data, når byen ændres, skal du også registrere en event-handler:

```python
def update_forecast() -> None:
    vm.load_forecast()

station_selection.on_value_change(update_forecast)
```

Sådan rejser et byskift gennem lagene:

1. Brugeren vælger en by i `ui.select` (View).
2. Bindingen skriver værdien til `vm.state.station` (state).
3. Event-handleren kalder `vm.load_forecast()` (ViewModel).
4. ViewModel kalder `fetch_forecast()` (Model), som henter data.
5. ViewModel lægger de nye data i state.
6. View viser de nye data. Det ser vi på i del 3.

#### Øvelser til del 2

**Øvelse 2.5 – Din første dataclass.** Lav en dataclass `CounterState` med feltet `count: int = 0`. Lav en klasse `CounterViewModel` med metoden `increment()`. Afprøv dem med `print` uden NiceGUI.

**Øvelse 2.6 – Reaktiv tæller.** Byg tælleren fra øvelse 1.2 igen, men nu med din `CounterViewModel`. Labelen skal bruge `bind_text_from`, og knappen skal kalde `vm.increment`. Sammenlign med din gamle løsning. Hvor ligger tallet nu?

**Øvelse 2.7 – Bindingens retning.** Lav et `ui.input` og en `ui.label`, som begge er bundet til det samme felt i en state. Tilføj en knap, der sætter feltet til `"Nulstillet"`. Afprøv inputfeltet med `bind_value_to`, `bind_value_from` og `bind_value`. Hvad sker der i hvert tilfælde, når du trykker på knappen?

**Øvelse 2.8 – Følg et byskift.** Åbn `src/app_2/view.py` og `src/app_2/viewmodel.py`. Indsæt `print("1: handler")`, `print("2: viewmodel")` og så videre på de steder, som de seks trin ovenfor beskriver. Kør appen, skift by, og kontrollér rækkefølgen i terminalen.

**Øvelse 2.9 – Ret og udvid lærerens app.** `WeatherState` har et felt `parameter`, og `options.py` har en dictionary `PARAMETERS`, men brugeren kan ikke vælge parameter i appen.

1. Tilføj et `ui.select` med parametrene i `view.py`, bind det til `vm.state.parameter`, og lad det kalde `update_forecast`.
2. Vælg `rain` i appen. Hvad sker der? Læs fejlmeddelelsen i terminalen.
3. Fejlen ligger i `fetch_forecast()` i `model.py`. Find den, forklar den for din makker, og ret den.

**Øvelse 2.10 – Find de to sandheder.** Kør programmet, og skriv et nyt navn i feltet.

```python
from nicegui import ui

name = "Anna"


def rename(e) -> None:
    global name
    name = e.value
    greeting.set_text(f"Hej {name}")


greeting = ui.label("Hej Anna")
badge = ui.label("Logget ind som: Anna")
ui.input("Navn", value="Anna", on_change=rename)

ui.run()
```

1. Hvilken tekst på siden bliver forkert?
2. Hvor mange steder i programmet ligger navnet? Skriv dem op.
3. Skriv programmet om, så navnet kun ligger i en state, og begge tekster er bundet til den.
4. Åbn `src/app_2`. Hvor mange filer skal du ændre for at tilføje Aalborg til appen? Hvorfor er det nok?

#### Projekt trin 3: State og valg

Opgaver og krav til trin 3 står i [aflevering.md](aflevering.md#trin-3-state-og-valg).

### Del 3: Refresh og fejlhåndtering

#### `@ui.refreshable` genopbygger en del af siden

Nye data i state ændrer ikke en graf, der allerede er tegnet. Med `@ui.refreshable` markerer du en funktion, der bygger en del af siden, så den kan bygges igen.

```python
@ui.refreshable
def weather_figure() -> None:
    df = vm.state.hourly_forecast
    fig = px.line(df, x="date", y="temperature_2m", markers=True)
    ui.plotly(fig).classes("w-full h-96")


weather_figure()            # opretter grafen første gang
weather_figure.refresh()    # sletter den gamle graf og bygger en ny
```

Event-handleren fra del 2 får derfor én linje mere:

```python
def update_forecast() -> None:
    vm.load_forecast()
    weather_figure.refresh()
```

Byvælgeren står uden for den refreshable funktion, så den bliver ikke bygget om.

#### View formaterer en kopi

Når view skal vise data pænt, for eksempel afrunde tal eller skrive datoer som tekst, gør den det på en kopi. De oprindelige data i state forbliver uændrede, så andre dele af appen stadig kan regne på dem.

```python
daily_df = vm.state.daily_forecast.copy()
daily_df["date"] = daily_df["date"].dt.strftime("%a %d/%m")
```

#### Fejl er en del af datahentning

Når et program taler med internettet, kan meget gå galt: der er ingen forbindelse, serveren svarer ikke, eller svaret mangler data. Uden fejlhåndtering stopper funktionen med en traceback i terminalen, og brugeren ser bare en app, der ikke reagerer.

#### `try`, `except` og `finally`

```python
try:
    response = requests.get(URL, params=params, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    print("Serveren svarede ikke i tide.")
except requests.ConnectionError:
    print("Ingen forbindelse.")
finally:
    print("Færdig med forsøget.")
```

| Blok | Hvornår kører den? |
|---|---|
| `try` | Altid. Stopper ved den første linje, der fejler |
| `except` | Kun hvis der opstod en fejl af den nævnte type |
| `else` | Kun hvis `try` lykkedes (valgfri) |
| `finally` | Altid, uanset om det gik godt eller skidt (valgfri) |

Fang de fejltyper, du forventer. Hvis du skriver `except:` uden type alle steder, bliver dine egne stavefejl også skjult, og så er de svære at finde.

#### Hvert lag har sin opgave ved fejl

| Lag | Opgave | Eksempel i `app_2` |
|---|---|---|
| Model | Opdager fejlen og giver den videre med en klar besked | `raise RuntimeError("The coordinate request timed out.") from error` |
| ViewModel | Fanger fejlen og skriver den i state | `self.state.error_message = "Vejrdata kunne ikke hentes."` |
| View | Viser beskeden til brugeren | `ui.label(vm.state.error_message)` |

Modellen kan ikke vise noget til brugeren, for den kender ikke NiceGUI. Den kan kun rejse en fejl med `raise`:

```python
def fetch_coordinates(address: str) -> tuple[float, float]:
    try:
        response = requests.get(url, params=params, timeout=(5, 10))
        response.raise_for_status()
    except requests.Timeout as error:
        raise RuntimeError("The coordinate request timed out.") from error

    results = response.json().get("results", [])
    if not results:
        raise ValueError(f"No coordinates were found for {address!r}.")
    ...
```

Den sidste del er vigtig. Et tomt svar er ikke en fejl for `requests`, så modellen må selv kontrollere det.

ViewModel fanger fejlen og gør den til state:

```python
def load_forecast(self) -> None:
    self.state.is_loading = True
    self.state.error_message = ""

    try:
        self.state.hourly_forecast = fetch_forecast(...)
    except Exception as error:
        print(repr(error))   # teknisk besked til udvikleren
        self.state.hourly_forecast = pd.DataFrame()
        self.state.error_message = "Vejrdata kunne ikke hentes."   # besked til brugeren
    finally:
        self.state.is_loading = False
```

Her fanger vi `Exception`, fordi ViewModel er det sidste sted, fejlen kan stoppes, før den rammer brugeren. Den tekniske fejl udskrives stadig i terminalen, så udvikleren kan se den. `finally` sørger for, at `is_loading` altid bliver sat tilbage. Læg også mærke til, at gamle data ryddes, så appen ikke viser data fra den forrige by under det nye valg.

View vælger, hvad brugeren ser:

```python
@ui.refreshable
def weather_figure() -> None:
    if vm.state.error_message:
        ui.label(vm.state.error_message).classes("text-red-600")
        return

    df = vm.state.hourly_forecast
    if df.empty:
        ui.label("Ingen prognosedata at vise.")
        return

    ui.plotly(px.line(df, x="date", y="temperature_2m")).classes("w-full h-96")
```

Fejlen er nu en del af state, og derfor virker den på samme måde som alt andet: ViewModel ændrer state, og view viser den.

#### Øvelser til del 3

**Øvelse 2.11 – Forudsig udskriften.** Hvad udskriver programmet? Skriv dit gæt ned, før du kører det.

```python
def divide(a, b):
    try:
        print("A")
        result = a / b
        print("B")
    except ZeroDivisionError:
        print("C")
        result = None
    finally:
        print("D")
    return result

print(divide(10, 2))
print(divide(10, 0))
```

**Øvelse 2.12 – Den rigtige fejltype.** Skriv en funktion `read_number()`, som beder brugeren om et tal med `input()` og returnerer det som `float`. Hvis brugeren skriver noget, der ikke er et tal, skal funktionen spørge igen. Hvilken fejltype skal du fange?

**Øvelse 2.13 – Fjern refresh.** Fjern linjen `weather_figure_3day.refresh()` i `src/app_2/view.py`, og skift by i appen. Hvad sker der med grafen, og hvad sker der med tabellen? Forklar forskellen.

**Øvelse 2.14 – Simulér en fejl.** Indsæt denne linje øverst i `fetch_forecast()` i `src/app_2/model.py`:

```python
raise requests.ConnectionError("Øvelsesfejl")
```

1. Start appen. Hvad ser brugeren, og hvad står der i terminalen?
2. Hvilket lag fangede fejlen, og hvilket lag viste den?
3. Fjern linjen igen, og kontrollér, at appen virker.

**Øvelse 2.15 – En by, der ikke findes.** Kald `fetch_coordinates("Xyzby")` fra en Python-fil. Hvilken fejltype får du, og hvilken linje i `model.py` rejser den?

#### Projekt trin 4: En robust app

Opgaver og krav til trin 4 står i [aflevering.md](aflevering.md#trin-4-en-robust-app).

---

## Modul 3: Pakker og navigation

**Mål:** Du kan dele et program op i moduler og pakker og importere mellem dem. Du kan bygge en app med flere sider og en fælles menu, hvor hver side har sit eget View og sin egen ViewModel.

**Fagligt fokus:**

- **Modularisering:** et program delt op i moduler og pakker, og hvad der sker ved en `import`
- **Afhængigheder mellem lag:** importer følger MVVM-lagene, så View kender ViewModel, og ViewModel kender Model, men ikke omvendt
- **Navigation:** flere sider i samme app med en fælles ramme (`ui.sub_pages`)
- **Arkitektur, der skalerer:** MVVM med flere sider, hvor hver side har sit eget View og sin egen ViewModel

**Lærerens eksempel:** `src/app_3/`

Modulet har to dele. Først lærer du, hvordan Python-kode organiseres i mapper. Derefter bruger du strukturen til at bygge en app med flere sider.

### Del 1: Moduler og pakker

#### Et modul er en fil

Hver `.py`-fil er et **modul**. Du har allerede brugt moduler i `app_2`, hvor `viewmodel.py` henter en funktion fra `model.py`:

```python
from model import fetch_forecast
```

Linjen betyder: find modulet `model`, og hent navnet `fetch_forecast` derfra. Der er to måder at importere på:

| Du skriver | Sådan bruger du det |
|---|---|
| `import model` | `model.fetch_forecast(...)` |
| `from model import fetch_forecast` | `fetch_forecast(...)` |

At dele et program op i moduler kaldes modularisering. Hvert modul skal have ét ansvar, og navnet skal fortælle, hvad det er.

#### Hvad sker der ved en import?

Når Python importerer et modul, bliver hele filen kørt én gang. Gem dette som `geometry.py`:

```python
print("geometry.py bliver indlæst")


def area(width: float, height: float) -> float:
    return width * height


if __name__ == "__main__":
    print("Test:", area(2, 3))
```

Og dette som `main.py` i samme mappe:

```python
from geometry import area

print(area(4, 5))
```

| Du kører | Udskrift |
|---|---|
| `python geometry.py` | `geometry.py bliver indlæst` og `Test: 6` |
| `python main.py` | `geometry.py bliver indlæst` og `20` |

Linjen `if __name__ == "__main__":` betyder "kun hvis denne fil er den, der blev startet". Koden under den kører ikke, når filen bliver importeret af en anden fil.

Det bruger vi to steder:

- Nederst i et modul til en lille test, som i `app_2/model.py`.
- I `main.py` omkring `ui.run()`, så appen kun starter, når `main.py` selv bliver kørt.

#### En pakke er en mappe med moduler

Når der bliver mange moduler, samler vi dem i mapper. En mappe med moduler kaldes en **pakke**. Den indeholder en fil med navnet `__init__.py`, som fortæller, at mappen er en pakke. Filen må gerne være tom.

`app_3` er en pakke med to underpakker:

```text
src/
└── app_3/                          pakken app_3
    ├── __init__.py
    ├── main.py                     root() og ui.run()
    ├── models/                     pakken app_3.models
    │   ├── __init__.py
    │   ├── models.py               STATIONS, PARAMETERS og CLIMATE_YEARS
    │   └── services.py             fetch_forecast() og andre API-kald
    └── views/                      pakken app_3.views
        ├── __init__.py
        ├── forecast.py             View for prognosesiden
        ├── forecast_viewmodel.py   ViewModel for prognosesiden
        ├── climate.py              View for klimasiden
        └── climate_viewmodel.py    ViewModel for klimasiden
```

Sammenlign med `app_2`, hvor alle filer lå i samme mappe:

| `app_2` | `app_3` |
|---|---|
| `options.py` | `models/models.py` |
| `model.py` | `models/services.py` |
| `viewmodel.py` | `views/forecast_viewmodel.py` |
| `view.py` | `views/forecast.py` og `main.py` |

#### Import mellem pakker

Et modul i en pakke har en adresse, hvor mapperne adskilles med punktum. Filen `src/app_3/models/services.py` har adressen `app_3.models.services`.

Vi skriver altid hele adressen, og den starter altid med pakkens navn. Det kaldes en **absolut import**:

```python
from app_3.models.services import fetch_forecast
from app_3.models.models import PARAMETERS
from app_3.views.forecast import forecast_view
```

Fordelen er, at den samme linje virker i alle filer i projektet, uanset hvilken mappe filen ligger i.

| I `app_2` | I `app_3` |
|---|---|
| `from model import fetch_forecast` | `from app_3.models.services import fetch_forecast` |
| `from options import PARAMETERS` | `from app_3.models.models import PARAMETERS` |
| `from viewmodel import WeatherViewModel` | `from app_3.views.forecast_viewmodel import ForecastViewModel` |

Du kan møde en anden skrivemåde i andres kode, for eksempel `from .services import fetch_forecast`. Det er en relativ import. Vi bruger absolutte importer i hele forløbet.

#### Sådan finder Python pakken

Python leder efter pakken `app_3` i den mappe, programmet bliver startet fra. Derfor skal appen startes fra `src`, som er mappen, hvor `app_3` ligger:

```text
cd src
python -m app_3.main
```

`-m` betyder "kør dette modul". Læg mærke til, at du skriver modulets adresse med punktummer og uden `.py`.

Tre fejl, du med sikkerhed kommer til at møde:

| Du gør | Fejlmeddelelse | Forklaring |
|---|---|---|
| Kører `python app_3/main.py` | `ModuleNotFoundError: No module named 'app_3'` | Python leder nu inde i mappen `app_3` og kan ikke se pakken udefra |
| Kører `python -m app_3.main` fra en forkert mappe | `Error while finding module specification for 'app_3.main'` | Du står ikke i `src` |
| Skriver `from models.services import ...` | `ModuleNotFoundError: No module named 'models'` | Adressen mangler pakkens navn forrest |

**I PyCharm:**

- Opret en pakke med højreklik → **New → Python Package**. Så laver PyCharm selv `__init__.py`.
- Højreklik på mappen `src`, og vælg **Mark Directory as → Sources Root**. Så forstår PyCharm dine importer, og du kan starte `main.py` med højreklik → **Run**.

#### Importer følger lagene

I modul 2 lærte du, at et lag kun må kalde laget til højre for sig: View kalder ViewModel, og ViewModel kalder Model. Med pakker kan du se reglen direkte i import-linjerne:

| Fil | Må importere fra | Må ikke importere fra |
|---|---|---|
| `main.py` | `views` | |
| `views/forecast.py` | sin egen ViewModel, `models/models.py` | |
| `views/forecast_viewmodel.py` | `models` | `nicegui` |
| `models/services.py` | | `views`, `nicegui` |

Hvis `models` importerer fra `views`, og `views` importerer fra `models`, får du en cirkulær import, og programmet kan ikke starte. Men vigtigere: så er lagdelingen brudt.

Du kan altså kontrollere din arkitektur ved at læse de øverste linjer i hver fil.

#### Øvelser: moduler og pakker

**Øvelse 3.1 – Dit første modul.** Opret `geometry.py` og `main.py` som i eksemplet ovenfor.

1. Kør begge filer, og sammenlign med tabellen.
2. Fjern linjen `if __name__ == "__main__":`, og ryk linjen under den ud til venstre. Kør `main.py`. Hvad er forskellen?
3. Tilføj en funktion `perimeter()` til `geometry.py`, og brug den i `main.py`.

**Øvelse 3.2 – Byg en pakke.** Opret denne struktur i en ny mappe:

```text
shop/
├── __init__.py
├── main.py
├── models/
│   ├── __init__.py
│   └── prices.py
└── views/
    ├── __init__.py
    └── receipt.py
```

`prices.py`:

```python
PRICES = {"æble": 4, "banan": 3, "mælk": 12}


def total(items: list[str]) -> int:
    return sum(PRICES[item] for item in items)
```

`receipt.py` skal indeholde en funktion `print_receipt(items)`, som udskriver hver vare med pris og til sidst totalen. `main.py` skal kalde `print_receipt(["æble", "banan", "mælk"])`.

Skriv selv import-linjerne i `receipt.py` og `main.py`, og start programmet med `python -m shop.main`. Hvilken mappe skal du stå i?

**Øvelse 3.3 – Fremprovokér fejlene.** Brug pakken fra øvelse 3.2:

1. Kør `python shop/main.py`. Læs fejlmeddelelsen.
2. Skriv `cd shop`, og kør `python -m shop.main`. Læs fejlmeddelelsen.
3. Ændr importen i `receipt.py` til `from models.prices import PRICES, total`, og start programmet rigtigt. Læs fejlmeddelelsen.

Forklar for din makker, hvad hver fejl betyder, og ret dem igen.

**Øvelse 3.4 – Find fejlene.** Linjerne står i `app_3/views/forecast.py`. Hvilke er forkerte, og hvorfor?

```python
from app_3.models.models import STATIONS
from models.services import fetch_forecast
from app_3.views.forecast_viewmodel.py import ForecastViewModel
from app_3.views import forecast_viewmodel
from app_3/models/models import PARAMETERS
```

**Øvelse 3.5 – Læs importerne.** Åbn alle filer i `src/app_3`, og læs kun import-linjerne.

1. Tegn en pil fra hver fil til de filer, den importerer fra.
2. Går der nogen pil fra `models` til `views`?
3. Hvilke filer importerer `nicegui`? Passer det med tabellen ovenfor?

### Del 2: Navigation

#### Flere sider i samme app

Indtil nu har hele appen været én side. Når appen får flere funktioner, deler vi den op i sider. Hver side er en funktion, der bygger sit eget indhold, og hver side ligger i sit eget modul i pakken `views`.

`views/forecast.py`:

```python
from nicegui import ui


def forecast_view() -> None:
    ui.label("Prognose").classes("text-2xl font-bold")
```

`views/climate.py`:

```python
from nicegui import ui


def climate_view() -> None:
    ui.label("Klima").classes("text-2xl font-bold")
```

Der er ingen `ui.run()` i de to filer. De beskriver kun en side.

#### En fælles ramme med `ui.sub_pages`

`main.py` importerer siderne og bygger den ramme, der er ens på alle sider: en header og en menu. `ui.sub_pages` er det område, hvor den valgte side bliver vist.

```python
from nicegui import ui
from app_3.views.forecast import forecast_view
from app_3.views.climate import climate_view


def root() -> None:
    with ui.header():
        ui.label("Weather app")
    with ui.left_drawer():
        ui.link("Forecast", "/")
        ui.link("Climate", "/climate")
    ui.sub_pages({"/": forecast_view, "/climate": climate_view}).classes("w-full")


if __name__ == "__main__":
    ui.run(root, reload=False)
```

Dictionary'en forbinder en adresse med en funktion. Når brugeren klikker på et link, skifter kun indholdet i `ui.sub_pages`. Header og menu bliver stående.

Læg mærke til, at der står `forecast_view` uden parenteser. Det er samme princip som med callbacks i modul 1.

#### MVVM med flere sider

Hver side har sit eget View og sin egen ViewModel med sin egen state. Modellaget er fælles: begge sider kan bruge de samme funktioner i `services.py`.

| Side | View | ViewModel | Model |
|---|---|---|---|
| Prognose | `views/forecast.py` | `views/forecast_viewmodel.py` | `models/services.py` |
| Klima | `views/climate.py` | `views/climate_viewmodel.py` | `models/services.py` |

Det er her, arkitekturen betaler sig. Du kan bygge en ny side uden at røre ved den gamle, og du kan genbruge modellen uden at kopiere kode.

#### Øvelser: navigation

**Øvelse 3.6 – To sider.** Lav en lille pakke med en `main.py` og en underpakke `views`. Appen skal have en header, en menu og to sider, `Forside` og `Om`, som ligger i hvert sit modul. Hver side skal bare vise en overskrift.

**Øvelse 3.7 – En tredje side.** Tilføj en side `Kontakt` til appen fra øvelse 3.6. Hvilke filer skulle du oprette, og hvilke skulle du ændre?

**Øvelse 3.8 – State på tværs af sider.** Lav en tæller med knap på `Forside`. Klik nogle gange, gå til `Om`, og gå tilbage. Hvad er der sket med tallet? Forklar hvorfor ud fra, hvor ViewModel bliver oprettet. Vi løser problemet i modul 4.

**Øvelse 3.9 – Læs lærerens kode.** Åbn `src/app_3/main.py` og `src/app_3/views/forecast.py`:

1. Hvad er forskellen på `view.py` i `app_2` og `views/forecast.py` i `app_3`?
2. Hvorfor er der ingen `ui.run()` i `forecast.py`?
3. Hvilke filer skulle du oprette og ændre for at tilføje en side mere?

### Projekt trin 5: Pakke og flere sider

Opgaver og krav til trin 5 står i [aflevering.md](aflevering.md#trin-5-pakke-og-flere-sider).

---

## Modul 4: Udvidelse

**Mål:** Du kan få din app til at huske data, og du kan forklare, hvorfor adgangen til gemte data samles ét sted.

**Fagligt fokus:**

- **Data persistence:** data, der overlever en genindlæsning og en genstart af appen
- **NiceGUI storage:** forskellen på `app.storage.user` og `app.storage.general`
- **Repository pattern:** al læsning og skrivning af gemte data samles i én klasse
- **Abstraktion:** resten af appen kender metoderne, men ikke hvor data bliver gemt, så lageret kan skiftes ud

### Data persistence

Alt, der ligger i en variabel eller i state, forsvinder, når siden genindlæses, eller appen genstartes. Data persistence betyder, at data overlever. Det kræver, at de bliver gemt et sted uden for programmets hukommelse, for eksempel i en fil eller en database.

### NiceGUI storage

NiceGUI har et indbygget lager, som opfører sig som en dictionary og automatisk bliver gemt i en fil.

| Lager | Hvem deler data? | Bruges til |
|---|---|---|
| `app.storage.user` | Én bruger (én browser) | Brugerens egne valg, fx favoritby |
| `app.storage.general` | Alle brugere | Fælles data for hele appen |

```python
from nicegui import app, ui


def root() -> None:
    visits = app.storage.user.get("visits", 0) + 1
    app.storage.user["visits"] = visits
    ui.label(f"Du har besøgt siden {visits} gange")


ui.run(root, storage_secret="skriv-din-egen-hemmelige-tekst")
```

`app.storage.user` kræver, at du giver `ui.run` en `storage_secret`. Den bruges til at beskytte den cookie, der genkender browseren.

Storage kan også bindes direkte til et element, ligesom state:

```python
ui.select(["Copenhagen", "Aarhus", "Odense"], label="By").bind_value(
    app.storage.user, "station"
)
```

NiceGUI gemmer data i mappen `.nicegui`. Tilføj den til din `.gitignore`, så brugerdata ikke ender på GitHub.

### Repository pattern

Hvis `app.storage.user[...]` står spredt ud over alle Views og ViewModels, får du samme problem som med globale variable: ingen har overblik, og hvis du en dag vil gemme i en database i stedet, skal du rette alle steder.

Et **repository** er en klasse, der samler al læsning og skrivning af én slags data. Resten af appen kalder dens metoder og behøver ikke vide, hvor data bliver gemt.

```python
from nicegui import app


class FavoriteRepository:
    """Det eneste sted i appen, der ved, hvor favoritterne gemmes."""

    KEY = "favorites"

    def get_all(self) -> list[str]:
        return list(app.storage.user.get(self.KEY, []))

    def add(self, city: str) -> None:
        favorites = self.get_all()
        if city not in favorites:
            favorites.append(city)
            app.storage.user[self.KEY] = favorites

    def remove(self, city: str) -> None:
        favorites = self.get_all()
        if city in favorites:
            favorites.remove(city)
            app.storage.user[self.KEY] = favorites
```

Repository hører til i modellaget, for eksempel i `models/repository.py`. ViewModel bruger det sådan her:

```python
class ForecastViewModel:
    def __init__(self) -> None:
        self.state = WeatherState()
        self.favorites = FavoriteRepository()

    def save_current_station(self) -> None:
        self.favorites.add(self.state.station)
```

Det er det samme princip som resten af forløbet: hvert stykke kode har ét ansvar, og hver oplysning har ét hjem.

```text
View  ──►  ViewModel  ──►  services.py     ──►  API på internettet
                      ──►  repository.py   ──►  NiceGUI storage
```

### Øvelser til modul 4

**Øvelse 4.1 – Besøgstæller.** Kør eksemplet med `visits`. Genindlæs siden, og genstart appen. Åbn derefter appen i et privat browservindue. Hvad sker der med tallet? Skift til `app.storage.general`, og prøv igen.

**Øvelse 4.2 – Find filen.** Find mappen `.nicegui` i dit projekt, og åbn filen i den. Hvilket format er data gemt i?

**Øvelse 4.3 – Et notat, der bliver.** Lav et `ui.textarea`, som er bundet til `app.storage.user`. Skriv noget, genstart appen, og kontrollér, at teksten stadig er der.

**Øvelse 4.4 – Løs problemet fra øvelse 3.8.** Brug storage til at få tælleren til at huske sit tal, når brugeren skifter side.

**Øvelse 4.5 – Skift lager.** Skriv en ny version af `FavoriteRepository`, som gemmer favoritterne i en JSON-fil i stedet for i NiceGUI storage. Metoderne skal have de samme navne. Hvor meget kode uden for klassen skal ændres, for at appen kan bruge den nye version?

### Projekt trin 6: Appen gemmer brugerens valg

Opgaver og krav til trin 6 står i [aflevering.md](aflevering.md#trin-6-appen-gemmer-brugerens-valg).

---

## Aflevering

Kravene til den endelige aflevering og tjeklisten står i [aflevering.md](aflevering.md#den-endelige-aflevering).

## Materialer

- NiceGUI dokumentation: https://nicegui.io/documentation
- NiceGUI binding: https://nicegui.io/documentation/section_binding_properties
- NiceGUI refreshable: https://nicegui.io/documentation/refreshable
- NiceGUI sub pages: https://nicegui.io/documentation/sub_pages
- NiceGUI storage: https://nicegui.io/documentation/storage
- NiceGUI styling med `.classes()`, `.style()` og `.props()`: https://nicegui.io/documentation/section_styling_appearance
- Tailwind CSS, sådan virker klasserne i `.classes()`: https://tailwindcss.com/docs/styling-with-utility-classes
- Tailwind tekststørrelse (`text-2xl`): https://tailwindcss.com/docs/font-size
- Tailwind farver (`text-gray-500`, `bg-blue-100`): https://tailwindcss.com/docs/colors
- Tailwind afstand (`p-4`, `m-2`, `gap-4`): https://tailwindcss.com/docs/padding
- Tailwind bredde og højde (`w-full`, `h-96`): https://tailwindcss.com/docs/width
- Quasar komponenter, egenskaber til `.props()`: https://quasar.dev/vue-components/button
- Python lambda-udtryk: https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
- Plotly Express: https://plotly.com/python/plotly-express/
- Requests: https://requests.readthedocs.io/en/latest/user/quickstart/
- Open-Meteo Forecast API: https://open-meteo.com/en/docs
- Open-Meteo Air Quality API: https://open-meteo.com/en/docs/air-quality-api
- MVC-arkitektur: https://openclassrooms.com/en/courses/6900866-write-maintainable-python-code/7009312-structure-an-application-with-the-mvc-design-pattern
- MVVM-arkitektur: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/stable/core_concepts/mvvm.html
- MVC på dansk Wikipedia: https://da.wikipedia.org/wiki/Model-View-Controller
- Separation of concerns: https://en.wikipedia.org/wiki/Separation_of_concerns
- MVVM på Wikipedia: https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel
- Microsofts guide til MVVM (eksempler i C#): https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm
- Martin Fowler om GUI-arkitekturer (for de nysgerrige): https://martinfowler.com/eaaDev/uiArchs.html
- Struktur i Python-projekter: https://docs.python-guide.org/writing/structure/
- Repository pattern i Python: https://www.cosmicpython.com/book/chapter_02_repository.html
