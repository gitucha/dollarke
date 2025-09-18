import csv
import streamlit as st
from models import Fund
from db import init_db, add_user, verify_user

st.set_page_config(page_title="DollarKE", layout="wide")
st.header("Welcome to DollarKE")
st.title("Kenyan Money Market Fund Comparison")

# initializing the database as well as the session state for user authentication

init_db()
if "user" not in st.session_state:
    st.session_state["user"] = None

# The user authentication in the sidebar coz why not
st.sidebar.header("User Authentication")

if st.session_state["user"] is None:

    auth_action = st.sidebar.selectbox("Action", ["Login", "Sign Up"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button(auth_action):

        if auth_action == "Sign Up":
            if add_user(username, password):
                st.sidebar.success("User registered successfully! Please log in.")
            else:
                st.sidebar.error("sorry brother, not today!, try a different username.")

        elif auth_action == "Login":
            if verify_user(username, password):
                st.session_state["user"] = username
                st.sidebar.success(f"Login successful! Welcome {username}")
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password.")

else:

    st.sidebar.write(f"Holaaaa @ *{st.session_state['user']}*")
    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
        st.rerun()

# The main dashboard that shows the data and charts only if the user is logged in

if st.session_state["user"]:
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

    # Creating a chart for data analysis
    st.subheader("Top 5 Funds by Net Return")
    top5 = sorted_funds[:5]

    chart_data = {f.name: f.net_return() for f in top5}

    st.bar_chart(list(chart_data.values()))
    st.write("Funds (left to right):", ", ".join(chart_data.keys()))
else:
    st.warning("Please log in to view the dashboard.")

    # --- Footer ---
st.markdown("""---""")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 14px;'>
        Built with love and passion using <a href='https://streamlit.io' target='_blank'>Streamlit</a>  
        | Data: Kenyan Money Market Funds (Dummy for Demo)  
        <br>
        © 2025 DollarKE Capstone Project by Brian
    </div>
    """,
    unsafe_allow_html=True
)