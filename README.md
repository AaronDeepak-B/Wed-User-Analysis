# Web User Activity Tracker with Dashboar

## Overview

This project is a Flask and Dash-based web application that tracks user login, sign-up, and logout activities in real-time using cookies and sessions. The collected data is stored in an SQLite database and visualized using interactive charts.

## Features

- Tracks user visits, logins, sign-ups, and logouts
- Stores user activity with timestamps, IP addresses, and locations
- Uses SQLite for data persistence
- Displays real-time analytics on a dashboard using Dash and Plotly
- Utilizes Flask sessions and cookies for tracking users

## Installation

### 1. Clone the Repository

```sh

git clone https://github.com/your-username/web-user-tracker.git
cd web-user-tracker
```

### 2. Create a Virtual Environment (Optional but Recommended)

```sh

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```sh

pip install -r requirements.txt
```

### 4. Run the Application

```sh

python app.py
```

The app will run on    `http://127.0.0.1:5000/`

## How It Works

1. **User Tracking**
   
   - When a user visits the site, their session is initialized.
   - Their IP address and location are logged.
   - Events like login, sign-up, and logout are stored in the SQLite database.

3. **Dashboard Visualization**
   
   - The `/dashboard/` route provides a real-time dashboard.
   - Uses Dash and Plotly to display user activities and location data.

   
## Deployment

### Deploy on Heroku (Recommended)

1. Install Heroku CLI:
   
   ```sh
   
   https://devcenter.heroku.com/articles/heroku-cli
   ```
   
2. Log in to Heroku:
   
   ```sh
   
   heroku login
   ```
   
3. Create a Heroku app and deploy:
   
   ```sh
   
   heroku create your-app-name
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```
   
Your app will be live at    `https://your-app-name.herokuapp.com/`


## File Structure

```
web-user-tracker/
│── app.py               # Main Flask application
│── requirements.txt     # Python dependencies
│── Procfile             # For Heroku deployment
│── user_data.db         # SQLite database (auto-created)
│── templates/           # HTML templates (if applicable)
```

## Technologies Used

- **Flask**: Web framework for handling requests and sessions
- **Dash & Plotly**: Interactive data visualization
- **SQLite**: Lightweight database for user activity storage
- **Geocoder**: IP-based location tracking
- **UUID & Sessions**: Unique user identification

## Contributing

Pull requests are welcome! If you'd like to improve the project, feel free to submit PRs.



