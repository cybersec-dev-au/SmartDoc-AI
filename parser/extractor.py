import re
import json
from datetime import datetime

def parse_structured_data(raw_text):
    """
    Parses the raw text from an OCR'd receipt or invoice for date, total amount, and items.
    """
    data = {"date": None, "total": 0.0, "items": []}
    
    # 1. Date extraction (common formats: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, etc.)
    date_patterns = [
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, raw_text)
        if match:
            data["date"] = match.group(0)
            break
            
    # 2. Total amount extraction (Look for something near "TOTAL", "AMOUNT", etc.)
    # Support decimals like .00 or ,00
    total_patterns = [
        r"(?i)total[\s:]*[\$€]?[ ]?([\d,]+\.?\d{2})",
        r"(?i)amount[\s:]*[\$€]?[ ]?([\d,]+\.?\d{2})",
        r"(?i)total due[\s:]*[\$€]?[ ]?([\d,]+\.?\d{2})"
    ]
    for pattern in total_patterns:
        match = re.search(pattern, raw_text)
        if match:
            data["total"] = float(match.group(1).replace(",", ""))
            break
            
    # 3. Items extraction (Very basic: find lines containing numbers and common item-related patterns)
    # Simple strategy: lines that look like "Item Description ... Price"
    lines = raw_text.split("\n")
    for line in lines:
        line = line.strip()
        # Item regex pattern: Name followed by a price-looking string at the end
        item_match = re.search(r"^(.*?)\s+[\$€]?[\s]?([\d,]+\.\d{2})$", line)
        if item_match:
            item_name = item_match.group(1).strip()
            item_price = float(item_match.group(2).replace(",", ""))
            # Avoid picking up the total line itself
            if "total" not in item_name.lower():
                data["items"].append({"name": item_name, "price": item_price})
                
    return data

if __name__ == "__main__":
    # Test text
    sample_text = """
    SUPER STORE #1234
    Date: 25/12/2025
    
    MILK       3.50
    BREAD      2.10
    EGGS       4.99
    
    TOTAL DUE  10.59
    THANK YOU!
    """
    print(json.dumps(parse_structured_data(sample_text), indent=4))
