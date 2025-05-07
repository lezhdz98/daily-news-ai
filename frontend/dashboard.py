import streamlit as st
import sys
from utils import generate_pdf
import time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.browser_agent import search_and_process_articles, main


def search_news(categories, language, sources, summary_type, location, style):
    return {}


# Page configuration
st.set_page_config(
    page_title="Daily News Browser AI Agent",
    page_icon="🗞️",
    layout="wide",
)

st.title("Daily News Browser AI Agent")
st.caption("Tool that uses an AI agent to browse the web and summarize news articles.")

# Initalize state
state_defaults = {
    "waiting": False,
    "search_result": None,
    "error_message": None
}

for key, value in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- FORM SECTION ---
st.markdown("### Search configuration")
st.caption("Select the desired parameters for the news search. The AI agent will use these parameters to browse the web and summarize the news articles.")
col1, col2 = st.columns(2, gap="medium")
with col1:
    categories = st.multiselect(
        "Categories",
        options=["Politics", "Finance", "Technology", "Science", "Health", "Sports", "Entertainment", "Lifestyle", "Education", "Opinion", "Crime & Law", "Environmnet"],
        default=["Politics"],
        max_selections=3
    )
    
    
with col2:
    location = st.selectbox(
        "Location",
        options=["International", "USA", "Mexico"],
        index=0,
    )
    
col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    style = st.selectbox("Symmary Style", ["Formal", "Informal", "Funny", "Technical"])
with col2:
    summary_type = st.selectbox("Summary Type", ["Concise", "Detailed"])
with col3:
    language = st.selectbox("Language", ["en", "es", "fr", "de"], index=0)
submitted = st.button("Search", disabled=st.session_state.waiting)

# If button was clicked and not waiting
if submitted and not st.session_state.waiting:
    st.session_state.waiting = True
    st.session_state.search_result = None
    st.session_state.summary_result = None
    st.session_state.error_message = None
    st.rerun()  # Ensure rerun so the button shows disabled on next render

if st.session_state.error_message:
    st.error(st.session_state.error_message)

# --- LOADING SECTION ---
# After rerun, if waiting is True, start the processing
if st.session_state.waiting and not st.session_state.search_result:
    try:
        with st.status("Searching the web...", state="running", expanded=True) as s:
            # Only upload video if its a new file
            st.toast('Searching the web...')
            s.update(label="Looking for news articles...", state="running")
            time.sleep(1)
            st.session_state.search_result = None
            if st.session_state.search_result == None:
                raise Exception("Error while looking for news, try again later...")
            
            st.toast('News articles looked successfully!', icon='✅')

            s.update(label="Loading results...", state="complete")
            st.toast('Loading results...')
            time.sleep(2)
            
    except Exception as e:
        st.session_state.error_message = f"Error during processing: {e}"
    finally:
        st.session_state.waiting = False
        st.rerun()  # Final rerun to re-enable the button and display results

# --- RESULTS SECTION ---
if st.session_state.search_result:
    result = st.session_state.search_result
    st.markdown("---")
    st.markdown("## News Summary")
    # Download button for PDF
    file_name, data = generate_pdf(result)
    st.download_button("Download PDF", data, file_name)

    for category, data in result.items():
        st.markdown(f"#### {category}")
        st.info(data["summary"]) 

        for article in data["articles"]:
            with st.expander(f"{article['title']} — *{article['source']}*"):
                st.markdown(f"**Description**: {article['description']}")
                st.markdown(f"**Location**: {article['location']}")
                st.markdown(f"[🔗 Read full article]({article['url']})", unsafe_allow_html=True)