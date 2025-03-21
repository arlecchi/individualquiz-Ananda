import pymysql
import pandas as pd

def get_events_by_sport():
    # Connect to MySQL database
    connection = pymysql.connect(
        host="127.0.0.1",    
        user="root",          
        password="",           
        database="quiz",
        port=3307
    )

    try:
        while True:  # Keep asking for input until the user decides to exit
            sport_name = input("\nEnter the sport name (or type 'exit' to quit): ").strip()

            if sport_name.lower() == 'exit':
                print("Exiting program. Goodbye!")
                break

            with connection.cursor() as cursor:
                # SQL Query to filter events by sport
                query = """
                SELECT event_id, event_name, date, venue, total_seats, available_seats
                FROM sports_events
                WHERE sport_type = %s
                ORDER BY date ASC;
                """
                cursor.execute(query, (sport_name,))
                results = cursor.fetchall()

                # Convert results to DataFrame
                df = pd.DataFrame(results, columns=['Event ID', 'Event Name', 'Date', 'Venue', 'Total Seats', 'Available Seats'])

                if df.empty:
                    print(f"No events found for sport: {sport_name}")
                    html_content = f"<h2>No events found for {sport_name}</h2>"
                else:
                    print("\n", df)
                    html_content = df.to_html(index=False)

                # Write results to an HTML file
                with open("output.html", "w", encoding="utf-8") as f:
                    f.write(f"""
                    <html>
                    <head>
                        <title>Sports Events</title>
                        <style>
                            table {{ border-collapse: collapse; width: 80%; margin: 20px auto; }}
                            th, td {{ border: 1px solid black; padding: 10px; text-align: left; }}
                            th {{ background-color: #f2f2f2; }}
                        </style>
                    </head>
                    <body>
                        <h1>Events for {sport_name}</h1>
                        {html_content}
                        <script>
                            setTimeout(() => {{
                                location.reload();
                            }}, 3000);
                        </script>
                    </body>
                    </html>
                    """)

                print("\nResults saved to output.html. Open it in your browser.")

    finally:
        connection.close()

# Call function
get_events_by_sport()
