from flask import Flask, request, jsonify
from bs4 import BeautifulSoup, UnicodeDammit

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    raw_file = request.files["file"].read()
    html = UnicodeDammit(raw_file).unicode_markup
    soup = BeautifulSoup(html, "html.parser")

    def extract_bold_label_value(label):
        el = soup.find("span", string=lambda s: s and label.lower() in s.strip().lower())
        if el:
            parent = el.find_parent("td").find_next_sibling("td")
            if parent:
                try:
                    return float(parent.text.strip().replace(",", ""))
                except:
                    return parent.text.strip()
        return None

    data = {
        "due": extract_bold_label_value("Due"),
        "deposits_paid": extract_bold_label_value("Deposits/Paid"),
        "outstanding": extract_bold_label_value("Outstanding"),
        "total_booking_cost_incl_pay_direct": extract_bold_label_value("Total Booking Cost Inc Pay Direct"),
    }

    return jsonify(data)
