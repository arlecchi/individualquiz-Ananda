from flask import Flask, request, jsonify, render_template
import csv

app = Flask(__name__)

# Load CSV data into memory
sports_events = []
csv_file_path = "sports_events.csv"  # Change this if needed

with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sports_events.append(row)

# Route to serve the HTML page
@app.route("/")
def index():
    return render_template("index.html")

# Route to get unique sports
@app.route("/sports")
def get_sports():
    sports = sorted(set(event["sport_type"] for event in sports_events))
    return jsonify(sports)

# Route to get events by sport
@app.route("/events")
def get_events():
    sport = request.args.get("sport")
    if not sport:
        return jsonify({"error": "Sport not provided"}), 400

    filtered_events = [
        {
            "event_id": event["event_id"],
            "event_name": event["event_name"],
            "date": event["date"],
            "venue": event["venue"],
            "total_seats": event["total_seats"],
            "available_seats": event["available_seats"],
        }
        for event in sports_events
        if event["sport_type"] == sport
    ]

    return jsonify(filtered_events)

if __name__ == "__main__":
    app.run(debug=True)
