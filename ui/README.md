# Hyprmonitor Web UI

This is a Flask-based web interface to view and interact with the data from the JSON files stored in /home/$USER/.config/hypr/hyprmonitor.

Features:
- View application usage statistics (current and by date)
- View tab/window usage statistics
- Search for application/tab usage
- Download raw JSON logs

To run:
1. Install requirements: `pip install flask`
2. Run: `python app.py`
3. Open http://localhost:5000 in your browser
