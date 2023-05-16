# Encrypted Signal

Backend Implementation for Secure Programming Project - Encrypted Signal. An Encrypted File Sharing Platform! Users can upload a file, share that file with another registered user. This application follows Secure Programming and covers some of the OWASP Top 10 Web Application Security Risks. A detailed project report can be found here: [Encrypted Signal - Secure Programming Report](https://github.com/TUNI-Projects/Encrypted-Signal-Backend/blob/master/report/Encrypted%20Signal%20-%20Secure%20Programming%20Report.pdf).

## Features

* User Registration, Login, Logout
* User File Upload, Download, Share and Delete

Only owner can share file with other users as well as delete the file.

## OWASP Top 10 Checklist

1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Security Logging and Monitoring Failures
5. Identification and Authentication Failures
6. Security Misconfiguration
7. Server-Side Request Forgery (SSRF)

I am confident that I have managed to cross these checklist on this project. However, they are in extremely primal level. They require a lot of fine tuning, in different layers, not only on application layer.

## Deployment

The Project is visible in a limited capacity on this website (https://tuni-projects.github.io/Encrypted-Signal/).

Limitations are -

* User Session is valid for 1 minute.
* File Upload Limit is 1 KB.

### How to Deploy

After creating and activating the virtual environment,

* Run `pip install -r requirements.txt` to install all required files.
* Run `cp .env.example .env` to create a copy of the `.env` file and use any text-editor to update the newly created `.env` file. You will need to select an appropriate `SECRET_KEY`. If you are unsure, append three UUID together to create a strong key.
* Run `python3 manage.py migrate` to complete all the database migration.
* Run `python3 manage.py runserver` to start the project.

I have written & tested this project on `python3.10` only.

Thank you.

Ibtehaz, 16 May 2023
