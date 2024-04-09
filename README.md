Blockchain Based Network Security Audit Trail

Introduction

This project implements a Blockchain Based Network Security Audit Trail system. The system intercepts network traffic, logs it securely on a blockchain network (Ganache), and provides a web interface to view and analyze the stored network data.

Prerequisites
Before running the project, ensure you have the following prerequisites:

A system with supported operating systems (Windows/MacOS/Linux)
An internet connection
Administrative privileges for installation of required tools
Basic knowledge of command line interface (CLI) and its commands
Installation
1. Installing Python
Download the Python installer from Python official website
Select the installer according to your operating system
Run the installer and follow the on-screen instructions to complete the installation. Use default settings.
2. Downloading Project from GitHub
Go to the GitHub repository
Download the project as a ZIP file
Extract the downloaded files using an extractor like WinRAR
3. Installing Required Python Packages
Open the command prompt
Navigate to the project directory
Run the following commands to install required Python packages:
Copy code
pip install mitmproxy
pip install web3
pip install flask
pip install werkzeug
4. Install SQLite
Download SQLite from SQLite official website according to your operating system
Extract the downloaded files and add the path to the SQLite folder to your system's PATH environment variable
5. Installing Ganache
Download Ganache from the official website
Select the installer for your operating system and follow the on-screen instructions to install it
Configuration
1. Running Ganache
Launch Ganache and create a new workspace
Set the gas limit to "9900000" in the chain menu
Click on start
2. Change Proxy Settings for Interception
Search for proxy settings in your operating system
Enable manual proxy setup and change it to "127.0.0.1:8888"
Save the settings
Running the Project
1. Running the Interception Part
Navigate to the project folder in the command prompt
Run the command python intercept.py to start intercepting network traffic
2. Creating Database and User
Disable proxy settings
Navigate to the decoding folder in the project directory
Run the command python createdb.py to create a database and table for login
Follow the on-screen instructions to add a new user
3. Running the Web Interface
Exit from the previous application
Run the command python app.py to start the Flask server
Open a web browser and go to http://127.0.0.1:5000
Log in using the credentials you created earlier
Explore the web interface to view and analyze the stored network data
Conclusion
You have successfully installed and configured the Blockchain Based Network Security Audit Trail project. You can now intercept network traffic, securely log it on a blockchain network, and analyze the stored data using the provided web interface.

