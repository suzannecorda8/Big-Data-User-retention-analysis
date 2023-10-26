import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

def analyze_retention_plotly(file_path):
    # Load your data and perform user retention analysis using Plotly
    df = pd.read_csv(file_path)

    # Convert 'timestamp' column to datetime data type
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create a figure with multiple subplots
    fig = make_subplots(rows=2, cols=2, subplot_titles=("User Visits by Page", "Daily User Visits", "User Retention by Page", "Hourly User Visits"))

    # Add trace for user visits by page
    page_visits = df.groupby('page').count()['user_id']
    fig.add_trace(go.Bar(x=page_visits.index, y=page_visits.values), row=1, col=1)

    # Add trace for daily user visits
    daily_visits = df.groupby(df['timestamp'].dt.date).count()['user_id']
    fig.add_trace(go.Scatter(x=daily_visits.index, y=daily_visits.values, mode='lines+markers'), row=1, col=2)

    # Add trace for user retention by page
    page_retention = df.groupby(['page', df['timestamp'].dt.date]).nunique()['user_id'].reset_index()
    fig.add_trace(go.Scatter(x=page_retention[page_retention['page'] == 'Menu']['timestamp'], y=page_retention[page_retention['page'] == 'Menu']['user_id'], mode='lines+markers', name='Menu'), row=2, col=1)
    fig.add_trace(go.Scatter(x=page_retention[page_retention['page'] == 'Outlets']['timestamp'], y=page_retention[page_retention['page'] == 'Outlets']['user_id'], mode='lines+markers', name='Outlets'), row=2, col=1)

    # Add trace for hourly user visits
    hourly_visits = df.groupby(df['timestamp'].dt.hour).count()['user_id']
    fig.add_trace(go.Scatter(x=hourly_visits.index, y=hourly_visits.values, mode='lines+markers'), row=2, col=2)

    # Update figure layout
    fig.update_layout(title="User Analysis Dashboard",
                      xaxis_title="Page/Dates/Hour of Day",
                      yaxis_title="Number of User Visits",
                      height=700,
                      width=1000)

    # Display the Plotly dashboard
    fig.show()

def open_file_dialog(label, entry):
    file_path = filedialog.askopenfilename(title="Select CSV file")
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        label.config(text="File selected: " + file_path)

def analyze_data():
    file_path = file_entry.get()
    if file_path:
        analyze_retention_plotly(file_path)

root = tk.Tk()
root.title("User Retention Analysis (Plotly)")

# Create a frame to hold the content
content_frame = ttk.Frame(root)
content_frame.pack(padx=10, pady=10)

# File selection section
file_label = ttk.Label(content_frame, text="Select a CSV file:")
file_label.pack()
file_entry = ttk.Entry(content_frame, width=40)
file_entry.pack()
browse_button = ttk.Button(content_frame, text="Browse", command=lambda: open_file_dialog(file_label, file_entry))
browse_button.pack()

# Analyze button with custom styling
analyze_button = ttk.Button(content_frame, text="Analyze", command=analyze_data, style="TButton")
analyze_button.pack()

# Style the button with green text and maintain the color
style = ttk.Style()
style.configure("TButton", foreground="green")

# Run the GUI main loop
root.mainloop()
