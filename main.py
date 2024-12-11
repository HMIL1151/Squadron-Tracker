import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("events.db")
cursor = conn.cursor()

# Create the 'people' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rank TEXT NOT NULL
);
''')

# Create the 'event_types' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS event_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    category TEXT NOT NULL,
    points INTEGER NOT NULL
);
''')

# Create the 'events' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    date TEXT NOT NULL,
    badge_qual BOOLEAN NOT NULL,
    badge_category TEXT,
    event_category TEXT,
    points INTEGER NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES people (id)
);
''')

# Commit changes to the database
conn.commit()

# Helper function to populate the people table
def add_person(name, rank):
    cursor.execute("INSERT INTO people (name, rank) VALUES (?, ?)", (name, rank))
    conn.commit()

# Helper function to populate the event_types table
def add_event_type(event_name, category, points):
    cursor.execute("INSERT INTO event_types (event_name, category, points) VALUES (?, ?, ?)", (event_name, category, points))
    conn.commit()

# Helper function to add an event
def add_event(person_id, event_name, date, badge_qual):
    # Fetch category and points from event_types
    cursor.execute("SELECT category, points FROM event_types WHERE event_name = ?", (event_name,))
    result = cursor.fetchone()
    if result:
        event_category, points = result
    else:
        event_category, points = "Unknown", 0

    # Determine badge category if badge_qual is True
    badge_category = event_category if badge_qual else None

    # Calculate year from date
    year = date.split("-")[0]

    # Insert into events table
    cursor.execute('''
    INSERT INTO events (person_id, event_name, date, badge_qual, badge_category, event_category, points, year)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (person_id, event_name, date, badge_qual, badge_category, event_category, points, year))
    conn.commit()

# Example data for testing
# Add people
add_person("Alice", "Captain")
add_person("Bob", "Lieutenant")

# Add event types
add_event_type("Marathon", "Sports", 50)
add_event_type("Hackathon", "Technology", 100)

# Add events
add_event(1, "Marathon", "2024-12-10", True)
add_event(2, "Hackathon", "2024-12-11", False)

# Fetch and display all events
cursor.execute("SELECT * FROM events")
for row in cursor.fetchall():
    print(row)

# Close the database connection
conn.close()
