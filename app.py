from flask import Flask, request
import sqlite3

app = Flask(__name__)


# Database initialization
def init_db():
    conn = sqlite3.connect("campusfind.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT,
            item_name TEXT,
            category TEXT,
            color TEXT,
            description TEXT,
            location TEXT,
            time TEXT
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CampusFind AI</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body>

        <h1>🎓 CampusFind AI</h1>

        <h2>Lost & Found Campus</h2>

        <p>Find lost items easily inside your campus.</p>

        <hr>

        <h3>📢 Report Lost Item</h3>

        <form action="/report/lost" method="POST">

            Item Name:<br>
            <input type="text" name="item_name" required>
            <br><br>

            Category:<br>
            <input type="text" name="category"
                   placeholder="Phone / Wallet / ID Card">
            <br><br>

            Color:<br>
            <input type="text" name="color">
            <br><br>

            Description:<br>
            <textarea name="description"></textarea>
            <br><br>

            Lost Location:<br>
            <input type="text" name="location"
                   placeholder="Library / Canteen">
            <br><br>

            Time:<br>
            <input type="text" name="time"
                   placeholder="10:30 AM">
            <br><br>

            <button type="submit">Submit Lost Item</button>

        </form>

        <hr>

        <h3>📦 Report Found Item</h3>

        <form action="/report/found" method="POST">

            Item Name:<br>
            <input type="text" name="item_name" required>
            <br><br>

            Category:<br>
            <input type="text" name="category"
                   placeholder="Phone / Wallet / ID Card">
            <br><br>

            Color:<br>
            <input type="text" name="color">
            <br><br>

            Description:<br>
            <textarea name="description"></textarea>
            <br><br>

            Found Location:<br>
            <input type="text" name="location"
                   placeholder="Library / Canteen">
            <br><br>

            Time:<br>
            <input type="text" name="time"
                   placeholder="10:30 AM">
            <br><br>

            <button type="submit">Submit Found Item</button>

        </form>

        <hr>

        <h3>🔍 Search Items</h3>

        <a href="/items">
            <button>View All Items</button>
        </a>

    </body>
    </html>
    """


# Report lost item
@app.route("/report/lost", methods=["POST"])
def report_lost():
    save_item("Lost")

    return """
    <h2>✅ Lost Item Reported!</h2>
    <p>Your lost item has been saved.</p>
    <a href="/">⬅ Back to Home</a>
    """


# Report found item
@app.route("/report/found", methods=["POST"])
def report_found():
    save_item("Found")

    return """
    <h2>✅ Found Item Reported!</h2>
    <p>Your found item has been saved.</p>
    <a href="/">⬅ Back to Home</a>
    """


# Save item to database
def save_item(item_type):
    conn = sqlite3.connect("campusfind.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items
        (item_type, item_name, category, color,
         description, location, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        item_type,
        request.form.get("item_name"),
        request.form.get("category"),
        request.form.get("color"),
        request.form.get("description"),
        request.form.get("location"),
        request.form.get("time")
    ))

    conn.commit()
    conn.close()


# View all items
@app.route("/items")
def items():
    conn = sqlite3.connect("campusfind.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CampusFind Items</title>
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
    </head>

    <body>

    <h1>🔍 CampusFind AI</h1>

    <h2>All Lost & Found Items</h2>
    """

    if not data:
        html += "<p>No items reported yet.</p>"

    for item in data:
        html += f"""
        <hr>

        <h3>{item[2]}</h3>

        <b>Type:</b> {item[1]}<br>
        <b>Category:</b> {item[3]}<br>
        <b>Color:</b> {item[4]}<br>
        <b>Description:</b> {item[5]}<br>
        <b>Location:</b> {item[6]}<br>
        <b>Time:</b> {item[7]}<br>
        """

    html += """
        <hr>
        <a href="/">⬅ Back to Home</a>

    </body>
    </html>
    """

    return html


# Start application
if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
