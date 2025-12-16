# 🚀 crm-marketing-automation-platform - Simplified Lead Management for Everyone

[![Download](https://img.shields.io/badge/Download-v1.0-blue)](https://github.com/Shayne1214/crm-marketing-automation-platform/releases)

## 🌟 Introduction

Welcome to the crm-marketing-automation-platform! This application serves as a Django REST API server for the Email Leads Manager. It helps users manage leads efficiently, with robust features designed for ease of use. You don’t need to be a tech expert to navigate this platform; our guide will walk you through the process of downloading and running the software.

## 🚀 Getting Started

Follow the steps below to get started with the crm-marketing-automation-platform.

### 1. 📦 Download the Application

To download the latest version, visit the [Releases page](https://github.com/Shayne1214/crm-marketing-automation-platform/releases). You will find all available versions and can choose the one that suits your needs.

### 2. 🛠️ Installation Requirements

Make sure your system meets the following requirements:

- **Operating System:** Windows, Linux, or MacOS.
- **Python Version:** Python 3.6 or above.
- **PIP Package Manager:** Ensure it is installed with Python.

### 3. ⚙️ Setting Up Your Environment

The first steps involve setting up your environment for the application to run smoothly.

1. **Create a Virtual Environment**:
   Open your command-line interface and run:
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   Depending on your operating system, activate the virtual environment with the following commands:
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Required Dependencies**:
   Next, install the required packages. In your command line, run:
   ```bash
   pip install -r requirements.txt
   ```

### 4. 🔐 Configuration

Now, you’ll want to set up some configuration options for better security and functionality.

1. **Create a `.env` File** (optional):
   Create a file named `.env` in the main directory. Add the following variables:
   ```plaintext
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   JWT_SECRET=your-jwt-secret-key-here
   FRONTEND_URL=http://localhost:3000
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_NAME=email-leads-manager
   ```

### 5. 🔄 Run Migrations

To set up your database, run the necessary migrations. This ensures all database tables are created. Execute the following command:
```bash
python manage.py migrate
```

### 6. 👤 Optional Superuser Creation

If you want to manage the application through an admin interface, create a superuser. This allows you to have full access to all features. Run:
```bash
python manage.py createsuperuser
```
Follow the instructions to set your username and password.

### 7. 🚀 Start the Server

To launch the application, use this command:
```bash
python manage.py runserver
```
Once the server is running, you can access the application in your web browser at: `http://127.0.0.1:8000`.

## 💡 Features

The crm-marketing-automation-platform offers various features to enhance your experience:

- **User Authentication**: Secure your application with JWT tokens.
- **Lead Management**: Upload leads easily using CSV files.
- **Account Management**: Manage user accounts efficiently.
- **Email Management**: Streamline your email communication.
- **Template Management**: Create and manage message and subject templates.
- **RESTful API**: Use our API endpoints for various integrations.
- **CORS Support**: Enjoy compatibility across different platforms.

## 🛠️ Troubleshooting

If you encounter issues, consider these common problems:

1. **Python Not Installed**: Ensure Python 3.6 or higher is installed on your system.
2. **Failed Dependency Installation**: Check your internet connection and run the install command again.
3. **Port Conflict**: If the server does not start, check if port 8000 is already in use.

## 🎉 Conclusion

You have now set up the crm-marketing-automation-platform successfully. If you need additional support, the community is here to help. Explore the application and unlock its capabilities for better lead management today!

[Download the latest release here](https://github.com/Shayne1214/crm-marketing-automation-platform/releases) to start managing your leads effectively.