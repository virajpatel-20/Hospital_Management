# MediCare — Hospital Management System (Improved)

## Project Structure
```
Hospital_Management/
├── backend/
│   ├── app.py               # Flask app entry point
│   ├── database.py          # MongoDB connection
│   └── routes/
│       ├── auth.py          # Register, login, profile, doctors
│       ├── appointment.py   # Booking, viewing, cancelling
│       ├── doctor.py        # Doctor appointment management
│       └── admin.py         # Admin stats and user management
├── frontend/
│   ├── css/style.css        # Full design system
│   ├── js/
│   │   ├── main.js          # Shared utilities, API, toast
│   │   └── sidebar.js       # Sidebar templates per role
│   ├── login.html           # Login page
│   ├── register.html        # Patient registration
│   ├── patient/
│   │   ├── dashboard.html   # Stats + recent appointments
│   │   ├── book.html        # Doctor search + booking form
│   │   ├── appointments.html # Full history with filters
│   │   └── profile.html     # Edit patient profile
│   ├── doctor/
│   │   ├── dashboard.html   # Pending overview + quick actions
│   │   ├── appointments.html # Full management (approve/complete/cancel)
│   │   └── profile.html     # Edit doctor profile
│   └── admin/
│       ├── dashboard.html   # System stats overview
│       ├── appointments.html # All appointments with filters
│       ├── users.html       # User management
│       └── add-doctor.html  # Register new doctor
└── requirements.txt
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB
Ensure MongoDB is running on `localhost:27017`

### 3. Run the backend
```bash
cd backend
python app.py
```

### 4. Open frontend
Open `frontend/login.html` in your browser.

## Features Implemented
- ✅ Password encryption with bcrypt
- ✅ Role-based access control (Patient / Doctor / Admin)
- ✅ Full appointment workflow (Pending → Approved → Completed)
- ✅ Form validation (frontend + backend)
- ✅ Dashboard pages for all 3 roles
- ✅ Search & filter functionality
- ✅ Appointment history
- ✅ Error handling with proper HTTP status codes
- ✅ Toast notifications
- ✅ Doctor search and selection
- ✅ Admin user management (activate/deactivate/delete)
- ✅ Profile editing
- ✅ Modern, responsive UI design

## Demo Credentials
Create accounts via:
- Admin: POST /register with role "admin" (seed manually or modify auth.py)
- Doctor: POST /register-doctor (via admin panel)
- Patient: Register via /register.html
