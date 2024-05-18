import tkinter as tk
import psutil
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ping3

# Function to measure ping to a given host
def measure_ping(host):
    try:
        # Perform ping and get the round-trip time (in seconds)
        ping_time = ping3.ping(host)
        if ping_time is not None:
            return ping_time * 1000  # Convert to milliseconds
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

# Function to update the ping label with the latest ping result
def update_ping_label():
    ping_result = measure_ping("www.google.com")  
    if ping_result is not None:
        ping_label.config(text=f"Ping: {ping_result:.2f} ms")
    else:
        ping_label.config(text="Failed to ping")
        
    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_ping_label)
    
# Function to get the network speed (upload and download) in KB/s
def get_net_speed():
    old_stat = psutil.net_io_counters()
    time.sleep(1)
    new_stat = psutil.net_io_counters()
    
    # Convert to KB/s
    bytes_sent = (new_stat.bytes_sent - old_stat.bytes_sent) / 1024
    bytes_recv = (new_stat.bytes_recv - old_stat.bytes_recv) / 1024
    
    print("Bytes sent:", bytes_sent)
    print("Bytes received:", bytes_recv)
    
    return bytes_sent, bytes_recv

# Function to update the GUI with the latest network speed values
def update_gui():
    # Get the latest values from the graph
    if upload_speeds and download_speeds:
        sent = upload_speeds[-1]
        recv = download_speeds[-1]
    
        print("Latest upload speed:", sent)
        print("Latest download speed:", recv)
    
        # Update upload speed label
        upload_speed_label.config(text=f"Upload: {sent:.2f} KB/s")
    
        # Update download speed label
        download_speed_label.config(text=f"Download: {recv:.2f} KB/s")

    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_gui)

# Function to update the plot with the latest network speed data
def update_plot(frame):
    sent, recv = get_net_speed()
    upload_speeds.append(sent)
    download_speeds.append(recv)
    
    ax.clear()  # Clear the previous plot
    ax.plot(upload_speeds, label='Upload')  # Plot upload speeds
    ax.plot(download_speeds, label='Download')  # Plot download speeds
    ax.legend()  # Add legend to the plot
    ax.set_title('Real-time Bandwidth Monitor')  # Set title of the plot
    ax.set_xlabel('Time')  # Set x-axis label
    ax.set_ylabel('Speed (KB/s)')  # Set y-axis label

# GUI setup
root = tk.Tk()  
root.title("Real-time Bandwidth Monitor")
root.minsize(600, 400)

# Upload speed label 
upload_speed_label = tk.Label(root, text="Upload: 0 KB/s")
upload_speed_label.pack()

# Download speed label
download_speed_label = tk.Label(root, text="Download: 0 KB/s")
download_speed_label.pack()

# Ping result label
ping_label = tk.Label(root, text="Ping: -- ms")
ping_label.pack()

# Initial call to update the ping label
update_ping_label()

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(6, 4))
upload_speeds, download_speeds = [], []

# Create a canvas to integrate Matplotlib plot with Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Animate the plot with a 1-second interval
ani = FuncAnimation(fig, update_plot, interval=1000)

# Run the Tkinter main loop
root.mainloop()
