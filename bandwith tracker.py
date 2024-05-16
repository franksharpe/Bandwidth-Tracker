import tkinter as tk
import psutil
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ping3


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

def update_ping_label():
    ping_result = measure_ping("www.google.com")  
    if ping_result is not None:
        ping_label.config(text=f"Ping: {ping_result:.2f} ms")
    else:
        ping_label.config(text="Failed to ping")
        
    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_ping_label)
    

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




#update the gui
def update_gui():
    # Get the latest values from the graph
    if upload_speeds and download_speeds:
        sent = upload_speeds[-1]
        recv = download_speeds[-1]
    
        print("Latest upload speed:", sent)
        print("Latest download speed:", recv)
    
        #upload label config
        upload_speed_label.config(text=f"Upload: {sent:.2f} KB/s")
    
        #download label config
        download_speed_label.config(text=f"Download: {recv:.2f} KB/s")

    #update gui after time
    root.after(1000, update_gui)


   
   
   
    
# Function to update the plot
def update_plot(frame):
    sent, recv = get_net_speed()
    upload_speeds.append(sent)
    download_speeds.append(recv)
    
    ax.clear()
    ax.plot(upload_speeds, label='Upload')
    ax.plot(download_speeds, label='Download')
    ax.legend()
    ax.set_title('Real-time Bandwidth Monitor')
    ax.set_xlabel('Time')
    ax.set_ylabel('Speed (KB/s)')









# GUI
root = tk.Tk()  
root.title("Real-time Bandwidth Monitor")
root.minsize(600, 400)

# Upload label 
upload_speed_label = tk.Label(root, text="Upload: 0 KB/s")
upload_speed_label.pack()

# Download label
download_speed_label = tk.Label(root, text="Download: 0 KB/s")
download_speed_label.pack()

# Create the label for displaying ping result
ping_label = tk.Label(root, text="Ping: -- ms")
ping_label.pack()

# Button to update the ping label
update_ping_label()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(6, 4))
upload_speeds, download_speeds = [], []

# Create a canvas to integrate Matplotlib plot with Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Animate the plot
ani = FuncAnimation(fig, update_plot, interval=1000)

# Run the GUI
root.mainloop()
