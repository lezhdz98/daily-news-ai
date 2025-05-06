from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def summarize_news_articles(
    articles: str,
    language: str = "English",
    region: str = "International",
    categories: str = "politics, sports, finance",
    tone: str = "Formal",
    type: str = "Detailed"
) -> str:
    """
    Summarizes news articles using GPT model with customization options.

    Args:
        articles (str): Raw article content.
        language (str): Language of the output summary.
        region (str): Geographical focus.
        categories (str): list of categories.
        tone (str): Desired tone of the summary (Formal, Conversational, Humurous).
        type (str): Level of detail (concise or Detailed).

    Returns:
        str: Summary in Markdown format.
    """

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert assistant that summarizes multiple news articles into a structured report. "
            "All articles belong to the following categories only: {categories}. "
            "Write the summary in {language}, targeting readers interested in news from the {region}. "
            "Use a {tone} tone in your writing. "
            "If the summary type is 'Concise', limit each category summary to about 100 words per category. If 'Detailed', provide a fuller overview. "
            "Organize the output by category using Markdown headers, like this:\n\n"
            "## Politics\nSummary here\n\n## Finance\nSummary here\n\n"
            "Only include the categories that appear in the input articles. Format the final output in clean, readable Markdown."

        ),
        ("human", "{articles}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "language": language,
        "region": region,
        "categories": categories,
        "tone": tone,
        "type": type,
        "articles": articles
    })

    return response.content


if __name__ == "__main__":
    # Example article string (you can replace this with real content)
    sample_articles = """
    [Politics] President Smith announced a new climate policy aimed at reducing emissions by 40% over the next decade.
    [Finance] The stock market saw a sharp decline today following disappointing tech earnings.
    [Sports] The national soccer team secured a dramatic win in the final moments of the World Cup qualifier.
    """

    summary = summarize_news_articles(
        articles=sample_articles,
        language="English",
        region="International",
        categories="politics, sports, finance",
        tone="Formal",
        type="Concise"
    )

    print("\n=== Generated Summary ===\n")
    print(summary)
