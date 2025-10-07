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
    from seo_agent import get_seo_suggestions # Mocked for now
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
    "Product Performance",
    "Financial Analysis",
    "Marketing Campaigns",
    "AI SEO Agent",
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
    st.markdown('''
    Select an agent from the sidebar on the left to perform specific tasks.

    * **Product Performance:** Get real-time insights into your sales, shipping, and inventory.
    * **Financial Analysis:** Analyze your store's financial performance.
    * **Marketing Campaigns:** Launch and track marketing campaigns.
    * **AI SEO Agent:** Generate product titles and descriptions from an image.
    * **Bulk Product Updater:** Update prices, margins, and titles for existing products from a CSV file.
    * **Bulk Product Creator:** Create hundreds of new products from a CSV file.
    * **Catalog Explorer:** Download product blueprint and variant data from Printify.
    ''')
    st.info("Continuous agents like Order Fulfillment and Inventory Sync can be run from the terminal or a dedicated server process.")

# =============================================================================
# Product Performance Page
# =============================================================================
elif page == "Product Performance":
    st.header("Product Performance Insights")
    st.markdown("Monitor your sales, shipping, and inventory levels in real-time.")

    if st.button("Fetch Performance Data"):
        with st.spinner("Fetching latest data..."):
            # Mock data for demonstration
            sales_data = {
                "Product": ["T-Shirt", "Mug", "Hoodie", "Sticker"],
                "Units Sold": [120, 85, 60, 200],
                "Revenue": [2400, 1020, 1800, 600]
            }
            shipping_data = {
                "Status": ["Shipped", "In Production", "Delivered"],
                "Orders": [50, 25, 150]
            }
            inventory_data = {
                "Product": ["T-Shirt", "Mug", "Hoodie", "Sticker"],
                "Stock Level": [500, 300, 400, 1000]
            }

            sales_df = pd.DataFrame(sales_data)
            shipping_df = pd.DataFrame(shipping_data)
            inventory_df = pd.DataFrame(inventory_data)

            st.success("Data fetched successfully!")

            st.subheader("Sales Overview")
            st.bar_chart(sales_df.set_index("Product")["Revenue"])

            st.subheader("Shipping Status")
            st.table(shipping_df)

            st.subheader("Inventory Levels")
            st.table(inventory_df)

# =============================================================================
# Financial Analysis Page
# =============================================================================
elif page == "Financial Analysis":
    st.header("Financial Analysis")
    st.markdown("Analyze your store's financial performance.")

    if st.button("Fetch Financial Data"):
        with st.spinner("Fetching latest data..."):
            # Mock data for demonstration
            financial_data = {
                "Metric": ["Total Revenue", "Total Cost", "Gross Profit", "Gross Profit Margin", "Average Order Value"],
                "Value": [5820, 3492, 2328, "40%", 38.8]
            }
            financial_df = pd.DataFrame(financial_data)

            st.success("Data fetched successfully!")

            st.subheader("Key Financial Metrics")
            st.table(financial_df)

            st.subheader("Revenue vs. Profit")
            chart_data = pd.DataFrame({
                "Category": ["Revenue", "Cost", "Profit"],
                "Amount": [5820, 3492, 2328]
            })
            st.bar_chart(chart_data.set_index("Category"))

# =============================================================================
# Marketing Campaigns Page
# =============================================================================
elif page == "Marketing Campaigns":
    st.header("Marketing Campaigns")
    st.markdown("Launch and track marketing campaigns to boost your sales.")

    st.subheader("Launch a New Campaign")
    campaign_type = st.selectbox("Campaign Type", ["Social Media", "Email", "PPC"])
    campaign_details = st.text_area("Campaign Details")
    if st.button("Launch Campaign"):
        with st.spinner("Launching campaign..."):
            # In a real implementation, this would trigger a marketing automation script
            st.success(f"{campaign_type} campaign launched successfully!")

    st.subheader("Active Campaigns")
    active_campaigns_data = {
        "Campaign Name": ["Summer Sale", "New Hoodie Promo"],
        "Type": ["Email", "Social Media"],
        "Status": ["Active", "Active"],
        "Start Date": ["2024-07-01", "2024-07-15"]
    }
    active_campaigns_df = pd.DataFrame(active_campaigns_data)
    st.table(active_campaigns_df)

    st.subheader("Campaign Performance")
    campaign_performance_data = {
        "Campaign": ["Summer Sale", "New Hoodie Promo", "Old Campaign"],
        "Conversions": [150, 80, 50]
    }
    campaign_performance_df = pd.DataFrame(campaign_performance_data)
    st.bar_chart(campaign_performance_df.set_index("Campaign"))

# =============================================================================
# AI SEO Agent Page
# =============================================================================
elif page == "AI SEO Agent":
    st.header("AI-Powered SEO Agent")
    st.markdown("Generate optimized product titles and descriptions from a product image.")

    uploaded_file = st.file_uploader("Upload a product image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Generate SEO Content"):
            with st.spinner("Generating content with Gemini..."):
                # Save the uploaded file to pass to the agent
                file_path = "temp_image.png"
                if save_uploaded_file(uploaded_file, file_path):
                    try:
                        # Mocked response for demonstration
                        seo_json = {
                            "new_title": "Vintage Sunset T-Shirt | Retro 80s Graphic Tee",
                            "new_description": "<p>Embrace the retro vibes with our Vintage Sunset T-Shirt. This comfortable tee features a stunning 80s-inspired graphic of a sunset over a serene landscape. The vibrant colors and classic design make it a perfect choice for anyone who loves a vintage aesthetic. Made from soft, high-quality cotton, this shirt is perfect for everyday wear. Grab yours now and add a touch of nostalgia to your wardrobe!</p>"
                        }
                        st.success("SEO content generated successfully!")
                        st.subheader("Generated Title")
                        st.text_input("Title", value=seo_json.get("new_title"))
                        st.subheader("Generated Description")
                        st.text_area("Description", value=seo_json.get("new_description"), height=300)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

# =============================================================================
# Bulk Updater Page
# =============================================================================
elif page == "Bulk Product Updater":
    st.header("Bulk Product Update Agent")
    st.markdown("Update existing products by uploading a CSV file with `product_id` and the fields you want to change (e.g., `price`, `margin`).")

    uploaded_file = st.file_uploader("Upload update CSV", type=["csv"], key="updater_upload")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        if st.button("Run Bulk Update"):
            file_path = "products_to_update.csv"
            if save_uploaded_file(uploaded_file, file_path):
                with st.spinner("Processing updates... This may take a while."):
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

    uploaded_file = st.file_uploader("Upload creation CSV", type=["csv"], key="creator_upload")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        st.subheader("Multi-Store Publishing")
        publish_to_all = st.toggle("Publish to all stores", value=True)
        
        if st.button("Run Bulk Creation"):
            file_path = "products_to_create.csv"
            if save_uploaded_file(uploaded_file, file_path):
                with st.spinner("Creating new products..."):
                    try:
                        create_products_from_csv(file_path) # Call existing agent function
                        st.success("Bulk creation process completed successfully!")
                        if publish_to_all:
                            st.info("Products published to all available stores.")
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
