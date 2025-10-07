
import streamlit as st
from seo_agent import run_seo_optimizer, update_product_seo

st.set_page_config(layout="wide")

st.title("🤖 AI-Powered SEO Agent")

# --- Session State Initialization ---
if 'seo_data' not in st.session_state:
    st.session_state.seo_data = None
if 'error' not in st.session_state:
    st.session_state.error = None
if 'update_status' not in st.session_state:
    st.session_state.update_status = None

# --- UI for Product ID Input ---
st.subheader("Step 1: Fetch and Analyze Product")
product_id = st.text_input("Enter Printify Product ID:", placeholder="e.g., 65a8a5b5b37603be04022acb")

if st.button("✨ Generate SEO Suggestions"):
    st.session_state.seo_data = None
    st.session_state.error = None
    st.session_state.update_status = None
    if product_id:
        with st.spinner("Calling the AI... This may take a moment..."):
            result = run_seo_optimizer(product_id)
            if "error" in result:
                st.session_state.error = result
            else:
                st.session_state.seo_data = result
    else:
        st.warning("Please enter a Product ID.")

# --- Display Errors ---
if st.session_state.error:
    st.error(f"**Error:** {st.session_state.error.get('error')}")
    if 'raw_response' in st.session_state.error:
        st.code(st.session_state.error.get('raw_response'), language='text')

# --- Display SEO Suggestions ---
if st.session_state.seo_data:
    data = st.session_state.seo_data
    st.subheader("Step 2: Review and Approve SEO Changes")

    col1, col2 = st.columns(2)

    with col1:
        st.image(data['image_url'], caption="Product Image", use_column_width=True)

    with col2:
        st.info("**Original Content**")
        st.text_input("Original Title", data['original_title'], disabled=True)
        st.text_area("Original Description", data['original_description'], height=200, disabled=True)
        
        st.success("**AI-Generated Suggestions**")
        new_title = st.text_input("New Title", data['new_title'])
        new_description = st.text_area("New Description (HTML)", data['new_description'], height=200)
        
        # Update session state if user edits the suggested text
        data['new_title'] = new_title
        data['new_description'] = new_description


    # --- Button to Update Product ---
    st.subheader("Step 3: Update Product on Printify")
    if st.button("🚀 Approve and Update Product", key="update_button"):
        with st.spinner("Updating product on Printify..."):
            update_result = update_product_seo(product_id, data['new_title'], data['new_description'])
            st.session_state.update_status = update_result

# --- Display Update Status ---
if st.session_state.update_status:
    if st.session_state.update_status.get("success"):
        st.balloons()
        st.success(st.session_state.update_status.get("message"))
    else:
        st.error(f"**Update Failed:** {st.session_state.update_status.get('message')}")
