# 🔐 Serverless Biometric Face Logging System

An automated serverless face detection system built using **AWS S3**, **Amazon Rekognition**, **Python**, **GitHub Actions**, and **Boto3**.

Whenever an employee image is processed, the application automatically uploads it to Amazon S3, performs facial analysis using Amazon Rekognition, and stores the results in a structured JSON log.

---

## 📌 Features

- 📷 Automatically detects image files
- ☁️ Uploads images to Amazon S3
- 🤖 Uses Amazon Rekognition for facial detection
- 👤 Detects one or multiple faces in an image
- 📊 Records confidence scores for every detected face
- 📝 Maintains a complete processing history in `result.json`
- ⚡ Automated execution using GitHub Actions
- 🔒 Secure AWS authentication using GitHub Secrets

---

## 🏗️ Architecture

```
Employee Image
       │
       ▼
Python Script
(process_photo.py)
       │
       ▼
Amazon S3 Bucket
       │
       ▼
Amazon Rekognition
       │
       ▼
Face Detection Results
       │
       ▼
result.json
```

---

## 📂 Project Structure

```
serverless-biometrics-logging/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── process_photo.py
├── requirements.txt
├── result.json
│
├── employee_01.jpg
├── person2.jpg
├── image.jpg
├── mulfaces.jpg
│
└── README.md
```

---

## 🛠 Technologies Used

- Python 3
- AWS S3
- Amazon Rekognition
- Boto3
- GitHub Actions
- JSON

---

## ⚙️ How It Works

### Step 1

The script searches the current directory for image files.

Supported formats:

- JPG
- JPEG
- PNG

---

### Step 2

The detected image is automatically uploaded to the configured Amazon S3 bucket.

Example path:

```
employees/image.jpg
```

---

### Step 3

Amazon Rekognition analyzes the uploaded image and detects:

- Number of faces
- Confidence score for each face

---

### Step 4

The application creates a log containing:

- Timestamp
- Image name
- S3 location
- Total faces detected
- Confidence score of every detected face

---

### Step 5

Instead of replacing previous results, the new record is appended to `result.json`, creating a complete processing history.

---

## 📋 Sample Output

```json
{
    "timestamp": "2026-07-08 10:49:22",
    "processed_file": "mulfaces.jpg",
    "s3_storage_uri": "s3://security-employee-vault-nik/employees/mulfaces.jpg",
    "total_faces_detected": 6,
    "faces": [
        {
            "face_index": 1,
            "confidence": 99.99
        }
    ]
}
```

---

## 🔐 Environment Variables

The following environment variables must be configured.

| Variable | Description |
|----------|-------------|
| AWS_REGION | AWS Region |
| S3_BUCKET_NAME | Target S3 Bucket |
| AWS_ACCESS_KEY_ID | AWS Access Key |
| AWS_SECRET_ACCESS_KEY | AWS Secret Key |

---

## 📦 Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/serverless-biometrics-logging.git
```

Move into the project.

```bash
cd serverless-biometrics-logging
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Configure AWS credentials and environment variables.

Run the application.

```bash
python process_photo.py
```

---

## 📈 Example Console Output

```
Detected target image: employee_01.jpg

Uploading image to Amazon S3...

Upload Complete.

Running Amazon Rekognition...

Number of Faces Detected : 1

Confidence : 100%

Analytics successfully written to result.json
```

---

## 🚀 Future Improvements

- Face comparison
- Employee attendance logging
- DynamoDB integration
- Lambda trigger from S3 uploads
- CloudWatch monitoring
- SNS email notifications
- Face indexing using Rekognition Collections
- REST API using API Gateway

---

## 👨‍💻 Author

**Nikhil Fegade**

Computer Engineering Student

AWS | Python | Cloud Computing | Data Engineering | DevOps

---
