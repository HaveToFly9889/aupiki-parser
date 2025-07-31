from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    html = request.files["file"].read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    def extract_by_label(label):
        el = soup.find("span", string=lambda s: s and label.lower() in s.lower())
        if el:
            td = el.find_parent("td")
            if td:
                value_td = td.find_next_sibling("td")
                if value_td:
                    text = value_td.get_text(strip=True).replace(",", "").replace("$", "")
                    try:
                        return float(text)
                    except:
                        return None
        return None

    data = {
        "due": extract_by_label("Due"),
        "paid": extract_by_label("Deposits/Paid"),
        "outstanding": extract_by_label("Outstanding"),
        "total_booking_cost": extract_by_label("Total Booking Cost Inc Pay Direct")
    }

    return jsonify(data)
