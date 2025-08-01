# 🚀 Distributed File Orchestration & Synchronization 📁✨
 
This is a secure, SSL-enabled, Python-based file transfer system that lets you **upload, download, view, and manage files** between distributed clients and a central server—just like your own private cloud! ☁️🔒  
Whether you're sharing images, documents, or any files, our system ensures your data is transferred safely and efficiently.  
Perfect for teams, students, or anyone who wants a simple, robust, and secure file sync solution! 🌍🤝

---

## 🛠️ How to Generate SSL Keys & Certificates

Follow these steps to create your own secure keys and certificates for the server:

1. **Remove any existing key/certificate files**

   ```bash
   rm server.key server.cer server.csr
   ```

2. **Generate a new password-protected private key**

   ```bash
   openssl genrsa -aes256 -out server.key 2048
   ```

   > _When prompted, enter a password of your choice. **Don't forget this password!**_

3. **Generate the Certificate Signing Request (.csr)**

   ```bash
   openssl req -new -key server.key -out server.csr
   ```

   - Enter the password you just set
   - Fill in certificate info (country, state, etc.) or just press Enter for defaults

4. **Create a self-signed certificate**

   ```bash
   openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.cer
   ```

   - Enter the same password again

5. **Add your password to the [`Server/ftpserver.py`](Server/ftpserver.py) file**

   - _Tip: Use environment variables for better security!_

6. **🚫 Never upload your keys or certificates to GitHub!**

---

## 💻 How to Run the Project

1. **Connect both devices to the same network** (e.g., mobile hotspot) 📶
2. **Start the FTP server** on one device:
   ```bash
   python Server/ftpserver.py
   ```
3. **Find the server's IP address** (e.g., using `ipconfig` or `ifconfig`)
4. **Connect from the client** using the server's IP and port **21**
5. **Enter your username and password** when prompted
6. **Enjoy secure file transfers!**
   - Upload, download, view, and manage files with ease! 🚀

---

## ✨ Features

- 🔒 **SSL/TLS Encryption** for all file transfers
- 📤 **Upload** and 📥 **Download** any file type
- 👀 **View** file contents directly from the client
- 🗑️ **Delete** unwanted files
- 📜 **List** all files on the server
- 🖼️ Supports images, text, and more!

