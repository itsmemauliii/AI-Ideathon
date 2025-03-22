import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
import streamlit as st

openai_key = st.secrets["OPENAI_API_KEY"]
tavily_key = st.secrets["TAVILY_API_KEY"]

import toml

# Load secrets from TOML file
secrets = toml.load("src/secrets.toml")

openai_key = secrets["OPENAI_API_KEY"]
tavily_key = secrets["TAVILY_API_KEY"]

# Tavily Search Tool
def scrape_news():
    tool = TavilySearchResults(
        max_results=10,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_domains=["insurancejournal.com", "reinsurancene.ws"]
    )
    response = tool.invoke({"query": "Climate risk and Insurance 2024"})
    return response

# Structure News Response
def structure_the_response(response):
    structured = []

    # If response is already a list, just loop through it.
    for article in response:  
        structured.append({
            "title": article.get("title", "No Title"),
            "source": article.get("source", {}).get("name", "Unknown Source"),
            "date": article.get("published_at", "Unknown Date"),
            "summary": article.get("snippet", "No Summary"),
            "tags": ["climate risk", "insurance"]  # You can customize tags or auto-detect with NLP later
        })

    return structured

# Search for Research References
def find_research_references(structured_response):
    enriched = []
    for item in structured_response:
        query = item["title"] + " site:arxiv.org"
        tool = TavilySearchResults(max_results=5)
        research_results = tool.invoke({"query": query})
        enriched.append({
            "news": item,
            "research_refs": research_results.get("results", [])
        })
    return enriched

# Streamlit Dashboard UI
def run_dashboard(data):
    st.title("Climate Risk & Insurance Insights Dashboard")

    st.sidebar.header("Filter by Tag")
    tags = sorted(set(tag for item in data for tag in item["news"]["tags"]))
    selected_tag = st.sidebar.selectbox("Select Tag", tags)

    for item in data:
        if selected_tag in item["news"]["tags"]:
            news = item["news"]
            st.subheader(news["title"])
            st.caption(f"{news['source']} | {news['date']}")
            st.write(news["summary"])

            st.markdown("### Research References")
            for ref in item["research_refs"]:
                st.write(f"- {ref['title']} ({ref['source']['name']})")

            st.markdown("---")
