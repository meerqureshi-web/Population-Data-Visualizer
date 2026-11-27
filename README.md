# Population-Data-Visualizer
A Python command-line application that reads city population data from a CSV file, summarizes the latest population statistics, calculates population growth, and displays chart visualizations using Pandas and Matplotlib.

## Features

- Loads population data from a CSV file
- Skips invalid rows and reports the reason
- Removes duplicate `City` and `Year` entries, keeping the last entry
- Calculates total population, largest city, and fastest-growing city
- Generates a population growth bar chart
- Generates a population trend line chart
- Saves charts as PNG files in the working directory

## Requirements

- Python 3
- Pandas
- Matplotlib

Install the dependencies with:

```bash
pip install pandas matplotlib
```

## Project Files

```text
Population_Data_Visualizer/
├── Codebase/
│   ├── Population Data Visualizer.py
│   └── population.csv
├── Documentation/
└── README.md
```

## CSV Format

The CSV file must contain at least these columns:

```csv
City,Year,Population
Raipur,2020,1000000
Raipur,2024,1100000
Durg,2020,500000
Durg,2024,600000
```

- `City`: City name
- `Year`: Four-digit or numeric year
- `Population`: Positive whole number

Column order is expected as `City`, `Year`, `Population`. The application supports common CSV separators detected by Pandas.

## Usage

Open a terminal in the project directory and run:

```bash
python "Codebase/Population Data Visualizer.py"
```

Enter the CSV file name when prompted:

```text
population.csv
```

You can also provide the path as a command-line argument:

```bash
python "Codebase/Population Data Visualizer.py" "Codebase/population.csv"
```

## Menu Options

After valid data is loaded, choose:

1. **Summary** — Shows the total population, largest city, and fastest-growing city.
2. **Growth and charts** — Calculates growth percentages and displays both charts.

## Generated Charts

When growth data is available, the application saves:

- `growth_bar_chart.png` — Population growth percentage by city
- `population_trend_line_chart.png` — Population trend over time by city

Chart windows are displayed through Matplotlib. Growth calculations require at least two different years for a city.

## Data Validation

Rows are skipped when:

- The year is not numeric
- The population is not numeric
- The population is not positive

Duplicate city-year entries are removed, with the final occurrence retained.
