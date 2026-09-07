from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "NOXEN_CHANGE_THIS_SECRET_KEY"
DATABASE = "noxen.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "noxen123"

def add_booking_status():
    conn = sqlite3.connect(DATABASE)
    try:
        conn.execute("ALTER TABLE bookings ADD COLUMN status TEXT DEFAULT 'Pending'")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()

def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            skill TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        service = request.form.get("service")
        name = request.form.get("name")
        mobile = request.form.get("mobile")
        address = request.form.get("address")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO bookings (service, name, mobile, address) VALUES (?, ?, ?, ?)",
            (service, name, mobile, address)
        )

        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Booking Confirmed - NOXEN</title>
            <style>
                body {{
                    font-family: Arial;
                    background:#f5f6f8;
                    padding:20px;
                }}
                .box {{
                    background:white;
                    padding:25px;
                    border-radius:20px;
                    max-width:500px;
                    margin:30px auto;
                }}
                .success {{
                    font-size:45px;
                }}
                .details {{
                    background:#f5f6f8;
                    padding:15px;
                    border-radius:12px;
                    margin-top:20px;
                    line-height:1.8;
                }}
            </style>
        </head>
        <body>
            <div class="box">
                <div class="success">✅</div>
                <h1>Booking Received!</h1>
                <p>Thank you, <b>{name}</b>.</p>

                <div class="details">
                    <b>Booking ID:</b> #{booking_id}<br>
                    <b>Service:</b> {service}<br>
                    <b>Mobile:</b> {mobile}<br>
                    <b>Address:</b> {address}
                </div>
            </div>
        </body>
        </html>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Book Service - NOXEN</title>
        <style>
            body {
                font-family:Arial;
                background:#f5f6f8;
                padding:20px;
            }
            .box {
                background:white;
                padding:25px;
                border-radius:20px;
                max-width:500px;
                margin:30px auto;
            }
            label {
                display:block;
                margin-top:18px;
                font-weight:bold;
            }
            input, select, textarea {
                width:100%;
                padding:13px;
                margin-top:7px;
                border:1px solid #ddd;
                border-radius:10px;
                box-sizing:border-box;
            }
            button {
                width:100%;
                margin-top:22px;
                padding:15px;
                background:#111827;
                color:white;
                border:none;
                border-radius:12px;
                font-weight:bold;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🔧 Book a NOXEN Service</h1>

            <form method="POST">

                <label>Choose Service</label>
                <select name="service" required>
                    <option value="">Select Service</option>
                    <option>Plumber</option>
                    <option>Electrician</option>
                    <option>AC Service</option>
                    <option>Cleaning</option>
                    <option>Carpenter</option>
                    <option>Painter</option>
                </select>

                <label>Your Name</label>
                <input type="text" name="name"
                       placeholder="Enter your name" required>

                <label>Mobile Number</label>
                <input type="tel" name="mobile"
                       pattern="[0-9]{10}"
                       placeholder="Enter mobile number" required>

                <label>Address</label>
                <textarea name="address" rows="4"
                          placeholder="Enter service address" required></textarea>

                <button type="submit">Continue Booking</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/worker", methods=["GET", "POST"])
def worker():
    if request.method == "POST":
        name = request.form.get("name")
        mobile = request.form.get("mobile")
        skill = request.form.get("skill")
        address = request.form.get("address")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, mobile, skill, address) VALUES (?, ?, ?, ?)",
            (name, mobile, skill, address)
        )
        worker_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return f"<h1>✅ Registration Successful!</h1><p>Worker ID: #{worker_id}</p><p>Welcome to NOXEN.</p>"

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Join NOXEN</title>
    </head>
    <body style="font-family:Arial;background:#f5f6f8;padding:20px">
        <div style="background:white;padding:25px;border-radius:20px;max-width:500px;margin:30px auto">
            <h1>👷 Join NOXEN</h1>
            <p>Apni skill ke according kaam kijiye.</p>
            <form method="POST">
                <input name="name" placeholder="Your Name" required style="width:100%;padding:13px;margin-top:15px;box-sizing:border-box">
                <input name="mobile" type="tel" pattern="[0-9]{10}" placeholder="Mobile Number" required style="width:100%;padding:13px;margin-top:15px;box-sizing:border-box">
                <input name="skill" placeholder="Your Skill (e.g. Plumber)" required style="width:100%;padding:13px;margin-top:15px;box-sizing:border-box">
                <textarea name="address" placeholder="Your Address" required style="width:100%;padding:13px;margin-top:15px;box-sizing:border-box"></textarea>
                <button type="submit" style="width:100%;padding:15px;margin-top:20px;background:#111827;color:white;border:0;border-radius:12px">Register as Worker</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        error = "Invalid username or password."

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NOXEN Admin Login</title>
        <style>
            body {{
                font-family:Arial;
                background:#f5f6f8;
                padding:20px;
            }}
            .box {{
                background:white;
                padding:25px;
                border-radius:20px;
                max-width:400px;
                margin:70px auto;
            }}
            input {{
                width:100%;
                padding:14px;
                margin-top:10px;
                border:1px solid #ddd;
                border-radius:10px;
                box-sizing:border-box;
            }}
            button {{
                width:100%;
                margin-top:20px;
                padding:15px;
                background:#111827;
                color:white;
                border:0;
                border-radius:12px;
                font-weight:bold;
            }}
            .error {{
                color:#dc2626;
                margin-top:15px;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🔐 NOXEN Admin</h1>

            <form method="POST">
                <input type="text" name="username"
                       placeholder="Username" required>

                <input type="password" name="password"
                       placeholder="Password" required>

                <button type="submit">Login</button>
            </form>

            <div class="error">{error}</div>
        </div>
    </body>
    </html>
    """

@app.route("/admin/booking/<int:booking_id>/accept", methods=["POST"])
def accept_booking(booking_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DATABASE)
    conn.execute(
        "UPDATE bookings SET status = 'Accepted' WHERE id = ?",
        (booking_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    bookings = conn.execute(
        "SELECT * FROM bookings ORDER BY id DESC"
    ).fetchall()

    workers = conn.execute(
        "SELECT * FROM workers ORDER BY id DESC"
    ).fetchall()

    conn.close()

    booking_rows = ""

    for b in bookings:
        booking_rows += f"""
        <tr>
            <td>#{b['id']}</td>
            <td>{b['service']}</td>
            <td>{b['name']}</td>
            <td>{b['mobile']}</td>
            <td>{b['address']}</td>
            <td>{b['status']}</td>
        </tr>
        """

    if not booking_rows:
        booking_rows = """
        <tr>
            <td colspan="5">No bookings yet.</td>
        </tr>
        """

    worker_rows = ""

    for w in workers:
        worker_rows += f"""
        <tr>
            <td>#{w['id']}</td>
            <td>{w['name']}</td>
            <td>{w['mobile']}</td>
            <td>{w['skill']}</td>
            <td>{w['address']}</td>
        </tr>
        """

    if not worker_rows:
        worker_rows = """
        <tr>
            <td colspan="5">No workers yet.</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NOXEN Admin Panel</title>
        <style>
            body {{
                font-family:Arial;
                background:#f5f6f8;
                padding:20px;
            }}
            .box {{
                background:white;
                padding:20px;
                border-radius:20px;
                overflow-x:auto;
                margin-bottom:25px;
            }}
            table {{
                width:100%;
                border-collapse:collapse;
                margin-top:15px;
                min-width:650px;
            }}
            th, td {{
                padding:12px;
                border-bottom:1px solid #ddd;
                text-align:left;
            }}
            th {{
                background:#111827;
                color:white;
            }}
        </style>
    </head>
    <body>

        <div class="box">
            <h1>🔐 NOXEN Admin Panel</h1>
            <p>Total Bookings: <b>{len(bookings)}</b></p>
            <p>Total Workers: <b>{len(workers)}</b></p>
        </div>

        <div class="box">
            <h2>👷 Registered Workers</h2>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Mobile</th>
                    <th>Skill</th>
                    <th>Address</th>
                    <th>Status</th>
                </tr>
                {worker_rows}
            </table>
        </div>

        <div class="box">
            <h2>📋 Customer Bookings</h2>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Name</th>
                    <th>Mobile</th>
                    <th>Status</th>
<th>Address</th>
                </tr>
                {booking_rows}
            </table>
        </div>

    </body>
    </html>
    """

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

init_db()


@app.route("/worker/update/<int:booking_id>/<status>")
def update_booking_status(booking_id, status):
    allowed = ["Pending", "Accepted", "Rejected", "Completed"]

    if status not in allowed:
        return "Invalid status", 400

    conn = sqlite3.connect(DATABASE)
    conn.execute(
        "UPDATE bookings SET status = ? WHERE id = ?",
        (status, booking_id)
    )
    conn.commit()
    conn.close()

    return redirect("/worker/dashboard")


@app.route("/worker/login", methods=["GET", "POST"])
def worker_login():
    if request.method == "POST":
        mobile = request.form.get("mobile", "").strip()

        conn = sqlite3.connect(DATABASE)
        worker = conn.execute(
            "SELECT * FROM workers WHERE mobile = ?",
            (mobile,)
        ).fetchone()
        conn.close()

        if worker:
            return redirect("/worker/dashboard?mobile=" + mobile)

        return """
        <h3>Worker not found</h3>
        <a href="/worker/login">Try Again</a>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Worker Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial;
                background: #f5f6f8;
                padding: 20px;
            }
            .box {
                background: white;
                max-width: 400px;
                margin: 80px auto;
                padding: 25px;
                border-radius: 20px;
            }
            input, button {
                width: 100%;
                padding: 14px;
                margin-top: 12px;
                box-sizing: border-box;
            }
            button {
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>👷 Worker Login</h2>
            <form method="POST">
                <input
                    type="tel"
                    name="mobile"
                    placeholder="Enter mobile number"
                    required
                >
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/worker/dashboard")
def worker_dashboard():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    worker_id = request.args.get("worker_id")

    rows = conn.execute(
        "SELECT * FROM bookings WHERE worker_id = ? ORDER BY id DESC",
        (worker_id,)
    ).fetchall()

    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Worker Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial;
                background: #f5f6f8;
                padding: 20px;
            }

            .box {
                background: white;
                padding: 25px;
                border-radius: 20px;
                max-width: 800px;
                margin: 30px auto;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }

            th, td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }

            th {
                background: #f1f1f1;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Worker Dashboard</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Name</th>
                    <th>Mobile</th>
                    <th>Address</th>
                </tr>
    """

    for row in rows:
        html += f"""
                <tr>
                    <td>{row['id']}</td>
                    <td>{row['service']}</td>
                    <td>{row['name']}</td>
                    <td>{row['mobile']}</td>
                    <td>{row['address']}</td>
                    <td>
                        <b>{row['status']}</b><br>
                        <a href="/worker/update/{row['id']}/Accepted">Accept</a> |
                        <a href="/worker/update/{row['id']}/Rejected">Reject</a> |
                        <a href="/worker/update/{row['id']}/Completed">Complete</a>
                    </td>
                </tr>
        """

    html += """
            </table>
        </div>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
