# VejrApp 



I denne opgave skal I lave din egen lille app med Python og NiceGUI. 


Du skal lære at: 

1. Lave en simpel app med NiceGUI 
2. Bruge basic UI objekter
  - inputfelter, knapper og tekst
  - row, column, page
3. skrive app i MVVM arkitektur.
4. Koncept af data persistence, error exception.


## Faglige mål og fokus 

- redegøre for arkitekturen af programmer på forskellige abstraktionsniveauer, 
herunder relationen mellem brug og funktion 
- rette, tilpasse og udvide avancerede programmer 
- arbejde inkrementelt og systematisk i programmeringsprocessen.


## Fagligt indhold 


- arkitekturen for programmers interaktion med omgivelserne med 
henblik på hændelsestyret interaktion og interaktion mellem systemer. 


## Materialer 

### MVC architecture 

https://openclassrooms.com/en/courses/6900866-write-maintainable-python-code/7009312-structure-an-application-with-the-mvc-design-pattern

### MVVM architecture 

https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/stable/core_concepts/mvvm.html#



## Aflevering

Opgaven skal afleveres via en Github repository, der skal indeholder:

- din Python-fil
- en readme fil, der forklare, hvad din app kan og appens features. 
- en kort refleksion overfor forskellige UI elementer, appens arkitektur.  

--- 

## Install 

https://nicegui.io/


## Module 1: NiceGUI Basis 

Vis static/mock vejr data i NiceGUI og plot med plotly. 

### Indehold

- UI-komponenter 
  -  `ui.label`, `ui.button`, `ui.plotly`
- Layout med context managers
  -  `ui.row`, ` ui.columns`
- event handler og callback-funktioner
  - ui.button(`on_click`)
- Opdatering af en komponent




### Opgaver: CO₂ Forecast App – version 1

I denne opgave skal I udvikle en lille NiceGUI-app, som viser en modelprognose for koncentrationen af CO₂ i atmosfæren.

I den første version skal I bruge kunstige data. I skal altså endnu ikke hente data fra internettet.


#### Startdata

Opret først en funktion, som returnerer følgende data:

```python
def make_co2_table() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "time": [
                "08:00",
                "10:00",
                "12:00",
                "14:00",
                "16:00",
            ],
            "carbon_dioxide": [
                421.2,
                422.5,
                424.1,
                423.6,
                422.8,
            ],
        }
    )
```

CO₂-koncentrationen angives i enheden ppm, som betyder “parts per million”.

#### Opgave 1: Vis appens titel

Opret følgende elementer:

* en overskrift med teksten `CO₂ Forecast App`
  - https://nicegui.io/documentation/label#label
* en mindre tekst med teksten `Model data for Copenhagen`
* en knap med teksten `Show CO₂`
  - https://nicegui.io/documentation/button




#### Opgave 2: Fremstil en graf

Skriv funktionen:

```python
def make_co2_plot(df: pd.DataFrame):
    ...
```

Funktionen skal returnerer et plot med:

* `time` på x-aksen
* `carbon_dioxide` på y-aksen
* markører på datapunkterne
* titlen `CO₂ forecast`
* akseteksten `CO₂ (ppm)` på y-aksen

https://plotly.com/python/plotly-express/

#### Opgave 3: Vis grafen i NiceGUI

Brug `ui.plotly()` til at vise figuren i appen.

Grafen skal fylde hele den tilgængelige bredde. Det kan gøres med:

```python
.classes("w-full")
```
https://nicegui.io/documentation/plotly#plotly_element

#### Opgave 4: Tilføj interaktion

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

#### Opgave 5: Vis en besked

Når grafen bliver opdateret, skal appen vise en kort besked:

```python
ui.notify("CO₂ forecast updated")
```


#### Ekstraopgave

Tilføj endnu en dataserie med modeldata for metan:

```python
"methane": [1980, 1985, 1992, 1988, 1983]
```

Tilføj to knapper:

* `CO₂`
* `Methane`

Når brugeren trykker på en knap, skal grafen vise den valgte parameter.

Overvej, hvordan `make_co2_plot()` kan ændres, så den modtager navnet på den valgte parameter som argument.

#### Aflevering

Appen skal som minimum indeholde:

* en overskrift
* kunstige data i en DataFrame
* en Plotly-graf
* mindst én knap
* en callback-funktion
* en graf, som kan opdateres


--- 

## Module 2: API og MVVM Arkitektur 

### Indehold
- Http client, API get 
- ` @dataclass`
- ` bind_value`
- UI refresh 


### Features 

I denne version kan brugeren vælge en by og en vejrparameter, som skal vises i appen. Vejrdata hentes fra Open-Meteos API og omdannes til en DataFrame, før de vises i en opdateret Plotly-graf.

Appen viser en loading-indikator, mens data hentes. Hvis der opstår en fejl, eller hvis API’et ikke returnerer nogen data, vises en passende fejlmeddelelse til brugeren.

Samtidig opdeles programmet efter MVVM-arkitekturen, så datahentning, applikationens tilstand og brugergrænsefladen får hver deres ansvar.

### Opgaver 

1. 

2. 


--- 
## Module 3: Navigation 

### Indehold 

- MVVM (**M**odel, **V**iew, **V**iewmodel) arkitektur


--- 

## Module 4: Udvidelse 

### Indehold 

- NiceGUI storage
- repository pattern


