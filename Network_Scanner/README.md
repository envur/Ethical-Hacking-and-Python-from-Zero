# Network Scanner

This is the second software created in the course, it's a very simple network scanner made with the basics of the Scapy library.

## Using it

The usage is really easy, just call the script on your terminal like this:
```bash
sudo python3 network_scanner.py -t 192.168.1.1/24
```

**Note that the *-t* argument can also be called by *--target* and it refers to the IP address/range you want to scan** 

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

The first one will receive an instance of the ```scapy.all.ARP()``` object containing the destination of our packets that will be defined with the **pdst** attribute. So, basically, this variable will store our ARP request.

```python
target_ips = scapy.ARP(pdst=ip)
```

The second one will receive an instance of a ```scapy.all.Ether()``` object, containing the broadcast MAC address as it's destination, that we will set using the **dst** attribute. 
This is really important, since it will guarantee that our packets are going to be sent to the whole network, not only one device.

```python
broadcast_MAC = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
```

the third one will store our ARP packets, made with the other two variables that we defined above. We can do this by replicating the following:

```python
arp_broadcast_ips = broadcast_MAC/target_ips
```

### Scanning the network:

Here, we will call the ```scapy.all.srp()``` function, which scans the network sending the packets whe created.

Note that, alongside with our packets stored in the ***arp_broadcast_ips***, we are passing two other arguments to it, ***timeout*** and ***verbose***.

The former sets, in seconds, the maximum time our script will wait for an answer from a client in the network. If we don't set this, we may be stuck if we don't get a response. Here, we are setting 2 seconds to it.

The latter is a boolean that determines if scapy is going to show us (or the user of the script) all of its info. Here it's set to ```False```, so we will only receive what we actively print.

```python
scapy.srp(arp_broadcast_ips, timeout=2, verbose=False)
```

The thing is, the ```scapy.all.srp()``` function returns an array of two lists to us. The first list contains all of the **answered** requests, while the second one contains all of the **unanswered** requests. So we have two options, to either store the two lists in two different variables:

```python
answered_list, unanswered_list = scapy.srp(arp_broadcast_ips, timeout=2, verbose=False)
```

Or simply discard the unanswered list, specifying that we want only the first item of the list our function returns:

```python
answered_list = scapy.srp(arp_broadcast_ips, timeout=2, verbose=False)[0]
```

### Appending the results of the scan to a list of dicts:

Now, this isn't exactly essential for our code to work, but it's a good thing to do, since using dict's keys makes our code easier to read than using only list's indexes. Also, since we are trying to only print the scanned client's IP Addresses along with their MAC Addresses, creating an array of dicts with only these two infos allows us to format our output to the user more easily.

Firstly, let's create an empty array that will receive our dicts:

```python
answers_data_list = []
```

Now, with a very simple **for loop**, let's iterate through our ***answered_list***, creating a dict with each of its items, with the ip and mac addresses while, at the same time, appending them to the array we just created above.

```python
for answer in answered_list:
	answers_data_list.append({"ip": answer[1].psrc, "mac": answer[1].hwsrc})
```

Now, we can simply return our array of dicts as the result of our ```scan()``` function.

```python
return answers_data_list
```

Great, so we just built a function that uses scapy to make a basic scan on our target network. Now, we must print the results of this scan. Let's create another function for that and pass the results of the ```scan()``` function to it:

```python
def print_results(results):
	print("IP Address\t\t\tMAC Address")
	print("--------------------------------------------------")
	
	for item in results:
		print(f'{item["ip"]}\t\t\t{item["mac"]}')
```

It's a really simple function, I know. The first two prints are just a decoration of our result. You can see the whole thing as a table and they are our columns' names.

Then, we make a **for loop** in order to print each one of our results. Note that we used ```\t```, the representation of a TAB, so the printed results can stay aligned with the first print.

The only thing that's missing now is a way to allow our users to pass the IP address/range they want to scan. We will be using **argparse** to do this.

Argparse is a Python lib that allows us to pass input values to our code in the moment we call it. This is kinda of a standard in scripts, as far as I noticed.

Let's also make this a function:

```python
def get_args():
    parser = argparse.ArgumentParser() # Instance of argparse
	# Adding an argument:
    parser.add_argument("-t", "--target", dest="target", help="Specify the IP range which you want to scan")
    opts = parser.parse_args()
	# Checking if the argument received a value:
    if not opts.target:
        parser.error("Specify the IP range! Use -h for help")
    return opts
```

So, we start with an instance of the ```argparse.ArgumentParser()```  (I called it parser, but you can give it any name, obviously) and then we add an argument.

To add a argument, we must use the ```add_argument()``` function, and pass to it three simple arguments:

The first one is the argument itself. Here we defined that the user must type ***-t*** or ***-target*** to call it.

```python
"-t", "--target"
```

Then, we will set the name of the attribute which will receive the value the user will input, using ***dest***. This way, we can use the value by calling it by this name.

It's not that different than setting a variable.

```python
dest="target"
```

Last but not least, we will explain why this argument exists, or what it represents, by using the ***help*** attribute.

```python
help="Specify the IP range which you want to scan"
```

This is how it should look:

```python
parser.add_argument("-t", "--target", dest="target", help="Specify the IP range which you want to scan")
```

Now, let's parse the argument we created using the ```parse_args()``` function. This will inspect what the user typed, and do the actions we determined for our argument.

Let's make a quick validation to see if we received any input so we can warn the users that they must reference our argument to make the code run:

```python
if not opts.target:
	parser.error("Specify the IP range! Use -h for help")
```

Then, we simply return our parsed arguments as the result of our function:

```python
return opts
```

Of course you could just use ```sys.args[]``` to accomplish the same thing, but it's not always the best option since it depends a lot on the position of the input and by doing this you are relying too much on the user, which isn't the best idea. Also, **argparse** makes a whole help section for us with the -h tag and that's pretty neat.

Now, to finish our code, let's call our functions:

```python
options = get_args() # Receiving the user's input
results = scan(str(options.target)) # Passing the users input to the scan function and getting the results
print_results(results) # Printing the results to the user
```

And that's the ending of the second software made in the course.