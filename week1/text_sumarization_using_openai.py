import os 
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
# from ipython.display import display, Markdown
from openai import OpenAI

load_dotenv()

"""
A program that summarizes a webpage using OpenAI's GPT-3.5-turbo model.
    It fetches the content of a webpage, extracts the text, and then uses the OpenAI API to generate a summary.
    The program requires the `requests`, `beautifulsoup4`, and `openai` libraries.
    The program uses the `requests` library to fetch the content of the webpage.
    The program uses the `beautifulsoup4` library to parse the HTML content of the webpage.

"""

api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI()

class Website:
    """utility class to represent a website we have scrapped"""
    url: str 
    title: str
    text: str

    def __init__(self, url):
        """Create this website object from the given url using BeutifulSoup library"""
        self.url = url 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else 'No title found'
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()

        self.text = soup.body.get_text(separator="\n", strip=True)

ed = Website("https://edwarddonner.com")
# print(ed.title)
# print(ed.text[:1000])

# format the text returned from the website using OpenAI
# system prompt - tells the model what task they are performing and what tone to use
# user prompt - the question the model to reply on

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

# A function that writes a User Prompt that asks for summaries of websites:
def user_prompt(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
    please provide a short summary of this website in markdown. \
    If it includes news or announcements, then summarize these too.\n\n"

    user_prompt += website.text
    return user_prompt

# print(user_prompt(ed))

def messages(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt(website)}
    ]

def summarize_website(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages(website),

    )
    return response.choices[0].message.content

summary = summarize_website("https://edwarddonner.com")
print(summary)

    
