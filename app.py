from flask import Flask, request, redirect
import sqlite3
from html import escape

app = Flask(__name__)

DATABASE = "campusfind.db"


# ================= DATABASE =================

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT NOT NULL,
            item_name TEXT NOT NULL,
            category TEXT,
            color TEXT,
            description TEXT,
            location TEXT,
            time TEXT,
            contact TEXT
        )
    """)

    # Add contact column if old database already exists
    try:
        cursor.execute("ALTER TABLE items ADD COLUMN contact TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def save_item(item_type):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items
        (item_type, item_name, category, color,
         description, location, time, contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item_type,
        request.form.get("item_name", ""),
        request.form.get("category", ""),
        request.form.get("color", ""),
        request.form.get("description", ""),
        request.form.get("location", ""),
        request.form.get("time", ""),
        request.form.get("contact", "")
    ))

    conn.commit()
    conn.close()


# ================= STYLE =================

STYLE = """
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    color: #172033;
}

.header {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: white;
    padding: 30px 20px;
    text-align: center;
}

.header h1 {
    margin: 0;
    font-size: 32px;
}

.header p {
    margin: 10px 0 0;
}

.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 22px;
    margin: 20px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

input,
textarea,
select {
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    border: 1px solid #ccd3df;
    border-radius: 8px;
    font-size: 16px;
}

textarea {
    min-height: 90px;
}

label {
    display: block;
    font-weight: bold;
    margin-top: 14px;
}

button {
    border: none;
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border-radius: 9px;
    font-size: 16px;
    margin-top: 18px;
}

.nav {
    display: inline-block;
    text-decoration: none;
    background: #111827;
    color: white;
    padding: 12px 18px;
    border-radius: 9px;
    margin: 5px;
}

.found {
    border-left: 6px solid #16a34a;
}

.lost {
    border-left: 6px solid #dc2626;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: bold;
}

.found-badge {
    background: #dcfce7;
    color: #166534;
}

.lost-badge {
    background: #fee2e2;
    color: #991b1b;
}

.search {
    margin-bottom: 20px;
}

.contact {
    background: #eef2ff;
    padding: 12px;
    border-radius: 8px;
    margin-top: 12px;
}

@media(max-width:600px) {
    .container {
        padding: 12px;
    }

    .header h1 {
        font-size: 27px;
    }
}
</style>
"""


# ================= HOME =================

@app.route("/")
def home():

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>CampusFind AI</title>
<meta name="viewport"
      content="width=device-width, initial-scale=1">
{STYLE}
</head>

<body>

<div class="header">
    <h1>🎓 CampusFind AI</h1>
    <p>Smart Campus Lost & Found</p>
</div>

<div class="container">

<div class="card">

<h2>🔍 Find Lost Items</h2>

<p>
Report lost and found items inside your campus.
</p>

<a class="nav" href="/items">
    🔎 Search Items
</a>

</div>


<div class="card">

<h2>📢 Report Lost Item</h2>

<form action="/report/lost" method="POST">

<label>Item Name</label>
<input type="text"
       name="item_name"
       placeholder="Example: Black Wallet"
       required>

<label>Category</label>
<input type="text"
       name="category"
       placeholder="Wallet / Phone / ID Card">

<label>Color</label>
<input type="text"
       name="color"
       placeholder="Example: Black">

<label>Description</label>
<textarea name="description"
          placeholder="Describe the item"></textarea>

<label>Lost Location</label>
<input type="text"
       name="location"
       placeholder="Library / Canteen">

<label>Time</label>
<input type="text"
       name="time"
       placeholder="10:30 AM">

<label>📞 Contact Number</label>
<input type="tel"
       name="contact"
       placeholder="Enter contact number"
       required>

<button type="submit">
📢 Submit Lost Item
</button>

</form>

</div>


<div class="card">

<h2>📦 Report Found Item</h2>

<form action="/report/found" method="POST">

<label>Item Name</label>
<input type="text"
       name="item_name"
       placeholder="Example: Black Bag"
       required>

<label>Category</label>
<input type="text"
       name="category"
       placeholder="Bag / Phone / ID Card">

<label>Color</label>
<input type="text"
       name="color"
       placeholder="Example: Black">

<label>Description</label>
<textarea name="description"
          placeholder="Describe the item"></textarea>

<label>Found Location</label>
<input type="text"
       name="location"
       placeholder="Library / Canteen">

<label>Time</label>
<input type="text"
       name="time"
       placeholder="11:00 AM">

<label>📞 Contact Number</label>
<input type="tel"
       name="contact"
       placeholder="Enter contact number"
       required>

<button type="submit">
📦 Submit Found Item
</button>

</form>

</div>

</div>

</body>
</html>
"""


# ================= LOST =================

@app.route("/report/lost", methods=["POST"])
def report_lost():

    save_item("Lost")

    return f"""
    {STYLE}

    <div class="container">

    <div class="card">

    <h2>✅ Lost Item Reported!</h2>

    <p>Your lost item has been successfully saved.</p>

    <a class="nav" href="/">⬅ Home</a>

    <a class="nav" href="/items">🔎 View Items</a>

    </div>

    </div>
    """


# ================= FOUND =================

@app.route("/report/found", methods=["POST"])
def report_found():

    save_item("Found")

    return f"""
    {STYLE}

    <div class="container">

    <div class="card">

    <h2>✅ Found Item Reported!</h2>

    <p>Your found item has been successfully saved.</p>

    <a class="nav" href="/">⬅ Home</a>

    <a class="nav" href="/items">🔎 View Items</a>

    </div>

    </div>
    """


# ================= SEARCH / ITEMS =================

@app.route("/items")
def items():

    search = request.args.get("search", "").strip()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search:

        keyword = "%" + search + "%"

        cursor.execute("""
            SELECT * FROM items
            WHERE item_name LIKE ?
               OR category LIKE ?
               OR color LIKE ?
               OR location LIKE ?
               OR description LIKE ?
            ORDER BY id DESC
        """, (
            keyword,
            keyword,
            keyword,
            keyword,
            keyword
        ))

    else:

        cursor.execute("""
            SELECT * FROM items
            ORDER BY id DESC
        """)

    data = cursor.fetchall()

    conn.close()

    html = f"""
<!DOCTYPE html>
<html>

<head>

<title>CampusFind Items</title>

<meta name="viewport"
      content="width=device-width, initial-scale=1">

{STYLE}

</head>

<body>

<div class="header">

<h1>🔍 CampusFind AI</h1>

<p>Lost & Found Items</p>

</div>

<div class="container">

<div class="card">

<h2>🔎 Search Items</h2>

<form action="/items" method="GET">

<input type="text"
       name="search"
       value="{escape(search)}"
       placeholder="Search wallet, phone, library...">

<button type="submit">
Search
</button>

</form>

<br>

<a class="nav" href="/">
⬅ Home
</a>

</div>
"""

    if not data:

        html += """
        <div class="card">
            <h3>No items found 🔎</h3>
            <p>Try another search.</p>
        </div>
        """

    for item in data:

        item_type = escape(str(item[1] or ""))
        item_name = escape(str(item[2] or ""))
        category = escape(str(item[3] or ""))
        color = escape(str(item[4] or ""))
        description = escape(str(item[5] or ""))
        location = escape(str(item[6] or ""))
        time = escape(str(item[7] or ""))
        contact = escape(str(item[8] or ""))

        if item_type == "Found":

            card_class = "found"
            badge_class = "found-badge"
            icon = "📦"

        else:

            card_class = "lost"
            badge_class = "lost-badge"
            icon = "📢"

        html += f"""

<div class="card {card_class}">

<span class="badge {badge_class}">
{icon} {item_type}
</span>

<h2>{item_name}</h2>

<p>
<b>Category:</b> {category}
</p>

<p>
<b>Color:</b> {color}
</p>

<p>
<b>Description:</b> {description}
</p>

<p>
<b>Location:</b> {location}
</p>

<p>
<b>Time:</b> {time}
</p>

<div class="contact">
📞 <b>Contact:</b> {contact}
</div>

</div>
"""

    html += """
</div>

</body>

</html>
"""

    return html


# ================= START =================

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
)
