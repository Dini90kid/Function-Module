import os, sys
from pathlib import Path
import streamlit as st

# Make repo root importable no matter CWD
BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from lakehouse_fm_agent.runtime.lineage import load_edges

st.set_page_config(page_title="Lakehouse FM Agent", layout="wide")
st.title("Lakehouse FM Agent — Preview")

up = st.file_uploader("Upload LINEAGE.txt", type=["txt"])
if up is not None:
    txt = up.getvalue().decode("utf-8", errors="ignore")
    tmp = Path("uploaded_LINEAGE.txt"); tmp.write_text(txt, encoding="utf-8")
    edges = load_edges(tmp)
    st.success(f"Parsed edges: {len(edges)}")
    with st.expander("Preview edges"):
        st.dataframe(edges)
    mmd = ["graph TD"] + [f'  "{p}" --> "{c}"' for p,c,k,s in edges]
    st.markdown("```mermaid\n" + "\n".join(mmd) + "\n```")
