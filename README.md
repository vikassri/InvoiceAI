# 🧾 InvoiceAI

InvoiceAI is a lightweight AI-powered web application that extracts structured data from invoice images using **LLM (NVIDIA API)**, and presents the results in clean JSON format via a **Streamlit interface**.

---

## 🚀 Features

- 📄 Upload invoice images (PNG, JPG, etc.)
- 🔍 Convert images in to base64 
- 🧠 Send the base64 to NVIDIA LLM API
- 🧾 Output clean JSON (invoice number, date, totals, items, etc.)
- 🌐 Simple and interactive UI with Streamlit
- ⚡ Fast and easy to deploy

---

## 🧱 Tech Stack

- **Frontend/UI:** Streamlit  
- **LLM Processing:** NVIDIA API (Gemma / LLaMA / Mistral)  
- **Language:** Python  

---

## 📂 Project Structure

```
invoiceAI/
│── app.py
│── utils.py
│── requirements.txt
│── README.md
/CML
|-- install_dependencies.py
|-- launch_app.py 
```

---

## ⚙️ Installation

### 1. Clone the repository
```
git clone https://github.com/your-username/invoiceAI.git
cd invoiceAI
```

### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

---

## 🔑 Setup NVIDIA API

```
export NVIDIA_API_KEY="your_api_key_here"
```

---

## ▶️ Run the App

```
streamlit run app.py
```

---
## 📄 Example Output
![Invoice Sample](examples/ss1.png)

---

## 💡 Author

Built by Vikas 🚀
