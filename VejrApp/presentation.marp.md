---
marp: true
theme: default
size: 16:9
paginate: true
title: Vejrappen · Modul 2 · MVVM
description: Tre undervisningsgange med API, state, binding, events og fejlhåndtering
style: |
  section { font-family: Arial, sans-serif; font-size: 28px; padding: 54px 68px; color: #17324d; background: #f8fafc; }
  h1 { font-size: 48px; color: #123753; }
  h2 { font-size: 38px; color: #123753; }
  strong { color: #007f86; }
  pre { font-size: 23px; line-height: 1.28; background: #eaf0f5; }
  code { font-family: 'DejaVu Sans Mono', monospace; }
  table { font-size: 25px; width: 100%; }
  th { background: #dbecef; }
  section.lead { background: #123753; color: #ffffff; }
  section.lead h1, section.lead h2 { color: #ffffff; }
  section.lead strong { color: #80d8d0; }
  section.small pre { font-size: 21px; }
---
<!-- _class: lead -->

# Weather Station 
## Repetition 

Åbn jeres app fra modul 1, og vis den til en makker.

- Hvilke NiceGUI-elementer bruger I til input og output?
- Hvordan har I organiseret layoutet med `with`?
- Hvor ligger de data, som grafen og tabellen viser?
- Hvilken funktion kører, når brugeren ændrer et valg?
- Kan du tegne en "flow", der viser hvordan events og data rejse igennem forskellige moduler 






## Modul 2 · MVVM arkitektur



### Indehold 

- **M**odel, **V**iew, **V**iew**M**odel arkitekture (**MVVM**) 
- **S**ingle **S**ource **O**f **T**ruth (**SSOT**) principle  
- Http client, API get 
- ` dataclass`
- ` bind_value`
- `Error ` og `Exceptions `

**Gennemgang:** vejrappen. 
**Øvelser:** jeres egen CO₂- og AQI-app.

---
<!-- _class: lead -->
## MVVM og data fra et API

**Mål:** Du kan forklare ansvaret i hvert lag og hente en prognose.

<!-- LÆRER: Start med at vise den eksisterende app og skifte by. Spørg eleverne, hvilke opgaver programmet udfører bag brugerfladen. -->

---
## Appens opgaver

Brugeren vælger en by og ser:

- En temperaturgraf for de første tre kalenderdage.
- En tabel med minimum og maksimum for ti dage.
- En forståelig besked, hvis data ikke kan hentes.

**Spørgsmål:** Hvilke opgaver handler om data, og hvilke handler om visning?

<!-- LÆRER: Tre kalenderdage fra første datas midnat er den præcise betydning af den viste filtrering. Det er ikke nødvendigvis de næste 72 timer. Ti dage kræver forecast_days=10 i forespørgslen; funktionsnavnet weather_table_10day begrænser ikke selv antallet af rækker. -->

---
## MVVM fordeler ansvaret

| Del | Ansvar i vores app |
|---|---|
| Model og service | Datastruktur, HTTP og konvertering til DataFrames |
| ViewModel | Aktuel state og handlingen `load_forecast()` |
| View | Byvalg, graf, tabel og brugerhændelser |

**MVVM:** Model–View–ViewModel.

<!-- LÆRER: En service er en hjælper til dataadgang i modeldelen, ikke et ekstra bogstav i MVVM. Grænsen mellem modellens data og ViewModels præsentationstilstand kan placeres forskelligt. Her ejer ViewModel state. En lille callback i view, som kalder ViewModel og opdaterer UI, passer til denne undervisningsvariant af MVVM. -->

---
## Filerne i undervisningseksemplet

| Fil | Eksempel på indhold |
|---|---|
| `options.py` | `STATIONS` og `PARAMETERS` |
| `service.py` | `fetch_forecast(latitude, longitude)` |
| `viewmodel.py` | `WeatherState` og `WeatherViewModel` |
| `view.py` | `weather_view()` og `ui.run()` |

View bruger ViewModel. ViewModel bruger service.
Service behøver ikke kende NiceGUI.

<!-- LÆRER: Dette er en foreslået filstruktur, ikke en beskrivelse af usete filer. Bed eleverne finde importerne i den udleverede view-fil. Diskutér, hvad der kan genbruges, hvis brugerfladen senere ændres. -->

---
## HTTP-klienten og API'et

**HTTP** er en protokol til forespørgsler og svar.
**API'et** beskriver, hvilke data vi kan bede om.
**Requests** er det Python-bibliotek, vi bruger som HTTP-klient.

En GET-forespørgsel indeholder en adresse og parametre.
Svaret indeholder en statuskode og en body med data.

<!-- LÆRER: Requests kører her på Python-serveren. NiceGUI-browseren kontakter ikke selv Open-Meteo. Bibliotekets navn er requests med s. Kilde: https://requests.readthedocs.io/en/latest/user/quickstart/ -->

---
<!-- _class: small -->
## Parametre beskriver vores forespørgsel

```python
URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 55.68,
    "longitude": 12.57,
    "hourly": "temperature_2m,precipitation",
    "daily": "temperature_2m_min,temperature_2m_max",
    "timezone": "Europe/Copenhagen",
    "forecast_days": 10,
}
```

Hver time giver grafdata. Hver dag giver tabeldata.

<!-- LÆRER: Koordinaterne er et eksempel for København. Her svarer STATIONS til steder med koordinater, ikke nødvendigvis fysiske målestationer. Open-Meteo leverer prognoser. timezone gør datoerne relevante for dansk lokal tid. Kilde: https://open-meteo.com/en/docs -->

---
## Et GET-kald med Requests

```python
import requests

response = requests.get(URL, params=params, timeout=10)
response.raise_for_status()
data = response.json()
```

`response` repræsenterer HTTP-svaret.
`data` indeholder JSON-data som Python-objekter.

<!-- LÆRER: Vis response.status_code og data.keys(). 200 betyder succes, 400 er eksempel på en ugyldig forespørgsel, 500 er en serverfejl. raise_for_status rejser en exception ved HTTP-fejl; selve håndteringen kommer i del 3. timeout=10 begrænser ventetid ved forbindelse/læsning, ikke nødvendigvis hele kaldets samlede varighed. JSON-konvertering kan også fejle. Kilde: https://requests.readthedocs.io/en/latest/user/quickstart/ -->

---
## JSON bliver til DataFrames

```python
import pandas as pd

hourly = pd.DataFrame(data["hourly"])
daily = pd.DataFrame(data["daily"])

hourly = hourly.rename(columns={"time": "date"})
daily = daily.rename(columns={"time": "date"})
hourly["date"] = pd.to_datetime(hourly["date"])
daily["date"] = pd.to_datetime(daily["date"])
```

Nu kan vi filtrere datoer og bruge kolonnerne i Plotly.

<!-- LÆRER: Vis data['hourly'] før konverteringen og hourly.head() efter. Forklar at hver nøgle bliver en kolonne, og listerne bliver rækker. ISO-datoerne i denne forespørgsel repræsenterer lokal tid, men pandas gør dem ikke automatisk timezone-aware. Undgå at blande dem med UTC-datoer senere. -->

---
## Servicefunktionens aftale

```python
def fetch_forecast(latitude, longitude):
    # Byg params med de valgte koordinater
    # Send GET, kontrollér status, læs JSON
    # Opret hourly og daily som på forrige slide
    return hourly, daily
```

**Input:** koordinater.
**Output:** to DataFrames med aftalte kolonnenavne.
**Ved fejl:** funktionen kan rejse en exception.

<!-- LÆRER: Dette er bevidst en skitse, ikke en færdig funktion. Saml de foregående kodeuddrag live. Hourly kræver date, temperature_2m og precipitation. Daily kræver date, temperature_2m_min og temperature_2m_max. Ingen ui.label eller ui.notify i servicefunktionen. -->

---
## Øvelse 1 · Data til jeres CO₂- og AQI-app

1. Flyt datahentningen til en servicefunktion i `service.py`.
2. Hent data fra den eller de datakilder, I bruger i projektet.
3. Undersøg datoer, værdier, enheder og eventuelle manglende data.
4. Returnér DataFrames med kolonnenavne, som I selv aftaler.

**Vis din makker:** Et servicekald uden NiceGUI og de første rækker.

<!-- LÆRER: 35 min, eller 25 min hvis repetition indgår i første undervisningsgang. Eleverne arbejder videre i egen app. Datakilderne er ikke angivet i oplægget: giv dem projektets konkrete API-adresser og et eksempel på svarformatet. Antag ikke, at ét API leverer både CO₂ og AQI. Afklar, hvad CO₂-serien måler, og hvilken AQI-skala de bruger. Ved forskellige tidsopløsninger eller steder kan de beholde to DataFrames. Hvis API-adgang ikke er klar, kan et gemt svar bruges til konverteringsdelen, mens HTTP-kald demonstreres fælles. Succeskriterium: service leverer data uden at oprette UI. Hurtige elever kan undersøge manglende værdier og sortere efter tid. -->

---
## Opsamling · Del 1

- Hvilket lag skal kende API-adressen?
- Hvad er forskellen på `response` og `data`?
- Hvorfor omdøber vi `time` til `date`?
- Kan vi undersøge servicefunktionen uden NiceGUI?

**Næste gang:** Hvem holder styr på den valgte by?

<!-- LÆRER: Facit: service; HTTP-svar versus afkodede data; view forventer date som del af aftalen; ja, med et almindeligt funktionskald. Brug 10 min på at få eleverne til selv at formulere svarene. -->

---
<!-- _class: lead -->
# Del 2
## State, binding og events

**Mål:** Du kan følge et byvalg fra brugerfladen til nye data.

<!-- LÆRER: 10 min genkaldelse: lad eleverne beskrive de fire filer uden at se oversigten. -->

---
## Single source of truth

**`vm.state` er det fælles udgangspunkt for appens aktuelle tilstand.**

Her finder vi valgt by, valgt parameter, prognoser og fejlbesked.
Graf og tabel læser den samme state.

Service leverer nye data. ViewModel lægger dem i state.
En lokal kopi til formatering kan godt bruges i view.

<!-- LÆRER: Skeln mellem Open-Meteo som ekstern datakilde og state som appens aktuelle autoritative tilstand. Et ui.select har også en value; binding forbinder denne med state. Pointen er at undgå konkurrerende variable som selected_city, current_city og station, der opdateres uafhængigt. Single source of truth er et designprincip, ikke en bestemt NiceGUI-funktion. -->

---
<!-- _class: small -->
## En enkel state-klasse

```python
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class WeatherState:
    station: str = "København"
    parameter: str = "Temperatur"
    hourly_forecast: pd.DataFrame = field(
        default_factory=pd.DataFrame)
    daily_forecast: pd.DataFrame = field(
        default_factory=pd.DataFrame)
    error_message: str = ""
```

<!-- LÆRER: Vælg station og parameter, som findes i jeres egne dictionaries. default_factory skaber en ny DataFrame for hver state-instans. En almindelig dataclass er tilstrækkelig til dette eksempel. Vi indfører ikke ui.state. Dette er et forslag, der matcher attributterne i den udleverede view-fil. -->

---
<!-- _class: small -->
## ViewModel opdaterer state

```python
class WeatherViewModel:
    def __init__(self):
        self.state = WeatherState()

    def load_forecast(self):
        location = STATIONS[self.state.station]
        hourly, daily = fetch_forecast(
            location["latitude"], location["longitude"])
        self.state.hourly_forecast = hourly
        self.state.daily_forecast = daily
        self.state.error_message = ""
```

<!-- LÆRER: Uddraget forudsætter import af STATIONS og fetch_forecast. Her antager vi fx STATIONS = {'København': {'latitude': 55.68, 'longitude': 12.57}}. Tilpas opslaget til den faktiske struktur. Exceptions tilføjes i del 3. ViewModel skaber ingen UI-elementer. -->

---
## Bindingens retning

| Metode | Hvad bliver synkroniseret? |
|---|---|
| `bind_value_to(state, "station")` | Elementets værdi til state |
| `bind_value_from(state, "station")` | State til elementets værdi |
| `bind_value(state, "station")` | Begge retninger |

Din view-fil bruger **`bind_value_to`**.
To-vejs binding er nyttig, hvis kode også ændrer byen.

<!-- LÆRER: Lad eleverne ændre vm.state.station via en knap og sammenligne retningerne. Almindelige Python-attributter observeres med NiceGUI's bindingmekanisme; undgå at præsentere alle ændringer som øjeblikkelige i alle sammenhænge. Kilder: https://nicegui.io/documentation/select og https://nicegui.io/documentation/section_binding_properties -->

---
## Byvalget i din view-fil

```python
station_selection = ui.select(
    options=list(STATIONS.keys()),
    value=vm.state.station,
    label="Station",
)
station_selection.bind_value_to(vm.state, "station")
station_selection.on_value_change(update_forecast)
```

Binding synkroniserer værdien. Event-handleren starter arbejdet.

<!-- LÆRER: Vis at binding alene ikke kalder load_forecast og ikke genopbygger Plotly-grafen. Initialværdien kommer eksplicit fra state. Undgå en generel garanti om callback-rækkefølge på tværs af NiceGUI-versioner. Undersøg den konkrete version med print(vm.state.station) i handleren. Ved behov kan e.value bruges til en eksplicit overdragelse til en ViewModel-metode. Kilde: https://nicegui.io/documentation/select -->

---
## En event-handler er en funktion

```python
def update_forecast():
    vm.load_forecast()
    weather_figure_3day.refresh()
    weather_table_10day.refresh()

station_selection.on_value_change(update_forecast)
```

`update_forecast` giver NiceGUI funktionen til senere brug.
`update_forecast()` kalder funktionen med det samme.

<!-- LÆRER: on_change=callback kan angives ved oprettelse af ui.select. on_value_change(callback) registrerer handleren bagefter, som i brugerens kode. Handleren her behøver ikke argumenter. En handler kan også modtage et event med e.value. Små UI-handlere i view må gerne delegere arbejdet til ViewModel. Kilde: https://nicegui.io/documentation/select -->

---
## Hvad sker der ved et byskift?

1. Brugeren vælger en by i `ui.select`.
2. Den valgte værdi overføres til `vm.state.station`.
3. Handleren beder ViewModel om en prognose.
4. Service returnerer data, og ViewModel opdaterer state.
5. View genopbygger grafen og tabellen.

**Undersøg:** Hvilke trin kræver netværk?

<!-- LÆRER: Dette er det tilsigtede flow i appen, ikke en generel specifikation af event-loopets rækkefølge. Facit: servicekaldet i trin 4. Brug print før og efter load_forecast til at gøre forløbet synligt. refresh forklares i næste del. -->

---
## Øvelse 2 · State og valg i jeres egen app

1. Opret en state med valgt dataserie, data og fejlbesked.
2. Lad jeres ViewModel hente data gennem servicefunktionen.
3. Tilføj et valg mellem CO₂ og AQI, og bind det til state.
4. Registrér en handler, som opdaterer den relevante visning.

**Undersøg:** Kræver et skift nye data, eller er de allerede hentet?
Grafens titel og enhed skal passe til den valgte serie.

<!-- LÆRER: 35 min. Et forslag er en AppState med parameter='CO₂', co2_data, aqi_data og error_message. Brug navne, som passer til elevernes eksisterende kode. Bindingseksempel: ui.select(['CO₂', 'AQI'], value=vm.state.parameter).bind_value(vm.state, 'parameter'). Registrér derefter en on_value_change-handler. Giv refresh-kaldet som stillads indtil del 3. Når begge serier er hentet, kræver skiftet kun ændret visning. Hvis kun én serie er hentet, skal handleren eventuelt hente den anden. Undgå at antage, at de to datasæt har samme kolonner eller enheder. Succeskriterium: valget i state bestemmer visningen, og der findes ikke en separat konkurrerende variabel for samme valg. -->

---
## Opsamling · Del 2

| Situation | Hvad skal ske? |
|---|---|
| Brugeren vælger en anden by | Ny forespørgsel og ny visning |
| Brugeren vælger nedbør | Grafen bruger en anden kolonne |
| Kode ændrer byen i state | To-vejs binding kan opdatere byvalget |

**Forklar:** Hvorfor er binding og en event-handler to forskellige ting?

<!-- LÆRER: Facit: Binding forbinder værdier. Handleren udfører en handling som load_forecast eller refresh. En programmatisk ændring af et bundet element kan også medføre et value-change-event; undgå utilsigtede dobbeltkald. Brug 10 min til opsamling. -->

---
<!-- _class: lead -->
# Del 3
## Refresh og fejlhåndtering

**Mål:** Du kan opdatere det rigtige UI-område og vise fejl uden et nedbrud.

<!-- LÆRER: Genkaldelse 10 min. Bed eleverne forklare, hvorfor nye DataFrames i state ikke i sig selv ændrer en allerede oprettet Plotly-figur. -->

---
## `@ui.refreshable`

```python
@ui.refreshable
def weather_figure_3day():
    # Læs state og opret grafens UI-elementer
    ...

weather_figure_3day()          # Opret første visning
weather_figure_3day.refresh()  # Genopbyg visningen
```

Refresh sletter funktionens tidligere UI-elementer og opretter dem igen.

<!-- LÆRER: ... markerer udeladt kode. Det er funktionen, som dekoreres, ikke DataFramen. En almindelig ændring i vm.state giver her ikke automatisk refresh. Byvælgeren ligger uden for de refreshable funktioner, så den bliver ikke genskabt. Zoom og andre lokale UI-valg i grafen kan gå tabt ved genopbygning. Kilde: https://nicegui.io/documentation/refreshable -->

---
## Grafen læser et udsnit af state

```python
df = vm.state.hourly_forecast
start_date = df["date"].min().normalize()
end_date = start_date + pd.Timedelta(days=3)

three_day_df = df[
    (df["date"] >= start_date) & (df["date"] < end_date)
]
parameter_id = PARAMETERS[vm.state.parameter]
fig = px.line(three_day_df, x="date", y=parameter_id)
ui.plotly(fig).classes("w-full h-96")
```

**Interval:** startdatoen er med, slutdatoen er ikke med.

<!-- LÆRER: Dette er et uddrag inde i weather_figure_3day. Tjek fejl og tom DataFrame før dette uddrag, som vist senere. normalize sætter tidspunktet til midnat. Tegn eksemplet på tavlen med tre kalenderdatoer. parentheses og & er vigtige ved pandas-filtrering. Den fulde prognose bliver i state. -->

---
## Tabellen formaterer en kopi

```python
daily_df = vm.state.daily_forecast.copy()
daily_df["date"] = (
    pd.to_datetime(daily_df["date"]).dt.strftime("%a %d/%m")
)
daily_df = daily_df.rename(columns={
    "temperature_2m_min": "minimum",
    "temperature_2m_max": "maximum",
})
rows = daily_df.to_dict("records")
```

State beholder datokolonnen i dens oprindelige datatype.

<!-- LÆRER: Det resterende tabeluddrag findes i brugerens view: afrunding til én decimal, columns med name/field/label/align og ui.table. Vis records som en liste af dictionaries. %a følger serverens locale og giver ikke nødvendigvis danske ugedage. row_key='date' fungerer for dette korte udsnit med unikke datoetiketter; behold en separat ISO-dato som nøgle ved længere perioder. -->

---
## Den første visning

```python
# Først: definér handlers og refreshable funktioner

vm.load_forecast()
weather_figure_3day()
weather_table_10day()
```

Ved start hentes data før graf og tabel oprettes.
Ved senere byskift bruger handleren `.refresh()`.

<!-- LÆRER: I brugerens kode nævner update_forecast to funktioner, som defineres længere nede. Navnene slås først op, når handleren kører. Det virker, fordi et brugerudløst byskift sker efter opbygningen. Registrér ikke en handler med et utilsigtet øjeblikkeligt kald før funktionerne findes. -->

---
## Fejl er en del af datahentning

| Situation | Mulig reaktion |
|---|---|
| Ingen forbindelse eller timeout | En besked og mulighed for at prøve igen |
| API svarer med HTTP-fejl | Kontrol med `raise_for_status()` |
| Data har forkert format | Kontrol af forventede felter |
| DataFrame er tom | En tomtilstandsbesked i view |

En tom DataFrame er ikke i sig selv en exception.

<!-- LÆRER: Spørg hvordan UI'et skal se ud efter et fejlet byskift. Her vælger vi at rydde gamle prognoser, så appen ikke viser gamle bydata under et nyt byvalg. En anden løsning kan beholde gamle data med tydelig markering, men det er ikke denne lektions strategi. -->

---
## `try` og `except`

```python
try:
    response = requests.get(URL, params=params, timeout=10)
    response.raise_for_status()
except requests.RequestException:
    print("Vejrdata kunne ikke hentes.")
```

Python forsøger at udføre `try`-blokken.
Ved en matchende exception fortsætter programmet i `except`.

<!-- LÆRER: Dette er et isoleret syntakseksempel. I appen lader vi service rejse fejlen og håndterer den i ViewModel på næste slide. Kode efter fejllinjen i try springes over. Fang kendte fejltyper, så stavefejl og andre programmeringsfejl stadig opdages under udvikling. Kilde: https://requests.readthedocs.io/en/latest/user/quickstart/ -->

---
<!-- _class: small -->
## ViewModel omsætter fejl til state

```python
def load_forecast(self):
    location = STATIONS[self.state.station]
    try:
        hourly, daily = fetch_forecast(
            location["latitude"], location["longitude"])
    except requests.RequestException:
        self.state.hourly_forecast = pd.DataFrame()
        self.state.daily_forecast = pd.DataFrame()
        self.state.error_message = "Vejrdata kunne ikke hentes."
    else:
        self.state.hourly_forecast = hourly
        self.state.daily_forecast = daily
        self.state.error_message = ""
```

<!-- LÆRER: Erstat den tidligere load_forecast-metode med denne, og importér requests. else kører, når try lykkes. Hvis I ikke ønsker at introducere else endnu, kan succeslinjerne stå sidst i try. RequestException dækker netværk og HTTP-fejl fra Requests, men ikke alle problemer med dataskemaet. Manglende keys eller en forkert kolonnelængde kræver særskilt validering i service. Log tekniske detaljer under udvikling frem for at vise et råt traceback i UI'et. -->

---
## View vælger, hvad brugeren ser

```python
if vm.state.error_message:
    ui.label(vm.state.error_message).classes("text-red-600")
    return

df = vm.state.hourly_forecast
if df.empty:
    ui.label("Ingen prognosedata at vise.")
    return

# Opret grafen, når der er data
```

Samme princip bruges med `daily_forecast` i tabellen.

<!-- LÆRER: Det oprindelige view tjekker allerede error_message. Tilføj empty-guard før opslag og min(). Fejlbeskeden kan vises to gange, fordi både graf og tabel tjekker den. Det er acceptabelt som første løsning; et fælles statusområde er en senere forbedring. Fordi ViewModel håndterer fejlen, når handleren stadig frem til begge refresh-kald. -->

---
## Øvelse 3 · En robust CO₂- og AQI-app

1. Gør graf og tabel refreshable, så de læser jeres state.
2. Håndtér en forespørgselsfejl i ViewModel med `try/except`.
3. Simulér en fejl, og vis en forståelig besked i appen.
4. Hent data igen, og kontrollér, at visningen vender tilbage.

**Kontrollér også:** Tomme data og skift mellem CO₂ og AQI.
Gamle data må ikke fremstå som data for det nye valg.

<!-- LÆRER: 25 min. Med Requests kan service midlertidigt rejse requests.ConnectionError('Øvelsesfejl'). Fjern fejlen og prøv igen. Ved et andet HTTP-bibliotek skal eleverne bruge dets exceptiontyper. Succeskriterier: fejlbeskeden vises, UI'et viser ikke misvisende gamle data, tomme datasæt giver en besked, og et nyt vellykket kald rydder fejlen. Hvis appen henter CO₂ og AQI separat, kan eleverne starte med én samlet fejltilstand. Ekstraopgave: separate fejlbeskeder, så den ene serie stadig kan vises, når den anden fejler. -->

---
## Fælles kodegennemgang

- Hvor er den valgte by gemt?
- Hvad starter et API-kald?
- Hvad sker der, hvis vi fjerner `.refresh()`?
- Hvorfor formaterer tabellen en kopi?
- Hvordan kommer appen tilbage efter en fejl?

**Afslutning:** Forklar et skift mellem CO₂ og AQI i jeres app med MVVM-rollerne.

<!-- LÆRER: 10 min. Facit: vm.state.station; event-handleren kalder ViewModel, som bruger service; state ændres, men eksisterende graf/tabel genopbygges ikke; vi bevarer data og datatyper i state; et vellykket kald erstatter data, rydder error_message og efterfølges af refresh. -->

---
## Valgfri udvidelse · Ventetid i brugerfladen

`requests.get()` er synkron og kan blokere NiceGUI-serveren.
Den enkle version gør kaldsforløbet let at følge i undervisningen.

En senere version kan bruge:

- `run.io_bound()` til det blokerende servicekald.
- En async HTTP-klient.
- Loading-state og midlertidigt deaktiveret byvalg.

<!-- LÆRER: Denne slide er en valgfri afslutning, ikke en ekstra obligatorisk del. Async alene gør ikke requests.get non-blocking. Flyt helst selve servicekaldet til en worker, og opdatér state efter await på UI-siden. Ved flere samtidige forespørgsler skal et gammelt svar ikke overskrive den senest valgte bys data. Undgå at introducere alt dette sammen med elevernes første try/except. Kilder: https://requests.readthedocs.io/en/stable/user/advanced/ og https://nicegui.io/documentation -->

---
## Dokumentation og videre arbejde

- [NiceGUI · Select og value binding](https://nicegui.io/documentation/select)
- [NiceGUI · Refreshable](https://nicegui.io/documentation/refreshable)
- [Requests · Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
- [Open-Meteo · Forecast API](https://open-meteo.com/en/docs)

**Projektets næste skridt:** Flere sider med samme ansvarsfordeling.

<!-- LÆRER: Kilder kontrolleret 2. oktober 2026. Eksemplerne tager udgangspunkt i brugerens view-fil og supplerer med foreslået service og ViewModel. Del 1 slutter med opsamlingen før Del 2, del 2 før Del 3. De sidste to slides er valgfrit perspektiv og referencer. -->
