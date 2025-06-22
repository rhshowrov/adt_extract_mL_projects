import pymupdf  # PyMuPDF
import os
import json

# --- Structured JSON Template ---
structured_data = {
    "company_details": {},
    "auditor_details": {},
    "appointment_details": {},
    "attachments": [],
    "previous_auditors": []
}

# --- Utility Functions ---
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_value(value):
    if value == "" or value is None:
        return None
    return value.strip() if isinstance(value, str) else value

# --- Main PDF Parsing ---
pdf_path = "Form ADT-1-29092023_signed.pdf"
doc = pymupdf.open(pdf_path)

# 1. Extract form field data
for page in doc:
    for widget in page.widgets() or []:
        field_name = widget.field_name
        field_value = clean_value(widget.field_value)
        if not field_value:
            continue

        if "CIN_C" in field_name:
            structured_data["company_details"]["cin"] = field_value
        elif "CompanyName_C" in field_name:
            structured_data["company_details"]["name"] = field_value
        elif "CompanyAdd_C" in field_name:
            structured_data["company_details"]["registered_office"] = field_value
        elif "EmailId_C" in field_name:
            structured_data["company_details"]["email"] = field_value
        elif 'WhtrCmpnyFallClassOfCmpny' in field_name:
            structured_data["company_details"]["rotation_rule_status"] = field_value.upper() in ["YES", "AFFR"]

        elif "NameAuditorFirm_C" in field_name:
            structured_data["auditor_details"]["name"] = field_value
        elif "MemberShNum" in field_name:
            structured_data["auditor_details"]["membership_number"] = field_value
        elif "PAN_C" in field_name:
            structured_data["auditor_details"]["pan"] = field_value
        elif "permaddress2a_C" in field_name:
            structured_data["auditor_details"]["address_line1"] = field_value
        elif "permaddress2b_C" in field_name:
            structured_data["auditor_details"]["address_line2"] = field_value
        elif "City_C" in field_name:
            structured_data["auditor_details"]["city"] = field_value
        elif "State_P" in field_name:
            structured_data["auditor_details"]["state"] = field_value
        elif "Pin_C" in field_name:
            structured_data["auditor_details"]["pincode"] = field_value
        elif "email" in field_name and "@" in field_value:
            structured_data["auditor_details"]["email"] = field_value

        elif "DateOfAccAuditedFrom_D" in field_name:
            structured_data["appointment_details"]["period_from"] = field_value
        elif "DateOfAccAuditedTo_D" in field_name:
            structured_data["appointment_details"]["period_to"] = field_value
        elif "NumOfFinanYearApp" in field_name:
            structured_data["appointment_details"]["duration_years"] = field_value
        elif "WhrtInLimit" in field_name and field_value == "YES":
            structured_data["appointment_details"]["within_legal_limits"] = True
        elif "WhtrJointAudAppoint" in field_name and field_value == "NO":
            structured_data["appointment_details"]["joint_auditors"] = False
        elif "DateAnnualGenMeet_D" in field_name:
            structured_data["appointment_details"]["agm_date"] = field_value
        elif "DateReceipt_D" in field_name:
            structured_data["appointment_details"]["appointment_date"] = field_value

        elif "Hidden_L" in field_name and field_value:
            attachments = field_value.split(":")
            for i in range(0, len(attachments), 2):
                if i+1 < len(attachments):
                    structured_data["attachments"].append(attachments[i].strip())

        elif "NumOfFinanYear" in field_name:
            structured_data['previous_auditors'].append({"auditor_tenure": field_value})

# Extracting table-based previous auditors
if len(doc) >= 2:
    tables = doc[1].find_tables()
    if tables.tables:
        table_data = tables[0].extract()
        for row in table_data[1:]:
            if row[1]:  # only if auditor name/info exists
                structured_data['previous_auditors'].append({
                    "auditor_type": row[1],
                    "start_date": row[2],
                    "end_date": row[3]
                })

# 3. Save extracted data to JSON
save_to_json(structured_data, "output.json")

# 4. Extract embedded files with .pdf extension
output_dir = "output_embedded"
os.makedirs(output_dir, exist_ok=True)
file_count = 0

for i in range(doc.embfile_count()):
    try:
        # filename extraction with fallback
        try:
            info = doc.embfile_info(i)
            original_name = info.get("filename", f"file_{i}")
        except:
            original_name = f"file_{i}"

        base_name = os.path.splitext(original_name)[0]
        final_name = f"{base_name}.pdf"

        fdata = doc.embfile_get(i)

        with open(os.path.join(output_dir, final_name), "wb") as f:
            f.write(fdata)

        print(f"Saved: {final_name}")
        file_count += 1

    except Exception as e:
        print(f"Failed to extract file {i}: {e}")

doc.close()


if file_count == 0:
    print(" No embedded files found.")
else:
    print(f"\n Done! Extracted {file_count} embedded files as PDF.")




