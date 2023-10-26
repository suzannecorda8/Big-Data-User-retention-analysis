import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Create a function to handle data analysis and visualization
def analyze_and_visualize_data():
    # Prompt the user to select the dataset CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    if not file_path:
        return  # User canceled the file dialog
    
    # Load the website data into a pandas DataFrame:
    df = pd.read_csv(file_path)

    # Calculate the number of unique users who visited each page:
    unique_users = df.groupby('page')['user_id'].nunique()
    
    # Calculate the retention rate for each page:
    retention_rate = df.groupby('page')['user_id'].apply(lambda x: x.nunique() / x.count())

    # Visualize the results using a bar chart and line plot:
    fig, ax1 = plt.subplots()
    ax1.bar(unique_users.index, unique_users.values)
    ax1.set_ylabel('Unique Users')
    ax2 = ax1.twinx()
    ax2.plot(retention_rate.index, retention_rate.values, color='r')
    ax2.set_ylabel('Retention Rate')
    plt.title('User Views and Retention on bagikopi.id')
    plt.show()

    # Save the figure to a file:
    fig.savefig('user_views_and_retention.png')

# Create a GUI window
root = tk.Tk()
root.title("Data Analysis and Visualization")

# Create a label for instructions
instructions = tk.Label(root, text="Select a CSV file to analyze:")
instructions.pack(pady=10)

# Create a button with custom styling
analyze_button = tk.Button(root, text="Browse and Analyze CSV File", command=analyze_and_visualize_data, bg="#007acc", fg="white", relief="flat", padx=10)
analyze_button.pack(pady=20)

# Run the GUI main loop
root.mainloop()
