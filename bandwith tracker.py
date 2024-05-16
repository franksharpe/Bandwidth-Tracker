import tkinter as tk
import psutil
import time

# Function to get the network speed
def get_net_speed():
    old_stat = psutil.net_io_counters()
    time.sleep(1)
    new_stat = psutil.net_io_counters()
    
    # Convert to KB/s
    bytes_sent = (new_stat.bytes_sent - old_stat.bytes_sent) / 1024
    bytes_recv = (new_stat.bytes_recv - old_stat.bytes_recv) / 1024
    
    return bytes_sent, bytes_recv

# Update the GUI with network speed
def update_gui():
    sent, recv = get_net_speed()
    
    # Upload label config
    upload_speed_label.config(text=f"Upload: {sent:.2f} KB/s")
    
    # Download label config
    download_speed_label.config(text=f"Download: {recv:.2f} KB/s")

    # Update GUI after time
    root.after(1000, update_gui)

# GUI
root = tk.Tk()  
root.title("Bandwidth Monitor")
root.minsize(300, 100)

# Upload label 
upload_speed_label = tk.Label(root, text="Upload: 0 KB/s")
upload_speed_label.pack()

# Download label
download_speed_label = tk.Label(root, text="Download: 0 KB/s")
download_speed_label.pack()

# Run update GUI
update_gui()

# Run the GUI
root.mainloop()
