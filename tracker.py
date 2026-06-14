import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime

# 1. Target Website
URL = "https://www.itpo.gov.in/itpo-event"

# 2. Setup the AI
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    # 3. Download the website text
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    soup = BeautifulSoup(response.text, 'html.parser')
    web_text = soup.get_text()

    # 4. Ask Gemini to find the events
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analyze the following website text and extract all listed events. 
    Format the output strictly as a clean markdown table with columns: Event Name, Date, Location, Description.
    Do not add conversational text or introduction. Just provide the table data.
    
    Website Content:
    {web_text[:20000]} 
    """
    
    ai_response = model.generate_content(prompt)
    
    # 5. Save the results to a file
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = "events_list.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Event List Updated on {current_date}\n\n")
        f.write(ai_response.text)
        
    print("Success! Event list updated.")

except Exception as e:
    print(f"An error occurred: {e}")
