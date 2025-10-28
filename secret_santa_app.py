import random
from typing import List, Tuple
import streamlit as st

# ---------- Utils ----------
def parse_names(raw: str) -> List[str]:
    # Split by lines, trim, remove empties and duplicates (preserve order)
    seen = set()
    out = []
    for line in raw.splitlines():
        name = line.strip()
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out

def sattolo_derangement(items: List[str]) -> List[str]:
    # This algorithm generates a derangement (no one gets themselves)
    arr = items[:]
    n = len(arr)
    if n < 2:
        raise ValueError("Need at least 2 participants.")
    for i in range(n - 1, 0, -1):
        j = random.randrange(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def build_pairs(givers: List[str], receivers: List[str]) -> List[Tuple[str, str]]:
    return list(zip(givers, receivers))

# ---------- UI ----------
st.set_page_config(page_title="Secret Santa", page_icon="🎁", layout="centered")
st.title("🎁 Secret Santa")

names_input = st.text_area(
    "Enter names:",
    height=200,
    placeholder="Write here!",
)

if st.button("Generate assignments", type="primary"):
    participants = parse_names(names_input)
    if len(participants) < 3:
        st.error("You need at least 3 participants.")
    else:
        random.seed()
        receivers = sattolo_derangement(participants)
        pairs = build_pairs(participants, receivers)

        st.success("Assignments generated.")

        rows = [{"Giver": g, "Receiver": r} for g, r in pairs]
        st.table(rows)