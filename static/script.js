// Fetch available sports and populate the dropdown
async function fetchSports() {
    const response = await fetch("/sports");
    const sports = await response.json();

    const select = document.getElementById("sport-select");
    sports.forEach(sport => {
        const option = document.createElement("option");
        option.value = sport;
        option.textContent = sport;
        select.appendChild(option);
    });
}

// Fetch events when a sport is selected
async function fetchEvents() {
    const sport = document.getElementById("sport-select").value;
    if (!sport) return;

    const response = await fetch(`/events?sport=${sport}`);
    const events = await response.json();

    const container = document.getElementById("events-container");
    container.innerHTML = ""; // Clear previous results

    if (events.length === 0) {
        container.innerHTML = `<p>No events found for ${sport}.</p>`;
        return;
    }

    let table = `<table border="1">
        <tr>
            <th>Event ID</th>
            <th>Event Name</th>
            <th>Date</th>
            <th>Venue</th>
            <th>Total Seats</th>
            <th>Available Seats</th>
        </tr>`;
    
    events.forEach(event => {
        table += `
        <tr>
            <td>${event.event_id}</td>
            <td>${event.event_name}</td>
            <td>${event.date}</td>
            <td>${event.venue}</td>
            <td>${event.total_seats}</td>
            <td>${event.available_seats}</td>
        </tr>`;
    });

    table += `</table>`;
    container.innerHTML = table;
}

// Load sports when the page loads
window.onload = fetchSports;
