import tkinter as tk
import psutil
import time

def get_net_speed():
    old_stat= psutil.net_io_counters()
    time.sleep(1)
    new_stat = psutil.net_io_counters()
    
    bytes_sent = (new_stat.bytes_sent - old_stat.bytes_sent) / 1024
    bytes_recv = (new_stat.bytes_recv - old_stat.bytes_recv) / 1024
    
    return bytes_sent, bytes_recv

def update_gui():
    sent, recv = get_net_speed()
    
    upload_speed_label.config(text=f"Upload: {sent:.2f} KB/s")
    download_speed_label.config(text=f"Download: {recv:.2f} KB/s")
    
    root.after(1000, update_gui)

root = tk.Tk()  
root.title("Bandwidth monitor")

upload_speed_label = tk.Label(root, text="Upload: 0 KB/s")
upload_speed_label.pack()

download_speed_label = tk.Label(root, text="Download: 0 KB/s")
download_speed_label.pack()

update_gui()

root.mainloop()  
