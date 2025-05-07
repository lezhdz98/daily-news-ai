import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from datetime import date
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")

async def search_and_process_articles(region: str = "International", categories: str = "politics, sports, finance") -> str:
    """
    Searches articles based on region and categories, then processes the articles with LLM.

    Args:
        region (str): Region to focus the search on (e.g., "USA", "Mexico", etc.).
        categories (str): Categories to filter the articles by (e.g., "politics", "sports", etc.).

    Returns:
        str: Processed result of the articles.
    """

    categories = categories.lower().split(", ")

    string_sources = ""

    valid_categories = {
        "politics": (
            "### Politics\n"
            "- The Hill: https://thehill.com/\n"
            "- BBC Politics: https://www.bbc.com/news/politics\n"
            "- Politico: https://www.politico.com/\n\n"
        ),
        "finance": (
            "### Business & Economy\n"
            "- CNBC: https://www.cnbc.com/\n"
            "- Bloomberg: https://www.bloomberg.com/\n\n"
        ),
        "technology": (
            "### Technology\n"
            "- TechCrunch: https://techcrunch.com/\n"
            "- The Verge: https://www.theverge.com/tech\n"
            "- Geekwire: https://www.geekwire.com/\n\n"
        ),
        "science": (
            "### Science\n"
            "- ScienceDaily: https://www.sciencedaily.com/\n"
            "- Scientific American: https://www.scientificamerican.com/\n"
            "- NASA News: https://www.nasa.gov/news\n\n"
        ),
        "health": (
            "### Health\n"
            "- Healthline: https://www.healthline.com/\n"
            "- WebMD: https://www.webmd.com/news\n"
            "- WHO News: https://www.who.int/news\n\n"
        ),
        "sports": (
            "### Sports\n"
            "- BBC Sport: https://www.bbc.com/sport\n"
            "- ESPN: https://www.espn.com/\n"
            "- Bleacher Report: https://bleacherreport.com/\n\n"
        ),
        "entertainment": (
            "### Entertainment\n"
            "- Variety: https://variety.com/\n"
            "- Entertainment Weekly: https://ew.com/\n"
            "- The Verge – Entertainment: https://www.theverge.com/entertainment\n\n"
        ),
        "lifestyle": (
            "### Lifestyle\n"
            "- VICE Life: https://www.vice.com/en/section/life\n"
            "- Refinery29: https://www.refinery29.com/\n"
            "- NYTimes Style: https://www.nytimes.com/section/style\n\n"
        ),
        "education": (
            "### Education\n"
            "- Edutopia: https://www.edutopia.org/\n"
            "- Inside Higher Ed: https://www.insidehighered.com/\n"
            "- Education Week: https://www.edweek.org/\n\n"
        ),
        "opinion": (
            "### Opinion\n"
            "- The Guardian Opinion: https://www.theguardian.com/uk/commentisfree\n"
            "- CNN Opinion: https://edition.cnn.com/opinions\n"
            "- Al Jazeera Opinion: https://www.aljazeera.com/opinions/\n\n"
        ),
        "crime & law": (
            "### Crime & Law\n"
            "- Law & Crime: https://lawandcrime.com/\n"
            "- Reuters Crime/Legal: https://www.reuters.com/legal/\n\n"
        ),
        "environment": (
            "### Environment\n"
            "- Mongabay: https://news.mongabay.com/\n"
            "- Grist: https://grist.org/\n"
            "- National Geographic Environment: https://www.nationalgeographic.com/environment/\n\n"
        )
    }

    for category in categories:
        if category not in valid_categories:
            raise ValueError(f"Invalid category: {category}. Allowed categories are: {', '.join(valid_categories.keys())}")
        string_sources += valid_categories[category]

    today = date.today().strftime("%B %d, %Y")

    task = (
        f"Search for news articles published today ({today}) in the specified region: {region}.\n"
        f"Focus on the following categories: {categories}.\n\n"
        "Use only the following trusted sources for each category:\n\n"
        f"{string_sources}\n"
        "Visit each site and extract the latest 1–2 headlines that are relevant to the category.\n\n"
        "Return only in **markdown format** with:\n"
        "- The **article title**\n"
        "- A **full summary** of the article (not just the lead paragraph)\n"
        "- The **URL** to the article\n\n"
        "Do not include ads, navigation menus, unrelated content, or metadata. Focus on accurate and clear summaries of the articles."
    )


    print("\n=== TASK ===\n")
    print(task)

    # Initialize the browser agent with LLM and the task description
    agent = Agent(
        task=task,
        llm=llm,
    )

    # Run the agent asynchronously and fetch the result
    result = await agent.run()

    return result

async def main():
    # Call the function with your desired region and categories
    articles_summary = await search_and_process_articles(
        region="USA", categories="sports"
    )
    print("\n=== Summarized Articles ===\n")
    print(articles_summary.final_result())
    print("\n=== END ===\n")

# Run the asynchronous main function
asyncio.run(main())
