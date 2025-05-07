import time
from markdown_pdf import MarkdownPdf, Section


def generate_pdf(articles):
    """Generate a PDF report file from the search and summary results."""
    markdown = f"# Daily News Summary\n *{time.strftime("%Y-%m-%d")}*\n\n"
    for category, data in articles.items():
        summary = data["summary"]
        articles = data["articles"]
        markdown += f"## {category} \n\n"
        markdown += f"**Summary:** {summary}\n\n"

        for article in articles:
            title = article["title"]
            source = article["source"]
            location = article["location"]
            description = article["description"]
            url = article["url"]

            markdown += f"#### **{title}**\n"
            markdown += f"  - New's Source: {source}\n"
            markdown += f"  - Location: {location}\n"
            markdown += f"  - Description: {description}\n"
            markdown += f"  - URL: {url}\n\n"
    
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(markdown, toc=False))
    pdf.writer.close()
    pdf.out_file.seek(0)  
    
    # Extract the binary data directly from BytesIO
    pdf_binary = pdf.out_file.read()
    # Generate a file name with a timestamp
    file_name = f"news_summary_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
    return file_name, pdf_binary