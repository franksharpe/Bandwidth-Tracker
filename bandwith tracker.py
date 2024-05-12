# Libraries
import tkinter as tk
import psutil
import time
import shodan
import ipaddress
import requests

# Shodan API Key
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"

# Initialize Shodan API
api = shodan.Shodan(SHODAN_API_KEY)

# Function to create a Shodan network alert
def create_shodan_alert(network_range):
    try:
        alert = api.create_alert(name="My Production Network", ip_range=network_range)
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

# Function to get the network address and subnet mask
def get_network_info():
    # Get network interface information
    interfaces = psutil.net_if_addrs()
    
    # Find the first non-loopback interface
    for interface in interfaces:
        if interface != 'lo':
            for addr in interfaces[interface]:
                # Print the attributes of addr to see what's available
                print(addr)
                # Check if the family attribute exists and its value
                if hasattr(addr, 'family') and addr.family == getattr(psutil, 'AF_INET', None):
                    return addr.address, addr.netmask
    return None, None

# Test the function
get_network_info()

# Function to calculate IP address range based on network address and subnet mask
def calculate_ip_range(network_address, subnet_mask):
    network = ipaddress.ip_network((network_address, subnet_mask), strict=False)
    return str(network.network_address) + '/' + str(network.prefixlen)

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

# Function to check email for breaches
def check_email_for_breaches(email):
    url = f"https://monitor.firefox.com/api/v1/breaches/{email}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        breaches = response.json()
        if breaches:
            print(f"The email '{email}' has been involved in the following breaches:")
            for breach in breaches:
                print(f"Breach: {breach['breachId']} - {breach['site']}")
        else:
            print(f"The email '{email}' has not been involved in any known breaches.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# GUI
root = tk.Tk()  
root.title("Bandwidth monitor")
root.minsize(300, 300)

# Upload label 
upload_speed_label = tk.Label(root, text="Upload: 0 KB/s")
upload_speed_label.pack()

# Download label
download_speed_label = tk.Label(root, text="Download: 0 KB/s")
download_speed_label.pack()

# Entry for email to check
email_to_check_entry = tk.Entry(root, width=50)  # Adjust the width as needed
email_to_check_entry.pack()


# Button to trigger breach check
breach_check_button = tk.Button(root, text="Check Breaches", command=lambda: check_email_for_breaches(email_to_check_entry.get()))
breach_check_button.pack()

# Run update GUI
update_gui()

# Get network information
network_address, subnet_mask = get_network_info()

# Calculate IP address range
if network_address and subnet_mask:
    network_range = calculate_ip_range(network_address, subnet_mask)
    print("Network Range:", network_range)
    
    # Create Shodan alert
    alert_id = create_shodan_alert(network_range)
    if alert_id:
        # Enable malware trigger for the Shodan alert
        enable_malware_trigger(alert_id)

# Run the GUI
root.mainloop()
