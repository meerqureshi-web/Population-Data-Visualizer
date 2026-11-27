"""PS 33 - Population Data Visualizer (Python 3, Pandas, Matplotlib)."""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
NO_GROWTH = "Growth: not available (only one year of data)"

def load_data(path):
    """Read CSV, skip invalid rows (with reason), drop duplicate City+Year rows."""
    csv_path = Path(path)
    candidates = [csv_path]
    if not csv_path.suffix:
        candidates.append(csv_path.with_suffix(".csv"))
    if not csv_path.is_absolute():
        script_dir = Path(__file__).resolve().parent
        candidates.extend(script_dir / candidate for candidate in tuple(candidates))
    csv_path = next((candidate for candidate in candidates if candidate.is_file()), csv_path)
    try:
        raw = pd.read_csv(csv_path, dtype=str, sep=None, engine="python")
    except FileNotFoundError:
        sys.exit(f"File '{path}' not found.")
    rows = []
    for i, r in enumerate(raw.itertuples(index=False), start=1):
        city, year, pop = (str(v).strip() for v in r[:3])
        if not year.isdigit():
            print(f"Row {i} skipped: invalid Year '{year}'.")
        elif not pop.lstrip("-").isdigit():
            print(f"Row {i} skipped: invalid Population '{pop}'.")
        elif int(pop) <= 0:
            print(f"Row {i} skipped: Population must be positive.")
        else:
            rows.append((city, int(year), int(pop)))
    df = pd.DataFrame(rows, columns=["City", "Year", "Population"])
    df = df.drop_duplicates(["City", "Year"], keep="last")
    print(f"Valid rows: {len(df)}")
    return df.sort_values("Year", kind="stable")

def analyse(df):
    """groupby() -> first/latest population of every city and growth %."""
    g = df.groupby("City", sort=False).agg(
        y1=("Year", "first"), y2=("Year", "last"),
        p1=("Population", "first"), p2=("Population", "last"))
    g["growth"] = (g.p2 - g.p1) / g.p1 * 100
    g.loc[g.y1 == g.y2, "growth"] = float("nan")  # only one year of data
    return g

def show_summary(df, g):
    year = f" ({df['Year'].max()})" if df["Year"].nunique() > 1 else ""
    print(f"Total population{year}: {g.p2.sum()}")
    print(f"Largest city: {g.p2.idxmax()} ({g.p2.max()})")
    if g.growth.notna().any():
        print(f"Fastest growing: {g.growth.idxmax()} ({g.growth.max():+.2f}%)")
    else:
        print(NO_GROWTH)

def finish(title, xlabel, ylabel, fname):
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.savefig(fname)


def show_growth_and_charts(df, g):
    growth = g.growth.dropna()
    if growth.empty:
        return print(NO_GROWTH)
    print(" | ".join(f"{c}: {v:+.2f}%" for c, v in growth.items()))
    plt.figure()
    plt.bar(growth.index, growth.values, color="teal")
    finish("Population Growth by City", "City", "Growth (%)", "growth_bar_chart.png")
    plt.figure()
    for city, d in df.groupby("City", sort=False):
        plt.plot(d["Year"], d["Population"], marker="o", label=city)
    plt.legend()
    finish("Population Trend", "Year", "Population", "population_trend_line_chart.png")
    print("Bar chart 'Population Growth by City' and line chart 'Population Trend' displayed")
    plt.show()

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else input("CSV file name: ")
    df = load_data(path)
    if df.empty:
        sys.exit("No valid data to analyse.")
    g = analyse(df)
    print("\n1. Summary\n2. Growth and charts")
    choice = input("Menu option: ").strip()
    action = {"1": show_summary, "2": show_growth_and_charts}.get(choice)
    action(df, g) if action else print("Invalid option.")

if __name__ == "__main__":
    main()
