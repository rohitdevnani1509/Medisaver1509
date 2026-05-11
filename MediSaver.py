import requests
import webbrowser
from difflib import SequenceMatcher

# ----------------------------
# CONFIG
# ----------------------------

FDA_API = "https://api.fda.gov/drug/ndc.json"

PHARMACY_LINKS = {
    "1mg": "https://www.1mg.com/search/all?name={}",
    "NetMeds": "https://www.netmeds.com/catalogsearch/result/{}",
    "PharmEasy": "https://pharmeasy.in/search/all?name={}"
}

# ----------------------------
# SAMPLE PRICE DATABASE
# (Demo AI price comparison)
# ----------------------------

PRICE_DB = {
    "Crocin": 35,
    "Dolo 650": 28,
    "Paracetamol": 12,
    "Calpol": 30,
    "Azithromycin": 65,
    "Azee": 120,
    "Metformin": 22,
    "Glycomet": 110,
    "Atorvastatin": 40,
    "Lipitor": 250
}

# ----------------------------
# FUNCTIONS
# ----------------------------

def fetch_medicine_data(medicine_name):
    """
    Fetch medicine data from openFDA
    """
    try:
        url = f"{FDA_API}?search=brand_name:{medicine_name}&limit=5"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()

        if "results" not in data:
            return None

        return data["results"]

    except Exception as e:
        print("API Error:", e)
        return None


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_cheaper_alternatives(medicine_name):
    """
    AI-like matching for cheaper alternatives
    """

    if medicine_name not in PRICE_DB:
        print("\nMedicine not found in local pricing database.")
        return []

    original_price = PRICE_DB[medicine_name]

    alternatives = []

    for med, price in PRICE_DB.items():

        if med.lower() == medicine_name.lower():
            continue

        # AI-like similarity logic
        score = similarity(medicine_name, med)

        # cheaper medicine condition
        if price < original_price:
            alternatives.append({
                "name": med,
                "price": price,
                "score": score
            })

    # sort by similarity + cheapest
    alternatives = sorted(
        alternatives,
        key=lambda x: (-x["score"], x["price"])
    )

    return alternatives[:5]


def generate_buy_links(medicine_name):
    """
    Generate online purchase/search links
    """

    links = {}

    for pharmacy, url in PHARMACY_LINKS.items():
        links[pharmacy] = url.format(medicine_name.replace(" ", "%20"))

    return links


def print_links(links):
    for pharmacy, link in links.items():
        print(f"{pharmacy}: {link}")


# ----------------------------
# MAIN APP
# ----------------------------

def main():

    print("\n==============================")
    print(" AI Medicine Alternative Finder ")
    print("==============================\n")

    medicine_name = input("Enter medicine name: ").strip()

    print("\nSearching medicine details...\n")

    medicine_data = fetch_medicine_data(medicine_name)

    if medicine_data:
        try:
            result = medicine_data[0]

            brand = result.get("brand_name", "N/A")
            generic = result.get("generic_name", "N/A")
            manufacturer = result.get("labeler_name", "N/A")

            print("Medicine Information")
            print("---------------------")
            print("Brand Name :", brand)
            print("Generic    :", generic)
            print("Manufacturer:", manufacturer)

        except Exception:
            print("Medicine information found but incomplete.")

    else:
        print("No FDA data found.")

    print("\nFinding cheaper alternatives using AI...\n")

    alternatives = find_cheaper_alternatives(medicine_name)

    if not alternatives:
        print("No cheaper alternatives found.")
        return

    print("Cheaper Alternatives")
    print("----------------------")

    for idx, alt in enumerate(alternatives, start=1):

        print(f"\n{idx}. {alt['name']}")
        print(f"   Estimated Price: ₹{alt['price']}")
        print(f"   Similarity Score: {round(alt['score'], 2)}")

        print("\n   Buy Online:")

        links = generate_buy_links(alt['name'])
        print_links(links)

    # Optional auto-open
    open_browser = input("\nOpen first alternative in browser? (y/n): ")

    if open_browser.lower() == 'y':
        first_med = alternatives[0]["name"]
        links = generate_buy_links(first_med)

        first_link = list(links.values())[0]

        webbrowser.open(first_link)
        print("Browser opened.")


# ----------------------------
# ENTRY
# ----------------------------

if __name__ == "__main__":
    main()