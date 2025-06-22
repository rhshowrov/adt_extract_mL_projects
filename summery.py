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
    "The following JSON contains structured data from an Indian company audit filing under the Companies Act, 2013 "
    "and the Companies (Audit and Auditors) Rules, 2014.\n\n"
    "Your task is to extract and summarize the key details in 3–5 lines. "
    "Mention the following where available:\n"
    "- Company name\n"
    "- Auditor name and appointment duration\n"
    "- Appointment date and AGM date\n"
    "- Whether joint auditors are appointed\n"
    "- If the appointment is within legal limits\n"
    "- Whether rotation rules are applicable\n"
    "- Supporting documents submitted\n\n"
    "Make the summary sound like an AI assistant explaining it to a non-technical person in India. "
    "Each sentence should appear on a new line, as if writing a short paragraph with line breaks.\n\n"
    f"{json_string}\n\nSummary:"
)


# Send the request
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

print("✅ Summary saved to summary.txt")

