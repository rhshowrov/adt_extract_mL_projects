import json
import re
import os

def load_json(json_file):
    """Load the JSON file from the base directory"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, json_file):
    """Save the updated JSON file to the base directory"""
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_text_file(file_path):
    """Read text content from a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_company_details(text, data, company_name):
    """Extract and update company details from text using dynamic patterns"""
    if "company_details" not in data:
        data["company_details"] = {}
    
    # Dynamic patterns based on company name
    director_pattern = re.compile(
        rf"For {re.escape(company_name)}\s*\n\s*(.+?)\s*\n\s*Directo[tr]\s*\(DIN:\s*(\d+)\)",
        re.IGNORECASE
    )
    
    # Extract director information
    director_match = director_pattern.search(text)
    if director_match:
        data["company_details"]["director"] = {
            "name": director_match.group(1).strip(),
            "din": director_match.group(2).strip()
        }
    
    # Extract address information (works with different address formats)
    address_pattern = re.compile(
        r"(?:Registered Office|PRODUCTION UNIT).*?(?:at|:)\s*(.+?)\s*[-—]\s*(\d{6})",
        re.IGNORECASE | re.DOTALL
    )
    address_match = address_pattern.search(text)
    if address_match:
        data["company_details"]["address"] = {
            "location": address_match.group(1).strip(),
            "pincode": address_match.group(2).strip()
        }
    
    # Extract contact info (flexible pattern for different formats)
    contact_pattern = re.compile(
        r"(?:\+|\bPhone\b)[\s:]*([\d\s\/]+)[\s|]*(?:Email\b)?[\s:]*([^\s|]+)[\s|]*(?:Website\b)?[\s:]*([^\s|]+)",
        re.IGNORECASE
    )
    contact_match = contact_pattern.search(text)
    if contact_match:
        data["company_details"]["contact"] = {
            "phone": contact_match.group(1).strip(),
            "email": contact_match.group(2).strip(),
            "website": contact_match.group(3).strip()
        }

def extract_auditor_details(text, data):
    """Extract and update auditor details from text with dynamic patterns"""
    if "auditor_details" not in data:
        data["auditor_details"] = {}
    
    # Flexible FRN pattern
    if frn_match := re.search(r"FRN\s*:\s*(\w+)", text, re.IGNORECASE):
        data["auditor_details"]["firm_registration_number"] = frn_match.group(1).strip()
    
    # Partner information with flexible formatting
    partner_pattern = re.compile(
        r"Partner\s*\n\s*(?:Name\s*:\s*)?(.+?)\s*\n\s*Mem(?:bership)?\s*No\.?\s*:\s*(\d+)",
        re.IGNORECASE
    )
    if partner_match := partner_pattern.search(text):
        data["auditor_details"]["partner"] = {
            "name": partner_match.group(1).strip(),
            "membership_number": partner_match.group(2).strip()
        }
    
    # Flexible PAN/GSTIN extraction
    tax_pattern = re.compile(
        r"(?:PAN\s*[:=]\s*([A-Z]{5}\d{4}[A-Z]))\s*(?:GSTIN\s*[:=]\s*(\d{2}[A-Z]{5}\d{4}[A-Z]\d[Z][A-Z\d]))",
        re.IGNORECASE
    )
    if tax_match := tax_pattern.search(text):
        data["auditor_details"].update({
            "pan": tax_match.group(1).strip(),
            "gstin": tax_match.group(2).strip() if tax_match.group(2) else None
        })

def extract_appointment_details(text, data, company_name):
    """Extract appointment details with company-specific patterns"""
    if "appointment_details" not in data:
        data["appointment_details"] = {}
    
    # Dynamic AGM pattern
    agm_pattern = re.compile(
        rf"(Annual General Meeting|AGM).*?(?:held on|dated)\s*(.+?)\s*(?:at|on)",
        re.IGNORECASE
    )
    if agm_match := agm_pattern.search(text):
        data["appointment_details"].update({
            "agm_date": agm_match.group(2).strip(),
            "appointment_date": agm_match.group(2).strip()
        })
    
    # Flexible term pattern
    term_pattern = re.compile(
        r"appointed.*?(?:for|term of)\s*(\d+)\s*years.*?(?:from|between)\s*(.+?)\s*(?:to|till)\s*(.+?)\s*(?:of|meeting)",
        re.IGNORECASE | re.DOTALL
    )
    if term_match := term_pattern.search(text):
        data["appointment_details"].update({
            "appointment_term": f"From {term_match.group(2).strip()} to {term_match.group(3).strip()}",
            "duration_years": term_match.group(1).strip()
        })
    
    # Flexible remuneration pattern
    remuneration_pattern = re.compile(
        r"remuneration.*?(?:shall be|as)\s*(.+?)\s*(?:in addition to|plus)\s*(.+?)\s*(?:incurred|payable)",
        re.IGNORECASE | re.DOTALL
    )
    if remuneration_match := remuneration_pattern.search(text):
        data["appointment_details"]["remuneration_terms"] = {
            "basis": remuneration_match.group(1).strip(),
            "additional_terms": remuneration_match.group(2).strip()
        }

def process_text_files(json_data, text_folder):
    """Process all text files with dynamic company-specific patterns"""
    # Get company name from JSON or default to pattern
    company_name = json_data.get("company_details", {}).get("name", "ALUPA FOODS PRIVATE LIMITED")
    
    text_files = [f for f in os.listdir(text_folder) if f.endswith('.txt')]
    
    for text_file in text_files:
        file_path = os.path.join(text_folder, text_file)
        try:
            text = read_text_file(file_path)
            
            # Determine content type dynamically
            if "consent" in text_file.lower() or "consent" in text.lower():
                extract_auditor_details(text, json_data)
                extract_appointment_details(text, json_data, company_name)
            elif "acceptance" in text_file.lower() or "accept" in text.lower():
                extract_auditor_details(text, json_data)
            elif "resolution" in text_file.lower() or "resolve" in text.lower():
                extract_company_details(text, json_data, company_name)
                extract_appointment_details(text, json_data, company_name)
            elif "intimation" in text_file.lower() or "appoint" in text.lower():
                extract_appointment_details(text, json_data, company_name)
            else:
                # Fallback processing for unknown files
                extract_company_details(text, json_data, company_name)
                extract_auditor_details(text, json_data)
                extract_appointment_details(text, json_data, company_name)
                
        except Exception as e:
            print(f"Error processing {text_file}: {str(e)}")
    
    return json_data

def main():
    """Main function with configurable paths"""
    config = {
        "input_json": "output.json",
        "text_files_dir": "output_images_text",
        "output_json": "updated_output.json"
    }
    
    print("Loading initial data...")
    json_data = load_json(config["input_json"])
    
    print("Processing text documents...")
    updated_data = process_text_files(json_data, config["text_files_dir"])
    
    print("Saving results...")
    save_json(updated_data, config["output_json"])
    
    print(f"Successfully updated {config['output_json']}")

if __name__ == "__main__":
    main()