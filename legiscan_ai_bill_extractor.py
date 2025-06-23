import requests
import pandas as pd
import time

API_KEY = "4ec115f659a1f2c779a02e2ec987b31c"
BASE_URL = "https://api.legiscan.com/"


def get_states():
    """
    Get the list of all states supported by LegiScan.
    Returns a list of state abbreviations.
    """
    url = f"{BASE_URL}?key={API_KEY}&op=getMasterList&state=US"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return list(data['masterlist'].keys())


def get_sessions(state):
    """
    Get the list of sessions for a given state.
    @param state
    @return a list of session_id.
    """
    url = f"{BASE_URL}?key={API_KEY}&op=getSessionList&state={state}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return [s['session_id'] for s in data['sessions']]


def search_ai_bills(state, session_id):
    """
    Search for AI-related bills in a given state/session.
    @param state
    @param session_id
    @return a list of bill dictionaries.
    """
    url = f"{BASE_URL}?key={API_KEY}&op=search&state={state}&query=artificial+intelligence&session_id={session_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    bills = []
    searchresult = data.get('searchresult', {})
    for key, bill in searchresult.items():
        if key == "summary":
            continue
        # Add the state to the bill dictionary for reference
        bill['State'] = state
        bills.append(bill)
    return bills


def get_bill_details(bill_id):
    """
    Retrieve detailed information for a specific bill by bill_id.
    """
    url = f"{BASE_URL}?key={API_KEY}&op=getBill&id={bill_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data['bill']


def main():
    print("=== LegiScan AI Bill Extractor ===")
    all_bills = []
    states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
        'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
        'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]
    for state in states:
        print(f"Searching {state}...")
        try:
            sessions = get_sessions(state)
            if not sessions:
                continue
            latest_session = sessions[-1]
            bills = search_ai_bills(state, latest_session)
            # Fetch and append description for each bill
            for bill in bills:
                try:
                    details = get_bill_details(bill['bill_id'])
                    bill['description'] = details.get('description', '')
                except Exception as e:
                    print(f"  Could not fetch details for bill {bill['bill_id']}: {e}")
                    bill['description'] = ''
                time.sleep(0.5)  # To avoid 429 error
            all_bills.extend(bills)
            time.sleep(1)  # To avoid 429 error
        except Exception as e:
            print(f"Error with state {state}: {e}")
            continue
    if not all_bills:
        print("No AI-related bills found.")
        return
    df = pd.DataFrame(all_bills)
    df.to_excel("ai_bills_legiscan.xlsx", index=False)
    print(f"Found {len(all_bills)} AI-related bills. Results saved to ai_bills_legiscan.xlsx")


if __name__ == "__main__":
    main() 