# 🚀 Industrial-Grade AI Chatbot Application

A robust, full-stack conversational AI application engineered during my **Tata Steel Technical Internship**. This system leverages a high-performance Python (Flask) micro-backend, a responsive modern web UI, and seamlessly integrates Meta's LLaMA-3-8B-Instruct model via a secured OpenRouter API pipeline. 

🔗 **Live Production Deployment:** [Interact with the Live Chatbot](https://my-ai-chatbot-64cm.onrender.com)  
📂 **Project Track:** Full-Stack Software Engineering & Applied Artificial Intelligence

---

## 🛠️ Tech Stack & Production Architecture

The system is architected to handle decoupled request-response lifecycles with enterprise-level security paradigms.

### 🔹 Backend Architecture (Server-Side)
* **Core Runtime:** Python 3.11+
* **Framework:** Flask (Micro-framework optimized for lightweight RESTful routing)
* **WSGI HTTP Server:** Gunicorn (Green Unicorn) for concurrent process management in production
* **API Integration:** Asynchronous upstream connection to Meta LLaMA-3 via OpenRouter endpoint layers

### 🔹 Frontend Interface (Client-Side)
* **Structure:** Semantic HTML5 utilizing asynchronous component containers
* **Styling:** Custom CSS3 implementing an optimized Dark Mode UI layout with responsive flex-box grids
* **Interactivity:** Vanilla ECMAScript 6 (JavaScript) utilizing the `Fetch API` with `async/await` handling to prevent browser-blocking operations during API streaming

---

## 🔑 Key Features & Engineering Highlights (Recruiter Focus)

* **Zero-Trust Token Security:** Implemented airtight security metrics by completely decoupling production credentials from source control. API keys are injected dynamically at runtime using server-side Environment Variables (`os.environ`), mitigating data leak vulnerabilities on public repositories.
* **Strict Production Directory Hierarchy:** Adheres strictly to the standard web-framework layout pattern, segregating structural templates from static asset pipelines to optimize browser caching.
* **Non-Blocking Asynchronous UX:** Designed the frontend to asynchronously handle API network delays gracefully, providing a seamless user conversational pipeline without full-page reloads.
* **Cloud Devops Pipeline:** Configured a continuous deployment (CI/CD) matrix connected to GitHub, featuring automated builds, dependency isolation via `requirements.txt`, and active log rotation.

---

## 📁 Repository Directory Structure

```text
AI-CHATBOT/
│
├── static/
│   ├── script.js        # Client-side API request handler & dynamic DOM injector
│   └── style.css        # Enterprise dark-theme responsive UI design variables
│
├── templates/
│   └── index.html       # Primary application viewport & layout structure
│
├── app.py               # Main Flask Application Server & secured OpenRouter API Controller
├── requirements.txt     # Locked production-level dependencies
└── README.md            # Comprehensive project documentation
