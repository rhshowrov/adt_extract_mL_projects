import json
from openai import OpenAI
from pathlib import Path
import re
# Initialize Mistral
client = OpenAI(
    api_key="TdpYZgAzjX3YHClFPWxvTLfI7i7OEtFv", 
    base_url="https://api.mistral.ai/v1"
)

#Load JSON file
with open("output.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

#Convert JSON to string
json_string = json.dumps(json_data, indent=2)

#prompt
prompt = (
    "The following JSON contains structured data from an Indian company's statutory auditor appointment filing, "
    "as per the Companies Act, 2013 and the Companies (Audit and Auditors) Rules, 2014.\n\n"
    "Please summarize the key points in 3–5 lines. Make sure to include the following where available:\n"
    "- Company name,director name and registered office\n"
    "- Auditor's firm name and partner membership number\n"
    "- Duration of appointment and its compliance with legal limits\n"
    "- AGM date and appointment date\n"
    "- Whether joint auditors were appointed\n"
    "- Applicability of auditor rotation rules\n"
    "- Whether the auditor has previously served the company and for how many years\n"
    "- Attachments submitted as supporting documents\n\n"
    "Write the summary in a friendly tone, like an AI assistant helping a non-technical Indian user understand it. "
    "Each sentence should appear on a new line, like a paragraph with line breaks.\n\n"
    f"{json_string}\n\nSummary:"
)


#Send the request
response = client.chat.completions.create(
    model="mistral-small-latest",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that summarizes company filings."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.5,
    max_tokens=300,
)

# Extract and save the summary
summary = response.choices[0].message.content.strip()
summary_sentences = re.split(r'(?<=[.!?])\s+', summary)
formatted_summary = "\n".join(summary_sentences)

# Save summary
Path("summary.txt").write_text(formatted_summary, encoding="utf-8")

print("Summary saved to summary.txt")

