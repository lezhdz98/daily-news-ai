import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from datetime import date
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")

async def search_and_process_articles(
    categories: list[str],
    summary_type: str = "detailed", 
    summary_style: str = "formal",
    summary_language: str = "English"
) -> str:
    """
    Searches for news articles published today based on the specified categories,
    then processes and summarizes them using a language model.

    Args:
        categories (list[str]): List of categories to filter articles by (e.g., "politics", "sports", "finance").
        summary_type (str): Type of summary to generate, e.g., "detailed" or "concise".
        summary_style (str): Tone/style of the summary, e.g., "formal", "humorous".
        summary_language (str): Language in which the summary should be written, e.g., "English", "Spanish".

    Returns:
        str: A markdown-formatted string containing the article titles, summaries, and URLs.
    """

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

    # Define the task for the agent
    task = (
        f"Search for news articles published **today** ({today}).\n\n"
        f"Focus only on these categories: {categories}.\n"
        "Use **only** the trusted sources listed below for each category.\n\n"
        f"{string_sources}\n"
        
        "For each category:\n"
        "- Visit each source listed.\n"
        "- Extract **up to 2 recent headlines** that are relevant.\n"
        "- Go to the article page and extract the **main content**.\n"
        "- If **no relevant articles** are found after checking all sources, clearly state: 'No results found for this category.'\n\n"
        
        f"For each article, provide the following in **markdown format** and in **{summary_language} language**:\n"
        "- **Title** of the article\n"
        f"- A **comprehensive summary** in a **{summary_type_prompt}** manner and **{summary_style}** tone\n"
        "- **Direct URL** to the article, dont hallucinate the URL, save the actual link of the article\n\n"

        "Important guidelines:\n"
        "- **Exclude** ads, unrelated content, menus, or metadata.\n"
        "- **Do not hallucinate or fabricate** any information.\n"
        "- If a detail is unknown or unavailable, leave it blank without guessing.\n"
    )


    print("\n=== TASK ===\n")
    print(task)

    # Initialize the browser agent with LLM and the task description
    agent = Agent(
        task=task,
        llm=llm
    )

    # Run the agent asynchronously and fetch the result
    result = await agent.run()

    return result

async def main():
    # Call the function with your desired categories
    articles_summary = await search_and_process_articles(["politics", "finance"], summary_type="detailed", summary_style="Humorous", summary_language="English")
    print("\n=== Summarized Articles ===\n")
    print(articles_summary.final_result())
    print("\n=== END ===\n")

# Only run the main function if this script is executed directly
if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
