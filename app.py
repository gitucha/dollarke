# app.py
import csv
import streamlit as st
from models import Fund

st.set_page_config(page_title="DollarKE", layout="wide")
st.title(" Kenyan Money Market Fund Comparison")

# Get the data from the mmf.csv file(dummy values)
funds = []
with open('data/mmfs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        funds.append(
            Fund(
                name=row['Fund'],
                yield_rate=float(row['Yield']),
                fees=float(row['Fees']),
                min_deposit=float(row['MinDeposit'])
            )
        )

# Filtering the mmfs using a sidebar by the minimum yield they produce 
st.sidebar.header("Filters")
min_yield = st.sidebar.slider("Minimum Yield %", 0.0, 20.0, 10.0)

# taking the filtered mmfs and sorting them
filtered_funds = [f for f in funds if f.yield_rate >= min_yield]
sorted_funds = sorted(filtered_funds, key=lambda f: f.net_return(), reverse=True)

#  Display the data inform of a Table 
st.subheader("Funds Table (Sorted by Net Return)")
table_data = [
    {
        "Fund": f.name,
        "Yield (%)": f.yield_rate,
        "Fees (%)": f.fees,
        "Min Deposit": f.min_deposit,
        "Net Return (%)": round(f.net_return(), 2)
    }
    for f in sorted_funds
]
st.table(table_data)

# --- Top 5 Bar Chart Using Streamlit ---
st.subheader("Top 5 Funds by Net Return (Built-in Streamlit Chart)")
top5 = sorted_funds[:5]

# We need a dict where the fund name is index and net return is value
chart_data = {
    f.name: f.net_return() for f in top5
}


# Quick hack: list of net returns, then write names separately.
st.bar_chart(list(chart_data.values()))
st.write("Funds (left to right):", ", ".join(chart_data.keys()))