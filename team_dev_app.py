import pandas as pd
import streamlit as st
import os

# File path to the Excel file
file_path = r"C:\Users\MWA27\OneDrive - Sky\Documents\Coaches Meeting Feb 2025.xlsx"

# Function to load the Team Development sheet
def load_team_dev_sheet():
    if not os.path.exists(file_path):
        st.error("File not found. Please upload the Excel file.")
        return None
    return pd.read_excel(file_path, sheet_name='Team Development')

# Function to save the updated Team Development sheet
def save_team_dev_sheet(df):
    if df is not None:
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name='Team Development', index=False)
        st.success("Data saved successfully!")

def main():
    st.title("Team Development Tracker")
    
    if not os.path.exists(file_path):
        uploaded_file = st.file_uploader("Upload the Excel file", type=['xlsx'])
        if uploaded_file:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded successfully!")
    
    df = load_team_dev_sheet()
    if df is None:
        return
    
    # Extract player names and categories
    players = df.iloc[2:, 0].dropna().tolist()
    categories = df.iloc[0, 1:].dropna().tolist()
    
    selected_player = st.selectbox("Select a Player", players)
    
    if selected_player:
        player_row = df[df.iloc[:, 0] == selected_player].index[0]
        player_data = df.iloc[player_row, 1:]
        
        st.subheader(f"Updating Development for {selected_player}")
        updated_data = {}
        
        for idx, category in enumerate(categories):
            value = st.text_input(f"{category}", value=str(player_data.iloc[idx]) if not pd.isna(player_data.iloc[idx]) else "")
            updated_data[idx + 1] = value
        
        if st.button("Save Data"):
            for col_idx, val in updated_data.items():
                df.iloc[player_row, col_idx] = val
            save_team_dev_sheet(df)

if __name__ == "__main__":
    main()