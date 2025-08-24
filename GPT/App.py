import json
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "Result"


def get_latest_result_dir() -> Path | None:
    if not RESULTS_DIR.exists():
        return None
    dirs = [d for d in RESULTS_DIR.iterdir() if d.is_dir()]
    if not dirs:
        return None
    return sorted(dirs)[-1]


st.set_page_config(page_title="NSGA-II Results Dashboard", layout="wide")
st.title("NSGA-II Results Dashboard")

latest = get_latest_result_dir()
if latest is None:
    st.info("No results found. Please run mainGA.py first.")
else:
    st.caption(f"Latest results: {latest.name}")
    csv_path = latest / "pareto_front_filtered.csv"
    json_path = latest / "best_solutions.json"

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        st.subheader("Pareto Front")
        st.dataframe(df, use_container_width=True)
        st.scatter_chart(df, x="f1", y="f2")
    else:
        st.warning("pareto_front_filtered.csv not found")

    if json_path.exists():
        with json_path.open("r", encoding="utf-8") as f:
            best = json.load(f)
        st.subheader("Best Solution")
        st.json(best)
    else:
        st.warning("best_solutions.json not found")