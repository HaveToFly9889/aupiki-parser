from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    html = request.files['file'].read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    def extract_bold_label_value(label):
        el = soup.find("span", string=lambda s: s and label in s and s.strip().lower() == label.lower())
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
        "credit_card_fee": extract_bold_label_value("382.07"),
        "pay_direct": extract_bold_label_value("Pay Direct"),
        "total_due": extract_bold_label_value("Total Due"),
        "deposits_paid": extract_bold_label_value("Deposits/Paid"),
        "outstanding": extract_bold_label_value("Outstanding"),
        "total_booking_cost_incl_pay_direct": extract_bold_label_value("Total Booking Cost Inc Pay Direct"),
    }

    return jsonify(data)
