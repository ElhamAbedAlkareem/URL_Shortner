
# 🔗 URL Shortener

This project is a lightweight, serverless URL shortener built with **AWS Lambda**, **DynamoDB**, and **S3**. It allows users to generate a short URL from any long URL and automatically redirects when the short URL is visited.

---

## 🚀 Features

- 🔗 Shortens long URLs with a random short ID
- 🚦 Redirects users when short URL is accessed
- 🗃️ Stores mappings in Amazon DynamoDB
- ☁️ Hosted serverlessly using AWS Lambda Function URLs
- 🌐 Frontend hosted as a static S3 website
- ✅ CORS-enabled and secure for frontend/backend interaction

---

## 🧰 Technologies Used

| Layer      | Technology           |
|------------|----------------------|
| Frontend   | HTML, CSS, JavaScript |
| Backend    | AWS Lambda (Python) |
| Storage    | Amazon DynamoDB      |
| Hosting    | Amazon S3 Static Website |
| Serverless | Lambda Function URL  |

---

## 📁 Project Structure

```
📦 url-shortener/
├── lambda_function.py     # Python Lambda code
├── index.html             # Frontend UI (hosted on S3)
├── style.css              # Optional CSS styling
├── background.jpg         # Optional background image
├── Deployment Guide       # Manual setup instructions
└── README.md              # You're reading this file
```

---

## 🛠 How It Works

1. **Frontend**:
   - User enters a long URL and clicks "Shorten"
   - JS sends a `POST` request to Lambda Function URL
   - Short URL is returned and displayed
   - When a short URL is visited, Lambda handles redirection

2. **Backend (Lambda)**:
   - `POST /shorten`: Accepts JSON `{ long_url }`, generates a short ID, stores it in DynamoDB, and returns a short URL
   - `GET /{short_id}`: Redirects user to the original long URL

3. **Database (DynamoDB)**:
   - Table: `ShortUrls`
   - Partition Key: `id` (short ID)
   - Attribute: `url` (original URL)

---

## 🧪 Sample Usage

### 🔹 POST Request

**Request:**
```http
POST https://<lambda-function-url>/
Content-Type: application/json

{
  "long_url": "https://www.example.com"
}
```

**Response:**
```json
{
  "short_url": "https://<lambda-function-url>/<short_id>"
}
```

---

### 🔹 GET Request

**Request:**
```http
GET https://<lambda-function-url>/<short_id>
```

**Response:**
```http
HTTP/1.1 302 Found
Location: https://www.example.com
```

---

## 📃 License

MIT License © 2025 Elham Abed Alkareem

---

## 🙋‍♀️ Author

**Elham Abed Alkareem**  
[elham.aa.91@gmail.com](mailto:elham.aa.91@gmail.com)
