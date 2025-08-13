# Log Error Analyzer

**Log Error Analyzer** is a Flask-based web application that allows users to upload `.log` or `.txt` files, extract error messages, and analyze them using the **Google Gemini API** (free tier). The backend processes files, extracts errors, and sends them to Gemini for analysis, returning JSON responses with detailed error insights. The frontend displays errors in styled cards with a loading spinner for improved UX.

---

## 📁 Project Structure

```

log-error-analyzer/
├── .env                    # Environment variables (e.g., GEMINI\_API\_KEY)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── app/                    # Main application code
│   ├── main.py             # Flask application entry point
│   ├── core/               # Core configuration and utilities
│   │   ├── auth.py         # Authentication logic (placeholder)
│   │   ├── config.py       # Configuration settings
│   ├── middleware/         # Middleware
│   │   ├── cors.py         # CORS middleware
│   │   ├── error\_handler.py# Error handling middleware
│   │   ├── gzip.py         # GZIP compression middleware
│   │   ├── logging.py      # Request logging middleware
│   │   ├── rate\_limiter.py # Rate limiting middleware
│   ├── routes/             # Route definitions
│   │   ├── log.py          # Log file upload and error processing endpoints
│   ├── schemas/            # Schemas for request/response validation
│   │   ├── log.py          # Schemas for log upload and error processing
│   ├── services/           # Business logic
│   │   ├── gemini.py       # Gemini API integration
│   │   ├── log\_processor.py# Log file processing logic
│   ├── utils/              # Utility functions
│   │   ├── logger.py       # Logging setup
├── frontend/               # Frontend assets
│   ├── index.html          # Frontend UI
├── uploads/                # Directory for uploaded files
└── logs/                   # Directory for application logs

````

---

## 🧠 Technique

### 🔹 File Upload and Error Extraction

- Endpoint: `/api/upload` (POST, `multipart/form-data`)
- Backend saves the uploaded file
- Extracts lines containing `"ERROR"`
- Returns a JSON array of extracted errors

### 🔹 Error Analysis with Gemini API

- Endpoint: `/api/process_errors` (POST, `application/json`)
- Each error is sent to Gemini (model: `gemini-1.5-flash`)
- Gemini returns structured JSON:
  - `error`
  - `description`
  - `resolve_technique`

### 🔹 Frontend Display

- Displays each analyzed error in a styled card
- Includes a loading spinner during API calls

---

## ✨ Features

- **Gemini API Integration**: Uses free-tier Gemini for analyzing log errors
- **Middleware Stack**: CORS, GZIP, error handling, rate limiting, logging
- **Validation**: Input/output schema validation
- **Logging**: Logs stored in `logs/app.log` for debugging and tracing

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- [Insomnia](https://insomnia.rest/) (for API testing)
- VS Code with Live Server
- Google Cloud account with Gemini API key

---

### 📦 Installation

```bash
# Clone the Repository
git clone https://github.com/Vaibhav-crux/log-error-analyzer.git
cd log-error-analyzer

# Set up Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
# Then update GEMINI_API_KEY inside the .env file
````

* Get your API key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

### 📁 Create Directories

```bash
mkdir uploads logs
```

### 🧪 Prepare a Test File

Create a test log file at `uploads/application.txt`:

```
[2025-08-13 08:19:05] ERROR    File upload failed: File type not supported
[2025-08-13 08:19:31] ERROR    Login failed for user 'charlie': Invalid credentials
[2025-08-13 08:22:11] ERROR    API error: Timeout while contacting external service
[2025-08-13 08:24:20] ERROR    Failed to send notification email: SMTP server unreachable
```

---

## 🚀 Running the Application

### ▶️ Start Flask Backend

```bash
python app/main.py
```

> Runs on: `http://127.0.0.1:5000`

### 🌐 Start Frontend

1. Open `frontend/index.html` in VS Code
2. Right-click → "Open with Live Server"

> Opens on: `http://127.0.0.1:5500`

---

## ✅ Test the Application

1. Go to `http://127.0.0.1:5500`
2. Upload the sample `application.txt`
3. Wait for spinner and verify four error cards show up

---

## 🧪 API Endpoints

### 1. `/api/upload`

* **Method**: `POST`
* **Content-Type**: `multipart/form-data`
* **Description**: Uploads a `.log` or `.txt` file, extracts `"ERROR"` lines

**Request Body**:

| Field   | Type | Description          |
| ------- | ---- | -------------------- |
| logfile | File | Log file (.log/.txt) |

**Example Response**:

```json
{
  "message": "Errors extracted, ready for processing",
  "errors": [
    "error1",
    "error2",
    ...
  ]
}
```

---

### 2. `/api/process_errors`

* **Method**: `POST`
* **Content-Type**: `application/json`
* **Description**: Sends extracted errors to Gemini API for analysis

**Request Body**:

```json
{
  "errors": ["error1", "error2", ...]
}
```

**Example Response**:

```json
{
  "message": "Error analysis complete",
  "errors": [
    {
      "error": "error1",
      "description": "Why it happened",
      "resolve_technique": "How to fix"
    },
    ...
  ]
}
```

---

## 🧪 Testing with Insomnia/Postman

1. **Install**: [Insomnia](https://insomnia.rest)

2. **Test Upload Endpoint**:

   * **Method**: POST
   * **URL**: `http://127.0.0.1:5000/api/upload`
   * **Body**: `multipart/form-data`

     * `logfile`: `uploads/application.txt`

3. **Test Process Errors**:

   * **Method**: POST
   * **URL**: `http://127.0.0.1:5000/api/process_errors`
   * **Body**: Raw JSON with errors returned from previous step

4. **Verify**:

   * HTTP 200 OK
   * Valid JSON response

---

## 🐞 Debugging

* **Logs**: Check `logs/app.log` for backend issues (including Gemini API failures)
* **Frontend**: Use browser dev tools (F12) to inspect network requests and console errors
* **Gemini API**:

  * Ensure API key is valid
  * Watch for HTTP `401` (unauthorized) or `429` (rate limit)
