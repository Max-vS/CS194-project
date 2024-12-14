import os

LLM_CONFIG = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.environ.get("OPENAI_API_KEY")
        }
    ]
}

FOI_OPTIONS = (
    "Agriculture", "Arts and Design", "Computer industry", "Construction",
    "Education", "Energy", "Entertainment", "Food Manufacturing",
    "Healthcare", "Hospitality industry", "Human Services",
    "Information technology", "Insurance occupations", "Journalist",
    "Law", "Marketing and advertising", "Metal fabrication",
    "Mining", "Real Estate", "Sales", "Telecommunication",
    "Transportation", "Utilities", "Wholesale trade"
)
