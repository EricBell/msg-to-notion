import os
from dotenv import load_dotenv
from notion_client import Client

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

# Initialize the Notion client
notion = Client(auth=NOTION_TOKEN)

def create_notion_entry(title: str, description: str):
    # Step 1: Create a page in the database
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Page": {
                "title": [
                    {
                        "text": {
                            "content": title
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
                                "content": description
                            }
                        }
                    ]
                }
            }
        ]
    )

    print(f"✅ Page created: {response['url']}")
    return response["url"]

# Example usage
if __name__ == "__main__":
    message_title = "Meeting Notes: May 24"
    message_description = "Discussed Notion automation and VS Code GitHub integration."
    create_notion_entry(message_title, message_description)
