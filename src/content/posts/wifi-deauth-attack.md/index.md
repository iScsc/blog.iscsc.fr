---
title: "Hacking WiFi with De-Authentication Attack"
summary: "In this article, we will demonstrate how to perform a basic wifi attack with `aircrack-ng` by forcing client deauthentication, retrieving the password hash and finally bruteforcing the password."
date: 2024-06-03T20:00:00+0200
lastUpdate: 2024-07-14T13:45:06+0200
tags: ["hacking", "wifi", "network", "bruteforce"]
author: clementS
draft: false
---

## Abstract

**Initial State:** A client is connected to a ***password securised Wifi***

The goal is to get the wifi password.  
To achieve this we must:  
1) Detect target WiFi signal
2) Detect connected computer to this WiFi
3) Send de-authentication packets to this computer to make it disconnect from the WiFi
4) Get the password "hash" when it tries to reconnect to WiFi
5) Bruteforce it :)

## Network Packet Structure

![Network Packet](ip_header.jpg)

On each network packet there are source & destination address.
By default, WiFi Cards only filter packet that have its IP as destination address.

That's a security layer often added in driver, so that is it hard to bypass.
> The first reason is not security; it avoids useless CPU overhead and often, drivers on personal computers are not made to allow monitor mode indeed

So how to bypass it ?

Buy a new WiFi Card with Monitor Mode capability that you can plug to your computer by USB (Monitor Mode is the ability to process all packets, even the ones that are not destinated to your MAC address).

I bought & used AWUS1900.

The WiFi card will be considered as fully configured & driver installed in the following of this tutorial.

Use this GitHub to install the driver for AWUS1900:  
https://github.com/morrownr/8814au/blob/main/README.md

You will also have to install aircrack-ng on your linux.

> sudo apt-get install aircrack-ng

## Step 1: Enable Monitor Mode
By default, your card is in Managed Mode (filter by destination address mode). You have to tell him to get and read every packet.

First get your card interface name:
```
iwconfig
```

![iwconfig](iwconfig.png)

**Interface name is often wlan0 or wlan1**  
Then turn Monitor Mode on.  


```
sudo airmon-ng interface_name
```

![airmon-ngstart](airmon-ngstart.png)

> Note: Interface name can change to `<interface_name>mon`. You can check it with `iwconfig`

## Step 2: Detect WiFi

```
sudo airodump-ng interface_name  
```
![airodump](airodump.png)

This will detect WiFi networks around. Each network is associated with a station address (the router).

Note the BSSID (MAC address of an access point) of the network you wish to access the security of.
Note also the channel used. This represents the physical radio band on which the signals are actually modulated and sent.
> Note That for that concern, it is impossible to detect signals if the base frequency is not handled by your network card (2.4 Ghz only card and 5 GHz signal for instance)

## Step 3: Detect Computer Connectedfor

Then, We just add a filter to filter by source or destination equal access point MAC address
```
sudo airodump-ng -c channel --bssid mac_bssid
```

![airodumpfiltered](airodumpfiltered.png)

Here we can see connected computer(s)

Choose the one you want to hack and note the station MAC address.

## Step 4: Listen Network while Deauth Attack To Victim

We will now perform a deauth attack on the victim's station. The goal is to make the station's WiFi Card disconnect and reconnect to network. This will make the  station send an authentication packet to the access point with the network password "hash" inside. **That's the packet we wanna catch.**

We will do that with 2 commands:  
- listen and write in a file all authentication packet catch threw this network.
```
sudo airodump-ng -c channel --bssid mac_bssid -w outfilename interface_name 
```

![airodumpfiltered2](airodumpfiltered2.png)

- attack victim to make it deauth.  
***We want to deauth victim while listening and writing network auth packet when victim try to reconnect to his network => open a new terminal to perform attack***
```
sudo aireplay-ng -0 1 -a  mac_bssid -c station_mac_address interface_name
```

![airplay](airplay.png)

## Step 5: Checking EAPOL packet received

If deauthentication and reauthentication forced worked, we should have received an EAPOL packet. In listing packet terminal window, there's EAPOL written in packet received.

![airodumpattack](airodumpattack.png)

Deauth worked most of the time but immediate reauthentication doesn't always work. Indeed, Mac OS does not reconnect immediatly to previously reconnected Network after WiFi card unplanned restart. Windows OS doesn't follow the rule and try to reconnect instantly. (Prefer Windows Station to deauth if you have the choice ;))

> very interesting,  source on this part  ?

Then, if it works stop the listening we have what we want by Ctrl+C over listening terminal.

## Step 6: Retreiving WiFi password

A new file was created, you can check it easlily with the `ls` command.

### Time to bruteforce
> To bruteforce we can choose different techniques
Here, we will now perform a dictionnary attack.
Choose your dictionnary, **rockyou.txt** by default.

> source rockyou.txt, what is it ?

```
sudo aircrack-ng -w rockyou.txt outfile.cap
```

![aircrack-ng](aircrack-ng.png)

## Conclusion

The hardest thing to do is to force victim to reconnect. Sometimes, victim OS does not reconnect automatically.  

Use strong passwords to protect your WiFi and WPA3 protocol (hash function harder to calculate => lower hash rate). It makes the bruteforce method less efficient.
