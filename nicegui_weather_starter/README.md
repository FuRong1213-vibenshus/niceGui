# GUI -- App udvikling 



This starter pack contains five small versions of a weather app project.
The code is intentionally not completely finished. Students should read the
TODO comments and complete the missing parts.

## Materialer 

- Tutorials: https://www.pythonguis.com/tutorials/getting-started-nicegui/


## Suggested Teaching Path

1. `01_mock_plot` - NiceGUI layout and Plotly with fake weather data.
2. `02_observation_api` - Fetch measured weather observations from DMI.
3. `03_forecast_api` - Fetch forecast data from DMI using coordinates.
4. `04_mvvm_structure` - Split the app into model, service, viewmodel, and view.
5. `05_extension_persistence` - Add favorite locations and compare ideas.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run One Version

```bash
cd 01_mock_plot
python main.py
```

Then open the local NiceGUI address shown in the terminal.

