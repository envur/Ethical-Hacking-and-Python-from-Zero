# Network Scanner

This is the second software created in the course, it's a very simple network scanner made with basics of the Scapy library.

## Using it

The usage is really easy, just call the script on your terminal like this:
```bash
sudo python3 network_scanner.py -t 192.168.1.1/24
```

**Note that the *-t* flag can also be called by *--target* and it refers to the IP address/range you want to scan** 

---

## The code

First thing to do, it's importing Scapy. If you don't have it installed, run the command below on your terminal:
```bash
pip install scapy
```

Now, in the file, you can import Scapy's functions:
```python
import scapy.all as scapy
```

Let's create the function that will be scanning our network, it will be receiving our IP address/range as an argument:

```python
def scan(ip):
	# Setting our variables:
	target_ips = scapy.ARP(pdst=ip)
	broadcast_MAC = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_broadcast_ips = broadcast_MAC/target_ips
	
	# Scanning the network:
	answered_list = scapy.srp(arp_broadcast_ips, timeout=2, verbose=False)[0]
	
	"""
	Appending the results of the scan to a list of dicts
	in order to format for the user and have
	better code readability:
	"""
	answers_data_list = []
	for answer in answered_list:
		answers_data_list.append({"ip": answer[1].psrc, "mac": answer[1].hwsrc})
		
	return answers_data_list
```

I'll be explaining all the parts of the function on the following sections:

### Setting our variables:

Here we'll be setting three variables.

The first one will receive an instance of the scapy.all.ARP() object containing the destination of our packets that will be defined with the **pdst** attribute. So, basically, this variable will store our ARP request.

```python
target_ips = scapy.ARP(pdst=ip)
```

The second one will receive an instance of a scapy.Ether() object, containing the broadcast MAC address as it's destination, that we will set using the **dst** attribute. 
This is really important, since it will guarantee that our packets are going to be sent to the whole network, not only one device.

```python
broadcast_MAC = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
```

the third one will store our ARP packets, made with the other two variables that we defined above. We can do this by replicating the following:

```python
arp_broadcast_ips = broadcast_MAC/target_ips
```

	To be finished...