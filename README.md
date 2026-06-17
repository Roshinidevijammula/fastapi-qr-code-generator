# Premium QR Code Generator (with AWS S3 & Docker)

A full-stack, responsive QR Code Generator designed with a premium dark-themed glassmorphic user interface. The application generates high-resolution QR codes dynamically, uploads them to secure AWS S3 storage, and returns the cloud hosted URL with action options (copy to clipboard & download).

The project is structured in two architectures:
1. **Monolithic Flask App (`qr-app`)**: Serves both the frontend and the generate APIs on the same port.
2. **Containerized Multi-service App (`generator`)**: Uses Docker Compose to orchestrate a separate Nginx frontend server and a Python Flask backend API.

---

## 🌟 Key Features
- **Cloud Integration**: Direct connection with AWS S3 using `boto3` for storing and serving generated QR codes.
- **Glassmorphic Dark UI**: Premium, high-quality modern styling with HSL gradients, active focus glows, and neon background blobs.
- **Loading & State Indicators**: Smooth transition animations and button disabling to prevent duplicate requests.
- **Action Triggers**: One-click URL copying to the clipboard with visual success verification and download access.
- **Dual-Architecture**: Supports local, lightweight Flask runs or full containerization with Nginx and Docker.

---

## 🛠️ Tech Stack
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphic dashboard system), JavaScript (ES6 Fetch & Clipboard API)
- **Backend**: Python 3.x, Flask, `boto3` (AWS SDK), `qrcode` (Pillow-based QR engine)
- **Containerization & Deployment**: Docker, Docker Compose, Nginx (frontend server)

---

## 📂 Project Structure
```text
VS/
├── qr-app/                     # Monolithic Flask Application
│   ├── templates/
│   │   └── index.html          # Main HTML structure
│   ├── static/
│   │   ├── style.css           # Custom Glassmorphic styles
│   │   └── script.js           # Clipboard & API fetch logic
│   ├── .env                    # S3 & AWS configuration
│   ├── app.py                  # Monolithic Flask server
│   └── requirements.txt        # Python dependencies
│
└── generator/                  # Containerized Architecture
    ├── docker-compose.yml      # Orchestrates frontend & backend containers
    ├── backend/
    │   ├── app.py              # Flask server with CORS enabled
    │   ├── Dockerfile          # Python image setup
    │   ├── .env                # Port 5050 S3 configs
    │   └── requirements.txt    # Backend library requirements
    └── frontend/
        ├── index.html          # Nginx HTML home page
        ├── style.css           # Nginx CSS layout
        └── script.js           # Feeds calls to port 5050 backend
```

---

## ⚙️ Configuration

Create a `.env` file in the root of the app directory you intend to run (`qr-app/` or `generator/backend/`) with your AWS credentials:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=ap-south-1
S3_BUCKET=your_s3_bucket_name
```

---

## 🚀 How to Run the Application

### Option 1: Monolithic Server (Lightweight, Recommended)

1. Open your terminal and navigate to the monolithic directory:
   ```bash
   cd qr-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python3 app.py
   ```
4. Open your browser and navigate to **`http://localhost:5000`**

---

### Option 2: Dockerized Multi-service

1. Open your terminal and navigate to the Docker compose directory:
   ```bash
   cd generator
   ```
2. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Open your browser and navigate to **`http://localhost:8080`**

---

## 🤝 Contributing
Feel free to fork the repository, open pull requests, and contribute to new features!

**Author**: [Roshini Devi](https://github.com/YOUR_USERNAME)
