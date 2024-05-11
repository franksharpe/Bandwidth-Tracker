#libarys

import tkinter as tk
import psutil
import time


#get the speeds
def get_net_speed():
    
#first speed

    old_stat= psutil.net_io_counters()
    
    #second wait
    time.sleep(1)
    
    #new speed
    new_stat = psutil.net_io_counters()
    
    #conver to KB/s
    
    #upload
    bytes_sent = (new_stat.bytes_sent - old_stat.bytes_sent) / 1024
    
    #download
    bytes_recv = (new_stat.bytes_recv - old_stat.bytes_recv) / 1024
    
    return bytes_sent, bytes_recv

#update the gui
def update_gui():
    sent, recv = get_net_speed()
    
    #upload label config
    upload_speed_label.config(text=f"Upload: {sent:.2f} KB/s")
    
    #download label config
    download_speed_label.config(text=f"Download: {recv:.2f} KB/s")

    #update gui after time
    root.after(1000, update_gui)

#gui
root = tk.Tk()  
root.title("Bandwidth monitor")

#upload label 
upload_speed_label = tk.Label(root, text="Upload: 0 KB/s")
upload_speed_label.pack()

#download label
download_speed_label = tk.Label(root, text="Download: 0 KB/s")
download_speed_label.pack()

#run update gui
update_gui()

#run the gui
root.mainloop()  
