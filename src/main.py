# Main application script
from utils import (
    scrape_news,
    structure_the_response,
    find_research_references,
    run_dashboard
)

def main():
    # Scrape News
    news_data = scrape_news()

    # Structure the responses
    structured_news = structure_the_response(news_data)

    # Find matching research papers
    enriched_news = find_research_references(structured_news)

    # Launch the dashboard
    run_dashboard(enriched_news)

if __name__ == "__main__":
    main()
