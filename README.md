Absolutely. Replace the **entire contents** of your `README.md` with this:

````markdown
# Citizen Police Complaint System

A web-based Citizen Police Complaint System developed using Flask and SQLite. The system allows citizens to submit police complaints online, track complaint status, upload evidence images, and select the complaint location on an interactive map.

The system also provides separate dashboards for citizens, police personnel, and administrators.

---

## 📌 Project Overview

The **Citizen Police Complaint System** is designed to provide a simple online platform for registering and managing police complaints.

Instead of depending completely on manual complaint registration, citizens can submit complaints through a web application. Each complaint receives a unique **Tracking ID**, which can be used to track the complaint status.

Police personnel can view assigned complaints, examine complaint details and evidence, view the complaint location, and update the complaint status.

Administrators can monitor complaints and assign cases to appropriate departments and police stations.

---

## 🎯 Objectives

- Provide an online platform for citizens to submit complaints.
- Reduce manual paperwork involved in complaint registration.
- Generate a unique Tracking ID for every complaint.
- Allow citizens to track their complaints.
- Allow citizens to upload supporting evidence images.
- Capture complaint locations using an interactive map.
- Provide separate dashboards for citizens, police, and administrators.
- Allow police personnel to update complaint status.
- Provide WhatsApp notifications for complaint-related updates.
- Centralize complaint information in a database.

---

## 🚀 Main Features

### 👤 Citizen Module

- Citizen registration
- Citizen login
- Secure password storage
- Online complaint registration
- Complaint title and description
- Upload complaint evidence images
- Select complaint location using a map
- Automatic Tracking ID generation
- View submitted complaints
- Track complaint status
- Logout functionality

### 👮 Police Module

- Police registration
- Police login
- Police dashboard
- View assigned complaints
- View complaint details
- View uploaded evidence
- View complaint location
- Update complaint status
- Track complaint information

### 🛡️ Admin Module

- Admin dashboard
- View registered complaints
- Monitor complaint status
- Assign complaints to departments
- Assign complaints to police stations
- Monitor complaint information

### 🗺️ Map Module

The system uses:

- OpenStreetMap
- Leaflet.js

Citizens can select the complaint location on an interactive map.

Police personnel can view the saved complaint location from the police dashboard.

### 📱 WhatsApp Integration

The project includes WhatsApp integration using Twilio.

The system can be used for:

- Complaint-related WhatsApp messages
- Complaint tracking requests
- Complaint assignment notifications
- Complaint status notifications

---

## 🔄 System Workflow

```text
Citizen
   |
   v
Register / Login
   |
   v
Submit Complaint
   |
   +---- Complaint Description
   |
   +---- Evidence Image
   |
   +---- Location
   |
   v
Tracking ID Generated
   |
   v
Admin Dashboard
   |
   v
Assign Department / Police Station
   |
   v
Police Dashboard
   |
   v
Police Reviews Complaint
   |
   v
Status Updated
   |
   v
Citizen Tracks Complaint
   |
   v
WhatsApp Notification
````

---

## 🏗️ System Architecture

```text
                    Citizen
                       |
                       v
              Flask Web Application
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
   Complaint       Tracking ID     Image Upload
   Registration    Generation
        |              |              |
        +--------------+--------------+
                       |
                       v
                  SQLite Database
                       |
          +------------+------------+
          |                         |
          v                         v
    Admin Dashboard          Police Dashboard
          |                         |
          v                         v
 Department / Station        Status Update
 Assignment                       |
                                  v
                         Citizen Notification
                                  |
                                  v
                           WhatsApp / Twilio
```

---

## 🛠️ Technologies Used

| Technology    | Purpose                                   |
| ------------- | ----------------------------------------- |
| Python        | Backend programming                       |
| Flask         | Web application framework                 |
| SQLite        | Database                                  |
| HTML5         | Web page structure                        |
| CSS3          | Styling                                   |
| Bootstrap 5   | Responsive user interface                 |
| JavaScript    | Client-side functionality                 |
| Jinja2        | Flask template rendering                  |
| Leaflet.js    | Interactive maps                          |
| OpenStreetMap | Map data                                  |
| Twilio        | WhatsApp integration                      |
| Werkzeug      | Password hashing and secure file handling |

---

## 📂 Project Structure

```text
Police-Complaint-System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── check_db.py
├── update_db.py
│
├── templates/
│   ├── admin.html
│   ├── complaint.html
│   ├── dashboard.html
│   ├── home.html
│   ├── login.html
│   ├── police_dashboard.html
│   ├── police_login.html
│   ├── police_register.html
│   ├── register.html
│   └── track.html
│
└── static/
    ├── style.css
    └── uploads/
```

> Note: `database.db` and uploaded evidence files are intentionally excluded from GitHub using `.gitignore`.

---

## 🗄️ Database

The project uses **SQLite** for storing application data.

### Users Table

Stores citizen account information.

Example fields:

```text
id
name
email
password
department
```

### Police Table

Stores police personnel account information.

Example fields:

```text
id
name
email
password
department
station
```

### Complaints Table

Stores complaint information.

Example fields:

```text
id
user_id
tracking_id
title
description
image
status
date
latitude
longitude
phone
```

---

## 🆔 Tracking ID

Every complaint receives a unique Tracking ID.

Example:

```text
CMP-XXXXXXXX
```

The Tracking ID allows citizens to identify and track their complaint.

---

## 📍 Complaint Location

The complaint form includes an interactive Leaflet map.

The citizen can select the complaint location on the map.

The application stores:

```text
Latitude
Longitude
```

These coordinates can later be displayed on the police dashboard.

---

## 📊 Complaint Status

The complaint status can be updated by authorized police personnel.

Example statuses:

```text
Pending
Under Investigation
Resolved
```

The citizen can view the updated status from the complaint dashboard or tracking page.

---

## 📱 WhatsApp Notification

The project supports WhatsApp communication through **Twilio**.

Example notification flow:

```text
Complaint Submitted
        |
        v
Complaint Assigned
        |
        v
Police Updates Status
        |
        v
WhatsApp Notification
        |
        v
Citizen
```

### Example Message

```text
Police Complaint Update

Tracking ID: CMP-12345678
Complaint: Example Complaint
Status: Under Investigation

Please use the tracking ID to check your complaint status.
```

---

## 🔐 Security

The project includes basic security measures such as:

* Password hashing using Werkzeug
* Session-based authentication
* Secure filename handling for uploaded files
* `.gitignore` for sensitive/local files
* Separate citizen and police authentication

### Important

This project is currently intended for **academic, demonstration, and local development purposes**.

Before production deployment, additional security measures should be implemented, including:

* Environment variables for secrets
* Strong authentication and authorization
* Admin authentication
* CSRF protection
* Input validation
* File type and file size validation
* Secure webhook verification
* HTTPS
* Production database
* Proper access control
* Audit logging

---

## 💻 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Rakesh-kumar0055/Police-Complaint-System.git
```

### 2. Open the Project

```bash
cd Police-Complaint-System
```

### 3. Create a Virtual Environment

Windows:

```powershell
py -m venv .venv
```

### 4. Activate the Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 6. Run the Application

```powershell
python app.py
```

### 7. Open in Browser

```text
http://localhost:5000
```

---

## 📦 Requirements

The main requirements include:

```text
Flask
Werkzeug
Twilio
```

The complete dependency list is available in:

```text
requirements.txt
```

---

## 🧪 Testing

The system can be tested using the following workflows.

### Citizen Testing

1. Register a citizen account.
2. Login.
3. Submit a complaint.
4. Upload an image.
5. Select a location.
6. Submit the complaint.
7. Copy the generated Tracking ID.
8. Check the complaint from the dashboard.
9. Track the complaint using the Tracking ID.

### Police Testing

1. Register/login as police personnel.
2. Open the police dashboard.
3. View assigned complaints.
4. Open complaint details.
5. View evidence.
6. View complaint location.
7. Update complaint status.

### Admin Testing

1. Login to the admin panel.
2. View complaints.
3. Assign department.
4. Assign police station.
5. Monitor complaint information.

---

## 🧰 Database Utilities

The project contains utility scripts for database-related operations.

### `check_db.py`

Used to inspect complaint information and saved coordinates.

Run:

```powershell
python check_db.py
```

### `update_db.py`

Used during development for database schema updates.

Run only when a database schema change is required:

```powershell
python update_db.py
```

> Do not repeatedly run database migration commands if the columns already exist.

---

## 🌐 Main Routes

| Route               | Purpose                 |
| ------------------- | ----------------------- |
| `/`                 | Home page               |
| `/register`         | Citizen registration    |
| `/login`            | Citizen login           |
| `/dashboard`        | Citizen dashboard       |
| `/complaint`        | Submit complaint        |
| `/track`            | Track complaint         |
| `/police_register`  | Police registration     |
| `/police_login`     | Police login            |
| `/police_dashboard` | Police dashboard        |
| `/admin`            | Admin dashboard         |
| `/twilio_whatsapp`  | Twilio WhatsApp webhook |
| `/webhook`          | WhatsApp/Meta webhook   |

---

## 📁 Files Not Published to GitHub

For security and privacy, the following files/data should not be published:

```text
database.db
*.db
.env
static/uploads/*
```

The `.gitignore` file is configured to prevent these files from being committed accidentally.

**Do not upload:**

* Real citizen complaint data
* Real phone numbers
* Evidence images
* Passwords
* API keys
* Twilio credentials
* Access tokens
* Secret keys

---

## 🔮 Future Enhancements

Possible future improvements include:

* AI-based complaint categorization
* Automatic department assignment
* Email notifications
* Improved WhatsApp integration
* Mobile application
* Advanced admin analytics
* Complaint priority detection
* Police station geolocation
* Real-time complaint notifications
* Digital audit trail
* Role-based access control
* Production database such as PostgreSQL
* Cloud deployment
* Advanced security and monitoring

---

## 📌 Project Highlights

```text
✔ Flask Web Application
✔ Citizen Complaint Registration
✔ Police Dashboard
✔ Admin Dashboard
✔ Complaint Tracking ID
✔ Complaint Status Management
✔ Evidence Image Upload
✔ Interactive Map
✔ OpenStreetMap Integration
✔ Leaflet.js Integration
✔ SQLite Database
✔ WhatsApp Integration
✔ Separate User and Police Workflows
```

---

## 🎓 Project Type

**Academic / Final Year Project**

### Project Title

**Web-Based Citizen Police Complaint System**

### Developer

**Rakesh Kumar A N**

### GitHub

**Rakesh-kumar0055**

---

## 📄 License

This project is intended for educational and academic purposes.

You may modify and extend the project for learning and demonstration purposes.

```

### Now do this

1. Open `README.md`
2. Press **Ctrl + A**
3. Delete everything
4. Paste the complete README above
5. Press **Ctrl + S**

**Do not run `git pull` again.**

After saving, tell me **“README done”**. Then we'll fix the `register.html` conflict.
```
