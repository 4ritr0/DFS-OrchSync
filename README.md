# RR-Team-61-distributed-file-orchestration-and-synchronization


## Steps to generate server.key server.cer server.csr 

1. remove any existing files 
    - rm server.key server.cer server.csr

2. Generate a new private key that's already password protected
    - openssl genrsa -aes256 -out server.key 2048
    - When prompted, enter a password of your choice (Don't forget this password)

3. Generate the .csr file with a protected key
    - openssl req -new -key server.key -out server.csr
    - You'll be prompted for:
    - The password you just set
    - Certificate information (country, state, etc.) (Hit enter to enable the default options)

4. Create the self-signed certificate:
    - openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.cer
    - Enter the same password again

5. Add the password in the ftpserver.py file to the password variable (using env varibles is preferred)

6. Dont upload these new key and certificates to github
