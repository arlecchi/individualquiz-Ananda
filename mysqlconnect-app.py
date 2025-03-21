from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="quiz",
        port=3307
    )

# Route to serve the HTML page
@app.route("/")
def index():
    return render_template("index.html")

# Route to get unique sports
@app.route("/sports")
def get_sports():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT sport_type FROM sports_events")
    sports = [row[0] for row in cursor.fetchall()]
    connection.close()
    return jsonify(sports)

# Route to get events by sport
@app.route("/events")
def get_events():
    sport = request.args.get("sport")
    if not sport:
        return jsonify({"error": "Sport not provided"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT event_id, event_name, date, venue, total_seats, available_seats
        FROM sports_events WHERE sport_type = %s ORDER BY date ASC
    """, (sport,))
    events = cursor.fetchall()
    connection.close()

    return jsonify([
        {"event_id": row[0], "event_name": row[1], "date": row[2], "venue": row[3], "total_seats": row[4], "available_seats": row[5]}
        for row in events
    ])

if __name__ == "__main__":
    app.run(debug=True)
