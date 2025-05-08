import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from datetime import date
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")

async def search_and_process_articles(
    categories: str = "politics, sports, finance", 
    summary_type: str = "detailed", 
    summary_style: str = "formal",
    summary_language: str = "English"
) -> str:
    """
    Searches articles based on region and categories, then processes the articles with LLM.

    Args:
        region (str): Region to focus the search on (e.g., "USA", "Mexico", etc.).
        categories (str): Categories to filter the articles by (e.g., "politics", "sports", etc.).

    Returns:
        str: Processed result of the articles.
    """

    categories = categories.lower().split(",")

    string_sources = ""

    valid_categories = {
        "politics": "### Politics\n- Politico: https://www.politico.com/\n\n",
        "finance": "### Business & Economy\n- Bloomberg: https://www.bloomberg.com/\n\n",
        "technology": "### Technology\n- TechCrunch: https://techcrunch.com/\n",
        "science": "### Science\n- ScienceDaily: https://www.sciencedaily.com/\n",
        "health": "### Health\n- Healthline: https://www.healthline.com/\n",
        "sports": "### Sports\n- CNN Sport: https://edition.cnn.com/sport\n",
        "entertainment": "### Entertainment\n- Entertainment Weekly: https://ew.com/\n",
        "lifestyle": "### Lifestyle\n- VICE Life: https://www.vice.com/en/section/life\n",
        "education": "### Education\n- Edutopia: https://www.edutopia.org/\n",
        "opinion": "### Opinion\n- The Guardian Opinion: https://www.theguardian.com/uk/commentisfree\n",
        "crime & law": "### Crime & Law\n- Law & Crime: https://lawandcrime.com/\n",
        "environment": "### Environment\n- National Geographic Environment: https://www.nationalgeographic.com/environment/\n\n"
    }

    for category in categories:
        if category not in valid_categories:
            raise ValueError(f"Invalid category: {category}. Allowed categories are: {', '.join(valid_categories.keys())}")
        string_sources += valid_categories[category]

    if(summary_type.lower() == "concise"):
        summary_type_prompt = "concise (less than 100 words per article)"
    else:
        summary_type_prompt = "detailed"
    
    today = date.today().strftime("%B %d, %Y")

    task = (
        f"Search for news articles published today ({today})\n"
        f"Focus on the following categories: {categories}.\n"
        "Use only the trusted sources listed for each category.\n" 
        "If no relevant articles are found after checking all sources for a category, "
        "clearly state that no results were found for that category .\n\n" 
        f"{string_sources}\n"
        "Visit each site and extract the latest 1–2 headlines that are relevant to the category.\n\n"
        "Extract the latest 1–2 headlines that are relevant to each category. You must find maximum up to TWO Articles by category.\n\n"
        f"Return all results in **markdown format** and in **{summary_language}**.\n\n"
        "For each article, include:\n"
        "- The **article title**\n"
        f"- A **comprehensive summary** written in a **{summary_type_prompt}** manner and a **{summary_style}** tone\n"
        "- The **URL** to the article\n\n"
        "Exclude ads, navigation menus, unrelated content, and metadata. Focus solely on accurate and clear summaries of the article content.\n\n"
        "Don't hallucinate or make up information. If you don't know a specific detail or field, ignore it and leave it blank.\n\n"
    )

    print("\n=== TASK ===\n")
    print(task)

    # Initialize the browser agent with LLM and the task description
    agent = Agent(
        task=task,
        llm=llm,
        save_conversation_path='conversation.txt',
    )

    # Run the agent asynchronously and fetch the result
    result = await agent.run()

    return result

async def main():
    # Call the function with your desired region and categories
    articles_summary = await search_and_process_articles()
    print("\n=== Summarized Articles ===\n")
    print(articles_summary.final_result())
    print("\n=== END ===\n")

# Only run the main function if this script is executed directly
if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
