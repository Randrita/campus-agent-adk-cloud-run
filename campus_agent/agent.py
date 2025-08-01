# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

import os
from pathlib import Path

import google.auth
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.cloud import logging as google_cloud_logging

# Load environment variables from .env file in root directory
root_dir = Path(__file__).parent.parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Use default project from credentials if not in .env
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

logging_client = google_cloud_logging.Client()
logger = logging_client.logger("campus-agent")


def campus_help(question: str) -> dict:
    """Returns a fun and helpful response for campus-related queries.

    Args:
        question (str): Student's question (e.g., "canteen", "wifi", "exam").

    Returns:
        dict: A response message with campus humor.
    """
    logger.log_text(f"Campus Help Invoked: {question}", severity="INFO")

    q = question.lower()

    if "library" in q:
        return {"status": "success", "reply": "📚 Library timing: 9AM–5PM. AC chal raha hai... kabhi kabhi."}

    elif "canteen" in q or "menu" in q:
        return {"status": "success", "reply": "🍜 Aaj ka menu: Maggi, samosa, aur disappointment."}

    elif "exam" in q:
        return {"status": "success", "reply": "😵 Exam tension? Bhai syllabus hi nahi mila abhi tak!"}

    elif "wifi" in q:
        return {"status": "success", "reply": "📶 WiFi: WhatsApp chalega, YouTube chhodo."}

    elif "hostel" in q:
        return {"status": "success", "reply": "🛏️ Hostel: Sapne bade hote hain, bathrooms chhote."}

    elif "placement" in q:
        return {"status": "success", "reply": "💼 Placement: Don’t worry, sabko ho jaata hai (almost)."}

    return {
        "status": "error",
        "reply": "🤖 Bhaiya/Bhenji, yeh bot sirf campus ke dukh-sukh ke liye hai. Try: library, canteen, exam, wifi, hostel, placement."
    }


campus_agent = Agent(
    name="campus_agent",
    model="gemini-2.5-flash",
    instruction="You are a humorous and helpful campus bot that guides students with real-life tips, relatable answers, and a bit of fun.",
    tools=[campus_help],
)
