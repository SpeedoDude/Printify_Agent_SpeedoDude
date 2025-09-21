# dashboard.py

import streamlit as st
import pandas as pd
import os

# --- Import agent functions ---
# Note: We may need to slightly modify agent functions later to better integrate with Streamlit,
# especially for capturing real-time log output.
try:
    from catalog_explorer import run_explorer # Assumes this prints to console or returns data
    from bulk_creator import create_products_from_csv
    from bulk_updater import update_products_from_csv
    # Import other agents as needed...
except ImportError as e:
    st.error(f"Error importing agent scripts: {e}. Ensure all files are in the same directory.")

# --- Helper function to save uploaded file ---
def save_uploaded_file(uploaded_file, file_path):
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False

# =============================================================================
# Streamlit App Layout
# =============================================================================

st.set_page_config(layout="wide", page_title="Printify Agent Dashboard")
st.title("🤖 Printify Agent Control Panel")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose an Agent", [
    "Home", 
    "Bulk Product Updater", 
    "Bulk Product Creator",
    "Catalog Explorer"
    # Add other agents here: "Order Fulfillment", "Inventory Sync"
])

# =============================================================================
# Home Page
# =============================================================================
if page == "Home":
    st.header("Welcome to Your Automated Store Manager")
    st.markdown("""
    Select an agent from the sidebar on the left to perform specific tasks.
    
    * **Bulk Product Updater:** Update prices, margins, and titles for existing products from a CSV file.
    * **Bulk Product Creator:** Create hundreds of new products from a CSV file.
    * **Catalog Explorer:** Download product blueprint and variant data from Printify.
    """)
    st.info("Continuous agents like Order Fulfillment and Inventory Sync can be run from the terminal or a dedicated server process.")

# =============================================================================
# Bulk Updater Page
# =============================================================================
elif page == "Bulk Product Updater":
    st.header("Bulk Product Update Agent")
    st.markdown("Update existing products by uploading a CSV file with `product_id` and the fields you want to change (e.g., `price`, `margin`).")

    # File uploader
    uploaded_file = st.file_uploader("Upload update CSV", type=["csv"], key="updater_upload")
    
    if uploaded_file is not None:
        # Display a preview of the uploaded data
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        # Run button
        if st.button("Run Bulk Update"):
            # Save the uploaded file to the path expected by the script
            file_path = "products_to_update.csv"
            if save_uploaded_file(uploaded_file, file_path):
                with st.spinner("Processing updates... This may take a while."):
                    # --- Call the agent logic ---
                    # For a truly interactive experience, we would capture stdout here.
                    # For now, we call the script and show a success message.
                    try:
                        update_products_from_csv(file_path) # Call existing agent function
                        st.success("Bulk update process completed successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"An error occurred during the update process: {e}")

# =============================================================================
# Bulk Creator Page
# =============================================================================
elif page == "Bulk Product Creator":
    st.header("Bulk Product Creator Agent")
    st.markdown("Create new products by uploading a CSV file with product details.")

    # File uploader
    uploaded_file = st.file_uploader("Upload creation CSV", type=["csv"], key="creator_upload")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        if st.button("Run Bulk Creation"):
            file_path = "products_to_create.csv"
            if save_uploaded_file(uploaded_file, file_path):
                with st.spinner("Creating new products..."):
                    try:
                        create_products_from_csv(file_path) # Call existing agent function
                        st.success("Bulk creation process completed successfully!")
                    except Exception as e:
                        st.error(f"An error occurred during creation: {e}")

# =============================================================================
# Catalog Explorer Page
# =============================================================================
elif page == "Catalog Explorer":
    st.header("Catalog Explorer Agent")
    st.markdown("Tools to explore the Printify catalog.")
    
    if st.button("Export All Blueprints to CSV"):
        st.info("This feature would run the `list_all_blueprints` function and provide a download link.")
        # In a real implementation:
        # list_all_blueprints() # This function needs modification to return a file path or data
        # with open("printify_blueprints.csv", "rb") as file:
        #     st.download_button(label="Download Blueprints CSV", data=file, file_name="printify_blueprints.csv")

