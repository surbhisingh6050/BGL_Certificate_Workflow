from flask import Flask, request, jsonify
from parser import parse_certificate_request
from sheets.lookup import get_sheet_data

app = Flask(__name__)


# --- Internal endpoint used by the WhatsApp bridge (unofficial-library POC) ---
# The Node.js bridge (logged into a real WhatsApp account sitting in the group)
# forwards the raw text of any group message here as {"text": "..."}.
# We return {"reply": "<text to post back into the group>"} or {"reply": null}
# to mean "ignore this message" (it didn't match the strict request format,
# e.g. normal chatter in the group).
@app.route('/internal/process-message', methods=['POST'])
def process_message():
    data = request.json or {}
    text = data.get('text', '')
    print(f"DEBUG: process_message received text: {text!r}")

    parsed = parse_certificate_request(text)
    if not parsed:
        print("DEBUG: Message did not match strict request format - ignoring")
        return jsonify({"reply": None})

    hospital_name = parsed['hospital_name']
    district = parsed['district']
    bgl_code = parsed['bgl_code']

    print(f"DEBUG: Parsed request -> hospital={hospital_name}, district={district}, bgl_code={bgl_code}")

    no_dues = get_sheet_data(district, bgl_code)
    print(f"DEBUG: get_sheet_data result: {no_dues}")

    if no_dues:
        reply = (
            f"✅ No dues found for {bgl_code} ({hospital_name}).\n"
            f"To issue the certificate, reply: ISSUE {bgl_code}"
        )
    else:
        reply = (
            f"❌ Dues pending or BGL Code {bgl_code} not found in {district} "
            f"for {hospital_name}. Please verify."
        )

    return jsonify({"reply": reply})


# --- Original official WhatsApp Cloud API webhook (kept for the later, ---
# --- "verified/proper way" phase - not used by the POC bridge) ---
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data or 'entry' not in data:
        return jsonify({"status": "error", "message": "Invalid payload"}), 400

    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        text = message['text']['body']
    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing key: {e}"}), 400

    parsed = parse_certificate_request(text)
    if not parsed:
        return jsonify({"status": "ignored", "message": "Message did not match expected format"}), 200

    hospital_name = parsed['hospital_name']
    district = parsed['district']
    bgl_code = parsed['bgl_code']

    no_dues = get_sheet_data(district, bgl_code)

    if no_dues:
        reply = {
            "interactive": {
                "type": "button",
                "body": {"text": f"Issue Certificate for BGL Code: {bgl_code}?"},
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": f"issue_{bgl_code}",
                                "title": "Issue Certificate"
                            }
                        }
                    ]
                }
            }
        }
    else:
        reply = {
            "text": {
                "body": f"Dues pending or BGL Code {bgl_code} not found in {district}. Please verify."
            }
        }

    return jsonify(reply)


if __name__ == '__main__':
    app.run(debug=True)
