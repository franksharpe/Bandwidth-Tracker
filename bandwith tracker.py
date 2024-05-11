#bandwith traceker

#things to add

#units customisation
#graphs
#logging data
#system info
#notifcations
# connect to api such as Have I Been Pwned API , Shodan API











#libraries
import tkinter as tk
import psutil
import time
import shodan

# Shodan API Key
SHODAN_API_KEY = "WTc1A44UYeTSPWKlsUc7capT1KyxnXwg"

# Initialize Shodan API
api = shodan.Shodan(SHODAN_API_KEY)

# Function to create a Shodan network alert
def create_shodan_alert(network_range):
    try:
        alert = api.create_alert(name="My Production Network", filters={'ip': network_range})
        print("Shodan alert created successfully!")
        return alert['id']
    except Exception as e:
        print(f"Error creating Shodan alert: {str(e)}")
        return None

# Function to enable malware trigger for a Shodan alert
def enable_malware_trigger(alert_id):
    try:
        triggers = api.alert_triggers(alert_id)
        for trigger in triggers:
            if trigger['name'] == 'Malware':
                api.enable_alert_trigger(alert_id, trigger['id'])
                print("Malware trigger enabled for the Shodan alert.")
                break
    except Exception as e:
        print(f"Error enabling malware trigger: {str(e)}")

# Get the speeds
def get_net_speed():
    old_stat = psutil.net_io_counters()
    time.sleep(1)
    new_stat = psutil.net_io_counters()
    
    # Convert to KB/s
    bytes_sent = (new_stat.bytes_sent - old_stat.bytes_sent) / 1024
    bytes_recv = (new_stat.bytes_recv - old_stat.bytes_recv) / 1024
    
    return bytes_sent, bytes_recv

# Update the GUI
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
root.title("Bandwidth monitor")

# Upload label 
upload_speed_label = tk.Label(root, text="Upload: 0 KB/s")
upload_speed_label.pack()

# Download label
download_speed_label = tk.Label(root, text="Download: 0 KB/s")
download_speed_label.pack()

# Run update GUI
update_gui()

# Create Shodan alert
alert_id = create_shodan_alert("198.20.0.0/16")
if alert_id:
    # Enable malware trigger for the Shodan alert
    enable_malware_trigger(alert_id)

# Run the GUI
root.mainloop()
