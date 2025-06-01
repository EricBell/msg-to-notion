# email-to-notion.py

import os
from dotenv import load_dotenv
from notion_client import Client

# Load environment variables from .env
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

def add_message_to_notion(short_description: str, message_body: str):
    # Step 1: Create the page
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": short_description
                        }
                    }
                ]
            }
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": message_body
                            }
                        }
                    ]
                }
            }
        ]
    )

    # Step 2: Update page with its own URL in "Page link" property
    page_id = response["id"]
    page_url = response["url"]

    notion.pages.update(
        page_id=page_id,
        properties={
            "Page link": {
                "url": page_url
            }
        }
    )

    print("✅ Page created and link saved:")
    print(f"Title: {short_description}")
    print(f"Page URL: {page_url}")
    return page_url

# Example usage
if __name__ == "__main__":
    short_description = "Sample: Secure Notion Entry"
    message_body = "This content was posted securely using environment variables."
    add_message_to_notion(short_description, message_body)
