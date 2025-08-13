# 🔍 Log File Error Analyzer

The **Log File Error Analyzer** is a backend application that allows users to upload `.log` or `.txt` files, extract error messages, and analyze them using the **Google Gemini API** (free tier).

* Built with **Flask** (backend), **HTML/JavaScript** (frontend)
* Extracts lines with `"ERROR"` from log files
* Sends them to **Gemini (gemini-1.5-flash)** for analysis
* Returns a structured JSON response with descriptions and resolution steps
* Supports CORS and has comprehensive logging

---

## 📁 Project Structure

```
log-error-analyzer/
├── app.py                  # Flask backend with /upload and /process_errors APIs
├── logger.py               # Logging configuration
├── uploads/                # Directory for uploaded log files
└── logs/                   # Directory for application logs (app.log)
```

---

## ⚙️ Technique

### Step 1: File Upload and Error Extraction

* User uploads a `.log` or `.txt` file
* Backend (`/upload`) saves and reads the file
* Extracts lines containing `"ERROR"`
* Returns them as a JSON array

### Step 2: Error Analysis (Gemini API)

* Frontend sends extracted errors to `/process_errors`
* Each error is sent to **Gemini API**
* Returns:

  * `error`: The raw error message
  * `description`: Why it occurred
  * `resolve_technique`: How to fix it

---

## 🌟 Features

* ✅ **Gemini API Integration** (free tier `gemini-1.5-flash`)
* 📄 **Logs** saved to `logs/app.log`
* 🔐 **CORS** configured for `http://127.0.0.1:5500`

---

## 🚫 Limitations

* Gemini Free Tier: **Rate limits** apply (processed individually to avoid 429 errors)
---

## 🛠️ Setup Instructions

### ✅ Prerequisites

* Python 3.8+
* pip install -r requirements.txt
* Google Cloud account + Gemini API key

---

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Vaibhav-crux/log-error-analyzer.git
cd log-error-analyzer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install flask flask-cors google-generativeai
```

---

### 🔑 Configure Gemini API Key

1. Open `app.py`
2. Replace this line:

```python
GEMINI_API_KEY = 'your-gemini-api-key-here'
```

3. Generate a key via Google Cloud Console:

   * Navigate to: **APIs & Services > Credentials**
   * Create an API key
   * Enable **Gemini API**

---

### 📁 Create Required Directories

```bash
mkdir uploads logs
```

---

### 🧪 Prepare Test File

Create `uploads/application.txt` with the following content:

```
[2025-08-13 08:19:05] ERROR    File upload failed: File type not supported
[2025-08-13 08:19:31] ERROR    Login failed for user 'charlie': Invalid credentials
[2025-08-13 08:22:11] ERROR    API error: Timeout while contacting external service
[2025-08-13 08:24:20] ERROR    Failed to send notification email: SMTP server unreachable
```

---

### 🚀 Running the Application

#### Start Flask Backend

```bash
python app.py
```

* Runs on: `http://127.0.0.1:5000`
* Logs saved in `logs/app.log`

---

## 📡 API Reference

### 📁 `/upload`

* **Method:** `POST`
* **Content-Type:** `multipart/form-data`
* **Description:** Uploads a `.log` or `.txt` file and extracts `"ERROR"` lines

#### Request Body:

| Field     | Type | Description           |
| --------- | ---- | --------------------- |
| `logfile` | File | `.log` or `.txt` file |

#### Example Request (Insomnia)

* Method: `POST`
* URL: `http://127.0.0.1:5000/upload`
* Body: `multipart/form-data`

  * Field: `logfile` = `uploads/application.txt`

#### Example Response:

```json
{
  "message": "Errors extracted, ready for processing",
  "errors": [
    "File upload failed: File type not supported",
    "Login failed for user 'charlie': Invalid credentials",
    "API error: Timeout while contacting external service",
    "Failed to send notification email: SMTP server unreachable"
  ]
}
```

---

### 🔍 `/process_errors`

* **Method:** `POST`
* **Content-Type:** `application/json`
* **Description:** Sends error messages to Gemini API and returns analysis

#### Request Body:

```json
{
  "errors": [
    "File upload failed: File type not supported",
    "Login failed for user 'charlie': Invalid credentials",
    "API error: Timeout while contacting external service",
    "Failed to send notification email: SMTP server unreachable"
  ]
}
```

#### Example Response:

```json
{
  "message": "Error analysis complete",
  "errors": [
    {
      "error": "File upload failed: File type not supported",
      "description": "The file type uploaded by user 'bob' is not allowed by the system.",
      "resolve_technique": "Ensure the file type is supported (e.g., .txt, .log) and retry the upload."
    },
    {
      "error": "Login failed for user 'charlie': Invalid credentials",
      "description": "User 'charlie' provided incorrect username or password.",
      "resolve_technique": "Verify the credentials and try logging in again or reset the password."
    },
    {
      "error": "API error: Timeout while contacting external service",
      "description": "The request to an external service timed out.",
      "resolve_technique": "Check the external service status and retry the request."
    },
    {
      "error": "Failed to send notification email: SMTP server unreachable",
      "description": "The SMTP server could not be contacted to send an email.",
      "resolve_technique": "Check the SMTP server configuration and ensure the server is reachable."
    }
  ]
}
```

---

## 🧪 Testing with Insomnia/Postman

1. **Upload File**

   * POST `http://127.0.0.1:5000/upload`
   * Body: `multipart/form-data`
   * Field: `logfile` → Select test file

2. **Process Errors**

   * POST `http://127.0.0.1:5000/process_errors`
   * Body: JSON
   * Paste `errors` array from `/upload` response

---

## 🐛 Debugging

### Gemini API Errors

Check `logs/app.log` for:

```
[ERROR] Failed to configure Gemini API: ...
[ERROR] Gemini API error: [401] Unauthorized...
[ERROR] Gemini API error: [429] Too Many Requests...
```

### Solution

* Verify your **API key**
* Respect Gemini rate limits

---
