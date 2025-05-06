import streamlit as st
import time

def search_news(categories, language, sources, summary_type, location, style):
    # Simulate a search operation
    time.sleep(2)
    result = {
        "Technology": {
            "summary": "Tech headlines today focused on AI breakthroughs and new product launches. OpenAI introduced GPT-5, while Apple unveiled a new AR headset.",
            "articles": [
                {
                    "category": "Technology",
                    "title": "OpenAI Releases GPT-5",
                    "description": "OpenAI has announced the release of GPT-5, offering major improvements in reasoning and multimodal capabilities.",
                    "url": "https://example.com/openai-gpt5",
                    "source": "CNN",
                    "language": "en",
                    "location": "International"
                },
                {
                    "category": "Technology",
                    "title": "Apple Launches New AR Headset",
                    "description": "Apple has revealed its latest innovation: an AR headset aimed at enhancing digital experiences.",
                    "url": "https://example.com/apple-ar-headset",
                    "source": "BBC",
                    "language": "en",
                    "location": "USA"
                }
            ]
        },
        "Health": {
            "summary": "The WHO issued new guidelines on mental health support, while research shows benefits of walking for older adults.",
            "articles": [
                {
                    "category": "Health",
                    "title": "WHO Updates Mental Health Guidelines",
                    "description": "New WHO guidelines aim to improve access to mental health support globally.",
                    "url": "https://example.com/who-mental-health",
                    "source": "The Guardian",
                    "language": "en",
                    "location": "International"
                },
                {
                    "category": "Health",
                    "title": "Walking Benefits for Older Adults",
                    "description": "A new study highlights the physical and cognitive benefits of daily walking for people over 60.",
                    "url": "https://example.com/walking-study",
                    "source": "Vox",
                    "language": "en",
                    "location": "USA"
                }
            ]
        }
    }

    print(f"Found {len(categories)} articles in {language} from {sources}.")
    return result

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
    "summary_result": None,
    "error_message": None
}

for key, value in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- FORM SECTION ---
st.markdown("### Search configuration")
st.caption("Select the desired parameters for the news search. The AI agent will use these parameters to browse the web and summarize the news articles.")
col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    categories = st.multiselect(
        "Categories",
        options=["Technology", "Health", "Finance", "Sports", "Entertainment", "Politics"],
        default=["Technology"],
        max_selections=3
    )
    language = st.selectbox("Language", ["en", "es", "fr", "de"], index=0)
    
with col2:
    sources = st.multiselect(
        "News sources",
        options=["CNN", "BBC", "Vox", "The Guardian", "New York Times"],
        default=["CNN"],
        max_selections=3
    )
    summary_type = st.selectbox("Summary Type", ["Concise", "Detailed"])
    

with col3:
    location = st.selectbox(
        "Location",
        options=["International", "USA", "Mexico"],
        index=0,
    )
    style = st.selectbox("Symmary Style", ["Formal", "Informal", "Funny", "Technical"])

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
            time.sleep(5)
            st.session_state.search_result = search_news(categories=categories, language=language, sources=sources, summary_type=summary_type, location=location, style=style)
            if st.session_state.search_result == None:
                raise Exception("Error while looking for news, try again later...")
            
            st.toast('News articles looked successfully!', icon='✅')
            st.toast('Generating news summary...')
            s.update(label="Summarizing news articles...", state="running")
            time.sleep(5)
            results = None
            st.session_state.analysis_result = None

            s.update(label="Summary completed!", state="complete")
            st.toast('Summary completed!', icon='✅')
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

    for category, data in result.items():
        st.markdown(f"#### {category}")
        st.info(data["summary"]) 

        for article in data["articles"]:
            with st.expander(f"{article['title']} — *{article['source']}*"):
                st.markdown(f"**Description**: {article['description']}")
                st.markdown(f"**Location**: {article['location']}")
                st.markdown(f"[🔗 Read full article]({article['url']})", unsafe_allow_html=True)