# Copyright 2025 Google LLC

#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

def get_campus_info(query: str) -> dict:
    """Provides information based on common campus-related queries.

    Args:
        query (str): The user's question or keyword.

    Returns:
        dict: A dictionary containing the answer with a 'status' and either
              a 'response' or 'error_message'.
    """
    logger.log_text(
        f"--- Tool: get_campus_info called with query: {query} ---", severity="INFO"
    )

    q = query.lower()

    # Mock campus data
    campus_faq = {
        "library": "📚 Library timing: 9AM–5PM. Aur haan, AC kabhi-kabhi kaam karta hai.",
        "canteen": "🍜 Aaj ka canteen menu: Maggi, Chai... aur ek surprise item.",
        "fees": "💰 Fees bharne ki last date: 15th August. Online portal se bhar sakte ho.",
        "exam timetable": "📝 Exam timetable will be released next week on the notice board and online.",
        "best canteen dish": "🥘 Maggi aur samosa sabse hit hain canteen mein!",
    }

    for key in campus_faq:
        if key in q:
            return {"status": "success", "response": campus_faq[key]}

    return {
        "status": "error",
        "error_message": f"Sorry, I don't have information for '{query}'. Try asking about library, canteen, fees, or exams.",
    }

root_agent = Agent(
    name="campus_agent",
    model="gemini-2.5-flash",
    instruction="You are a friendly campus help assistant designed to answer common student queries accurately and informally.",
    tools=[get_campus_info],
)
