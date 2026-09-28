from flask import Flask, render_template, request, redirect, session, flash, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import sqlite3
import uuid
import datetime
import os
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Meta WhatsApp Cloud API
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
VERIFY_TOKEN = "police123"

# Twilio WhatsApp
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = "cf0804c929742e877787f08ff822c163"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS police (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            department TEXT,
            station TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tracking_id TEXT,
            person_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            title TEXT,
            description TEXT,
            image TEXT,
            latitude TEXT,
            longitude TEXT,
            department TEXT,
            station TEXT,
            status TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


def send_twilio_whatsapp(to_number, message):
    try:
        print("Sending to:", to_number)

        client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )

        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=to_number
        )

        print("Message SID:", msg.sid)

    except Exception as e:
        print("Twilio Send Error:", str(e))
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
            conn.close()
            flash("Registered Successfully")
            return redirect("/login")

        except Exception as e:
            print("User Register Error:", e)
            flash("Email already exists")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            return redirect("/dashboard")

        flash("Invalid credentials")

    return render_template("login.html")


@app.route("/police_register", methods=["GET", "POST"])
def police_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        station = request.form["station"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO police
                (name, email, password, department, station)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, password, department, station))
            conn.commit()
            conn.close()

            flash("Police Registered Successfully")
            return redirect("/police_login")

        except Exception as e:
            print("Police Register Error:", e)
            flash("Police Register Failed")

    return render_template("police_register.html")


@app.route("/police_login", methods=["GET", "POST"])
def police_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        police = conn.execute(
            "SELECT * FROM police WHERE email=?",
            (email,)
        ).fetchone()
        conn.close()

        if police and check_password_hash(police["password"], password):
            session["police_id"] = police["id"]
            session["police_name"] = police["name"]
            session["police_department"] = police["department"]
            session["police_station"] = police["station"]
            return redirect("/police_dashboard")

        flash("Invalid credentials")

    return render_template("police_login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    complaints = conn.execute(
        "SELECT * FROM complaints WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", complaints=complaints)


@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        person_name = request.form["person_name"]
        phone = request.form["phone"]
        email = request.form.get("email", "")
        address = request.form["address"]
        title = request.form["title"]
        description = request.form["description"]

        department = "Unassigned"
        station = "Unassigned"

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if not latitude or not longitude:
            flash("Please select location on map")
            return redirect("/complaint")

        file = request.files.get("image")
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        tracking_id = "CMP" + uuid.uuid4().hex[:6].upper()
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        conn = get_db()
        conn.execute("""
            INSERT INTO complaints
            (user_id, tracking_id, person_name, phone, email, address,
             title, description, image, latitude, longitude,
             department, station, status, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            tracking_id,
            person_name,
            phone,
            email,
            address,
            title,
            description,
            filename,
            latitude,
            longitude,
            department,
            station,
            "Pending",
            date
        ))

        conn.commit()
        conn.close()

        flash(f"Complaint Submitted! Tracking ID: {tracking_id}")
        return redirect("/dashboard")

    return render_template("complaint.html")


@app.route("/police_dashboard")
def police_dashboard():
    if "police_id" not in session:
        return redirect("/police_login")

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    ).fetchall()

    complaints = [dict(row) for row in rows]
    conn.close()

    return render_template("police_dashboard.html", complaints=complaints)

@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):
    if "police_id" not in session:
        return redirect("/police_login")

    status = request.form["status"]

    conn = get_db()

    complaint = conn.execute(
        "SELECT * FROM complaints WHERE id=?",
        (id,)
    ).fetchone()

    conn.execute(
        "UPDATE complaints SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    if complaint and complaint["phone"]:

        phone = complaint["phone"]

        print("Phone from DB:", phone)

        if not phone.startswith("whatsapp:"):
            phone = phone.replace(" ", "")

            if phone.startswith("+"):
                phone = "whatsapp:" + phone
            elif phone.startswith("91") and len(phone) == 12:
                phone = "whatsapp:+" + phone
            else:
                phone = "whatsapp:+91" + phone

        print("Final WhatsApp number:", phone)

        if status == "Resolved":
            msg = f"""✅ Complaint Resolved

Tracking ID: {complaint['tracking_id']}
Complaint: {complaint['title']}

Your complaint has been successfully resolved.

Thank you for using the Citizen Police Complaint System."""
        else:
            msg = f"""Police Complaint Status Update 🚔

Tracking ID: {complaint['tracking_id']}
Complaint: {complaint['title']}
New Status: {status}

Thank you."""

        send_twilio_whatsapp(phone, msg)

    else:
        print("No phone number found for this complaint")

    return redirect("/police_dashboard")
@app.route("/admin")
def admin():
    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    ).fetchall()

    complaints = [dict(row) for row in rows]

    total = conn.execute(
        "SELECT COUNT(*) FROM complaints"
    ).fetchone()[0]

    pending = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Pending'"
    ).fetchone()[0]

    progress = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='In Progress'"
    ).fetchone()[0]

    resolved = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        complaints=complaints,
        total=total,
        pending=pending,
        progress=progress,
        resolved=resolved
    )
@app.route("/assign_case/<int:id>", methods=["POST"])
def assign_case(id):
    department = request.form["department"]
    station = request.form["station"]

    conn = get_db()

    complaint = conn.execute(
        "SELECT * FROM complaints WHERE id=?",
        (id,)
    ).fetchone()

    conn.execute("""
        UPDATE complaints
        SET department=?, station=?
        WHERE id=?
    """, (department, station, id))

    conn.commit()
    conn.close()

    if complaint and complaint["phone"]:
        phone = complaint["phone"]

        if not phone.startswith("whatsapp:"):
            phone = phone.replace(" ", "")

            if phone.startswith("+"):
                phone = "whatsapp:" + phone
            elif phone.startswith("91") and len(phone) == 12:
                phone = "whatsapp:+" + phone
            else:
                phone = "whatsapp:+91" + phone

        msg = f"""🚔 Complaint Assigned

Tracking ID: {complaint['tracking_id']}

Department: {department}
Police Station: {station}

Your complaint has been assigned and is under review."""

        send_twilio_whatsapp(phone, msg)

    flash("Case assigned successfully")
    return redirect("/admin")

@app.route("/track", methods=["GET", "POST"])
def track():
    complaint = None

    if request.method == "POST":
        tracking_id = request.form["tracking_id"]

        conn = get_db()
        complaint = conn.execute(
            "SELECT * FROM complaints WHERE tracking_id=?",
            (tracking_id,)
        ).fetchone()
        conn.close()

    return render_template("track.html", complaint=complaint)

def auto_categorize_complaint(text):
    text = text.lower()

    if "stolen" in text or "theft" in text or "robbery" in text or "bike" in text or "mobile" in text:
        return "Theft/Robbery"
    elif "accident" in text or "traffic" in text or "signal" in text or "vehicle" in text:
        return "Traffic Police"
    elif "hack" in text or "online" in text or "fraud" in text or "otp" in text or "bank" in text:
        return "Cyber Crime"
    elif "woman" in text or "harassment" in text or "abuse" in text or "domestic" in text:
        return "Women Safety"
    elif "missing" in text or "kidnap" in text or "lost person" in text:
        return "Missing Person"
    elif "noise" in text or "fight" in text or "public" in text or "disturbance" in text:
        return "Public Disturbance"
    else:
        return "General Police"
@app.route("/twilio_whatsapp", methods=["POST"])
def twilio_whatsapp():
    phone = request.form.get("From")
    message = request.form.get("Body", "").strip()

    print("WhatsApp Message:", message)

    response = MessagingResponse()

    # Track complaint by WhatsApp
    if message.upper().startswith("TRACK"):
        parts = message.split()

        if len(parts) < 2:
            response.message(
                "Please send tracking ID like this:\n\nTRACK CMP123456"
            )
            return str(response)

        tracking_id = parts[1].upper()

        conn = get_db()
        complaint = conn.execute(
            "SELECT * FROM complaints WHERE tracking_id=?",
            (tracking_id,)
        ).fetchone()
        conn.close()

        if complaint:
            response.message(
                f"""📌 Complaint Status

Tracking ID: {complaint['tracking_id']}
Status: {complaint['status']}
Department: {complaint['department']}
Police Station: {complaint['station']}
Date: {complaint['date']}"""
            )
        else:
            response.message(
                f"❌ Complaint not found for Tracking ID: {tracking_id}"
            )

        return str(response)

    # Register new complaint
    tracking_id = "CMP" + uuid.uuid4().hex[:6].upper()
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    department = auto_categorize_complaint(message)
    station = "Unassigned"

    conn = get_db()

    conn.execute("""
        INSERT INTO complaints
        (user_id, tracking_id, person_name, phone, email, address,
         title, description, image, latitude, longitude,
         department, station, status, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        None,
        tracking_id,
        "WhatsApp User",
        phone,
        "",
        "",
        "WhatsApp Complaint",
        message,
        None,
        "",
        "",
        department,
        station,
        "Pending",
        date
    ))

    conn.commit()
    conn.close()

    response.message(
        f"""Complaint Registered Successfully ✅

Tracking ID: {tracking_id}
Department: {department}
Status: Pending

Admin will assign your complaint to a police station."""
    )

    return str(response)

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()
    print(data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone = message["from"]

        if "text" in message:
            complaint_text = message["text"]["body"]
        else:
            complaint_text = "Media complaint received from WhatsApp"

        tracking_id = "CMP" + uuid.uuid4().hex[:6].upper()
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        conn = get_db()
        conn.execute("""
            INSERT INTO complaints
            (user_id, tracking_id, person_name, phone, email, address,
             title, description, image, latitude, longitude,
             department, station, status, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            None,
            tracking_id,
            "WhatsApp User",
            "whatsapp:" + phone,
            "",
            "",
            "WhatsApp Complaint",
            complaint_text,
            None,
            "",
            "",
            "Unassigned",
            "Unassigned",
            "Pending",
            date
        ))

        conn.commit()
        conn.close()

        reply = f"""Complaint Registered Successfully ✅

Tracking ID: {tracking_id}
Status: Pending

Your complaint will be assigned to a police department soon."""

        send_twilio_whatsapp(phone, reply)

    except Exception as e:
        print("WhatsApp Webhook Error:", e)

    return jsonify({"status": "success"}), 200


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=False
    )