import tkinter as tk
from tkinter import ttk, Label, filedialog  # Import specific components from tkinter.
import pandas as pd  # For data manipulation.
from matplotlib.figure import Figure  # For creating figures.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # For embedding Matplotlib figures in tkinter.
import matplotlib.pyplot as plt  # For data visualization.
from matplotlib.ticker import AutoMinorLocator  # For fine-grained tick control.


# Function to center the main window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# Function to display CSV data
def display_csv_data(_=None):
    try:
        csv_file = 'supermarket_sales.csv'
        df = pd.read_csv(csv_file)

        # Clear the existing frame
        for widget in display_frame.winfo_children():
            widget.destroy()

        # Creating widget to display the CSV data
        tree = ttk.Treeview(display_frame)
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        # Add headers
        for column in df.columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        # Inserting data rows
        for row in df.itertuples(index=False):
            tree.insert("", "end", values=row)

        # allowing it to fill both horizontally and vertically, and expand to available space
        tree.pack(side="left", fill="both", expand=True)

        # Adding scrollbar to the right of the dataset frame
        y_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=y_scrollbar.set)

        # Disable the Dataset label and visually indicate the Dashboard label as active
        dataset_label.config(state=tk.DISABLED, fg="gray", bg="white")
        dashboard_label.config(state=tk.NORMAL, fg="white", bg="black")
    except Exception as e:
        print(f"Error: {e}")


# Function to open the dashboard
def show_dashboard(_=None):
    for widget in display_frame.winfo_children():
        widget.destroy()
    dashboard_label.config(state=tk.DISABLED, fg="gray", bg="white")
    dataset_label.config(state=tk.NORMAL, fg="white", bg="black")

    # Creating a Canvas widget for data visualizations
    canvas = tk.Canvas(display_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Creating frame inside the Canvas
    dashboard_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=dashboard_frame, anchor="nw")

    # Display data visualizations on the dashboard
    display_pie_chart(dashboard_frame)
    display_horizontal_bar_chart(dashboard_frame)
    display_bar_chart(dashboard_frame)
    display_line_chart(dashboard_frame)


# Function to display the pie chart
def display_pie_chart(_):
    label1 = Label(display_frame, text="City-Based Sales Analysis", font=("Times", 15))
    label1.place(relx=0.04, rely=0.001, relwidth=0.3, relheight=0.1, x=10)

    percentages = [34.25, 19.97, 32.88, 12.90]
    cities = ['Phoenix', 'Seattle', 'St.\nLouis', 'Texas']
    p_colors = ['red', 'violet', 'orange', 'green']

    fig1 = Figure(figsize=(4, 4), dpi=100)

    ax = fig1.add_subplot(111)
    ax.pie(percentages, labels=cities, autopct='%1.2f%%', startangle=90, colors=p_colors)
    fig1.set_facecolor('#F0F8FF')

    canvas1 = FigureCanvasTkAgg(fig1, master=display_frame)
    canvas1.get_tk_widget().pack()
    canvas1.get_tk_widget().place(relx=0.09, rely=0.07)
    canvas1.get_tk_widget().place(relwidth=0.2, relheight=0.4)


# Function to display the horizontal bar chart
def display_horizontal_bar_chart(_):
    label2 = Label(display_frame, text="Revenue by Product Segment", font=("Times", 15))
    label2.place(relx=0.44, rely=0.001, relwidth=0.3, relheight=0.1, x=10)

    sold_count = [178, 152, 170, 174, 166, 160]
    products = ['Fashion Accessories', 'Health and beauty', 'Electronic accessories', 'Food and beverages',
                'Sports and travel', 'Home and lifestyle']
    colors = ['red', 'green', 'blue', 'orange', 'cyan', 'purple']

    fig2 = Figure(figsize=(15, 5), dpi=70)

    ax2 = fig2.add_subplot(111)
    bars = ax2.barh(products, sold_count)
    for i in range(len(colors)):
        bars[i].set_color(colors[i])

    ax2.set_xlabel("Sold Count")
    ax2.set_ylabel("Product Line")

    for i in range(len(products)):
        if products[i] == 'Health and beauty':
            ax2.text(sold_count[i] + 5, i, 'Min', va='center', rotation=90)
        elif products[i] == 'Fashion Accessories':
            ax2.text(sold_count[i] + 5, i, 'Max', va='center', rotation=90)

    ax2.xaxis.grid(True)

    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    fig2.set_facecolor('#F0F8FF')

    canvas2 = FigureCanvasTkAgg(fig2, master=display_frame)
    canvas2.get_tk_widget().place(relx=0.35, rely=0.07)
    canvas2.get_tk_widget().place(relwidth=0.6, relheight=0.4)


# Function to display the bar chart
def display_bar_chart(_):
    label3 = Label(display_frame, text="Payment Method Preferences", font=("Times", 15))
    label3.place(relx=0.07, rely=0.47, relwidth=0.3, relheight=0.1, x=10)

    payment_methods = ["E-wallet", "Crypto", "Mobile", "Gift Cards", "Cash", "Credit"]
    counts = [133, 12, 213, 183, 148, 311]
    colors = ["yellow", "black", "green", "orange", "violet", "red"]

    fig3 = Figure(figsize=(6, 4), dpi=70)
    ax = fig3.add_subplot(111)

    bars = ax.bar(payment_methods, counts, color=colors)

    ax.set_xlabel("Payment")
    ax.set_ylabel("Count")

    for bar, payment in zip(bars, payment_methods):
        if payment == "Crypto":
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, "Min", ha="center")
        elif payment == "Credit":
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, "Max", ha="center")

    ax.yaxis.grid(True)

    ax.yaxis.set_minor_locator(AutoMinorLocator())
    fig3.set_facecolor('#F0F8FF')

    canvas3 = FigureCanvasTkAgg(fig3, master=display_frame)
    canvas3.get_tk_widget().place(relx=0.05, rely=0.54)
    canvas3.get_tk_widget().place(relwidth=0.35, relheight=0.43)


# Creating tooltip for line chart
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

    def show_tooltip(self, _):
        # Tooltip size and position
        x, y, _, _ = self.widget.bbox("current")
        x += self.widget.winfo_rootx() + 730
        y += self.widget.winfo_rooty() - 75

        # Create a new Toplevel window for the tooltip
        self.tooltip = tk.Toplevel(self.widget)

        # Set the Toplevel window to override the system window manager
        self.tooltip.wm_overrideredirect(True)

        # Set the size and position of the tooltip window
        self.tooltip.wm_geometry(f"+{x}+{y}")

        # Create a label widget within the tooltip to display the provided text
        label = tk.Label(self.tooltip, text=self.text, background="#FFD39B", relief="solid",
                         borderwidth=1, font=("Times", 10))
        label.pack()

    def hide_tooltip(self, _):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# Function to display the line chart
def display_line_chart(_):
    label4 = Label(display_frame, text="City-Wise Best Sellers", font=("Times", 15))
    label4.place(relx=0.50, rely=0.47, relwidth=0.3, relheight=0.1, x=10)

    cities = [
        "P1", "P2", "P3", "P4", "P5", "P6",
        "S1", "S2", "S3", "S4", "S5", "S6",
        "L1", "L2", "L3", "L4", "L5", "L6",
        "T1", "T2", "T3", "T4", "T5", "T6",
    ]

    total_sales = [
        23766, 21560, 18968, 16615, 15761, 13895, 15369, 12624, 10291, 8960, 8750.049, 8546.265,
        19988, 19980, 17549, 17051, 16413, 15214, 8616, 8025, 7582, 7048, 6748, 3637,
    ]

    fig4, ax = plt.subplots(figsize=(6, 4))

    ax.plot(cities, total_sales, marker='o')
    ax.set_ylabel("Total Sales")

    x_positions = range(len(cities))
    ax.set_xticks(x_positions)
    ax.set_xticklabels(cities, rotation=90)

    ax.grid(True)

    ax.xaxis.set_minor_locator(AutoMinorLocator())

    fig4.set_facecolor('#F0F8FF')

    canvas4 = FigureCanvasTkAgg(fig4, master=display_frame)
    canvas4.get_tk_widget().place(relx=0.44, rely=0.54, relwidth=0.51, relheight=0.43)

    # Tooltip text
    tooltip = ToolTip(canvas4.get_tk_widget(), "P1= Phoenix (Food and beverages)\n"
                                               "P2= Phoenix (Fashion accessories)\n"
                                               "P3= Phoenix (Electronic accessories)\n"
                                               "P4= Phoenix (Health and beauty)\n"
                                               "P5= Phoenix (Sports and travel)\n"
                                               "P6= Phoenix (Home and lifestyle)\n"
                                               "S1= Seattle (Home and lifestyle)\n"
                                               "S2= Seattle (Sports and travel)\n"
                                               "S3= Seattle (Electronic accessories)\n"
                                               "S4= Seattle (Health and beauty)\n"
                                               "S5= Seattle (Fashion accessories)\n"
                                               "S6= Seattle (Food and beverages)\n"
                                               "L1= St.Louis (Sports and travel)\n"
                                               "L2= St.Louis (Health and beauty)\n"
                                               "L3= St.Louis (Home and lifestyle)\n"
                                               "L4= St.Louis (Electronic accessories)\n"
                                               "L5= St.Louis (Fashion accessories)\n"
                                               "L6= St.Louis (Food and beverages)\n"
                                               "T1= Texas (Food and beverages)\n"
                                               "T2= Texas (Electronic accessories)\n"
                                               "T3= Texas (Fashion accessories)\n"
                                               "T4= Texas (Home and lifestyle)\n"
                                               "T5= Texas (Sports and travel)\n"
                                               "T6= Texas (Health and beauty)")

    def on_hover(event):
        tooltip.show_tooltip(event)

    def on_leave(event):
        tooltip.hide_tooltip(event)

    canvas4.get_tk_widget().bind("<Enter>", on_hover)
    canvas4.get_tk_widget().bind("<Leave>", on_leave)


# Function to export the displayed dataset to an Excel file
def export_to_excel():
    try:
        # Selecting the displayed data which is in a .csv file
        csv_file = 'supermarket_sales.csv'
        df = pd.read_csv(csv_file)

        # Select a path for saving the file
        save_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel Files", "*.xlsx")])

        # Checking if the user canceled download
        if not save_path:
            return

        # Export the DataFrame to an Excel file
        df.to_excel(save_path, index=False)
    except Exception as e:
        print(f"An error occurred while exporting: {e}")


# Main window
data = tk.Tk()
data.title("Supermarket Stats Dashboard")
data.state("zoomed")
data.resizable(False, False)
center_window(data, 1920, 1080)
data.configure(bg="white")

# Upper frame and titles
upper_frame = tk.Frame(data, bg="#3D59AB", height=50)
upper_frame.pack(side="top", fill="x")

title_label = tk.Label(upper_frame, text="Supermarket Sales Dashboard", bg="#3D59AB", fg="black", font=("Courier", 24),
                       borderwidth=2, relief="ridge")
title_label.pack(pady=10)

# Side Frame and titles
side_frame = tk.Frame(data, bg="#3D59AB", width=200)
side_frame.pack(side="left", fill="y")

dataset_label = tk.Label(side_frame, text="Dataset", bg="black", fg="white", font=("Courier", 18), borderwidth=2,
                         relief="ridge", cursor="hand2")
dataset_label.pack(pady=100, padx=10)
dataset_label.bind("<Button-1>", display_csv_data)

dashboard_label = tk.Label(side_frame, text="Dashboard", bg="black", fg="white", font=("Courier", 18), borderwidth=2,
                           relief="ridge", cursor="hand2")
dashboard_label.pack(pady=1, padx=10)
dashboard_label.bind("<Button-1>", show_dashboard)

# Download button
download_button = tk.Button(side_frame, text="Download\ndataset", bg="black", fg="white",
                            font=("Courier", 12), borderwidth=2, relief="ridge", cursor="hand2",
                            command=export_to_excel)
download_button.place(relx=0.5, rely=1.0, anchor="s", bordermode="outside", y=-80)

# Creating a frame to display the data and pack it on the right side of the main window,
display_frame = tk.Frame(data)
display_frame.pack(side="right", fill="both", expand=True)

# Call the function to initially display the CSV data.
display_csv_data()

# Start the main event loop
data.mainloop()
