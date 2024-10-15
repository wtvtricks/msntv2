### UPDATE:
I'm going to recreate this server because it sucks. DO NOT USE THIS REPO

#### How to use (linux):
You need the following:
python3, flask, dnslib
- First clone this repo: `https://github.com/PocketPii/msntv2.git`
- Second install python3, Flask and dnslib: 
`sudo apt update && sudo apt install python3 python3-dnslib python3-flask`
- If you have a firewall allow ports 6060, 7070, 80, 53 (or the ports you put in config.py)
- Now run `python3 main.py` (if you get a permission error run it with sudo)

#### How to configure the USB:
You need the following:
USB Drive, A computer
- Insert your usb into your computer
- Format the USB to fat32 
- Copy the `copytousb.html` file from the USB folder to your USB Drive

#### Changing the Server URL:
You need the following:
Already configured USB Drive [(From here)](#how-to-configure-the-usb "From here"), A computer

- Run the main.py file from the USB folder
- Turn on your MSN TV 2 box
- Go to Settings > Change Connection Settings > Configure Router
- Get your local IP from your computer
- Input that IP to your MSN TV 2 box
- The script will run and redirect you back

#### How to connect to Server:
You need the following:
A computer with the MSN TV 2 server running

- Run the main.py in the root folder 
-  Go to Settings > Change Connection Settings > Change broadband settings
- Change the Preferred DNS Server local ip
- Set the Alternate DNS Server to 1.0.0.1
- Click save changes and go back to the login screen
- Now click connect

Note: For a server without a local ip you can use the public ip too.


#### How to flash CF card
You need the following:
A computer, CF card reader, Philips head screwdriver  and the CFImage.img file

-  Remove the rubber feet from your MSN TV 2 box
- Unscrew the 4 screws
- Remove the bottom plate
- Unscrew the 5 screws 
- Lift up the metal casing and remove the metal shield
- Remove the CF card 
- Insert CF car into CF Reader
- Use a image for flashing the CFImage.img file to the CF card
- Eject it
- Put it back into the MSN TV 2
- Reassemble the MSN TV 2



