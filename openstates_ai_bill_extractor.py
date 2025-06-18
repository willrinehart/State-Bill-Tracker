import requests
import pandas as pd
import time

API_KEY = "f0eda389-bfbf-437e-adab-753bfb042523"
BASE_URL = "https://v3.openstates.org"

HEADERS = {
    "X-API-KEY": API_KEY
}

def get_jurisdictions():
    time.sleep(1)  # Add a 1 second delay to avoid rate limiting
    url = f"{BASE_URL}/jurisdictions"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    # Get all state-level jurisdictions
    return [j['name'] for j in data['results'] if j['classification'] == 'state']

def search_ai_bills(jurisdiction):
    url = f"{BASE_URL}/bills"
    params = {
        "jurisdiction": jurisdiction,
        "q": "artificial intelligence",
        "sort": "updated_desc",
        "per_page": 50  # adjust as needed
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    bills = []
    for bill in data['results']:
        bills.append({
            "State": jurisdiction,
            "bill_id": bill.get("id", ""),
            "identifier": bill.get("identifier", ""),
            "title": bill.get("title", ""),
            "description": bill.get("description", ""),
            "classification": ", ".join(bill.get("classification", [])),
            "subjects": ", ".join(bill.get("subject", [])) if bill.get("subject") else "",
            "status": bill.get("latest_action_description", ""),
            "status_date": bill.get("latest_action_date", ""),
            "url": bill.get("extras", {}).get("openstates_url", bill.get("sources", [{}])[0].get("url", "")),
            "sponsors": ", ".join([s.get("name", "") for s in bill.get("sponsorships", [])])
        })
    return bills

def main():
    print("=== OpenStates AI Bill Extractor ===")
    all_bills = []
    states = get_jurisdictions()
    for state in states:
        print(f"Searching {state}...")
        try:
            bills = search_ai_bills(state)
            all_bills.extend(bills)
            time.sleep(1)  # Be polite to the API
        except Exception as e:
            print(f"Error with state {state}: {e}")
            continue
    if not all_bills:
        print("No AI-related bills found.")
        return
    df = pd.DataFrame(all_bills)
    df.to_excel("ai_bills_openstates.xlsx", index=False)
    print(f"Found {len(all_bills)} AI-related bills. Results saved to ai_bills_openstates.xlsx")

if __name__ == "__main__":
    main() 