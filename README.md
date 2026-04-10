# Code security reviewer 🛡️

AI-powered code security reviewer built with FastAPI - static analysis + LLM feedback. <br>
**🚧 Still Under Construction**

## 🔜 Planned features 
- web app for code security analysis
- AI-powered feedback via custom code-trained LLMs
- Static analysis with Bandit (Python)
- Multi-language support (future)

## 📦 Installation

```bash
git clone https://github.com/nicowu07/code-reviewer.git
cd code-reviewer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set up the database:

```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```

Inside psql:

```sql
CREATE DATABASE code_reviewer;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE code_reviewer TO your_user;
GRANT ALL ON SCHEMA public TO your_user;
\q
```

Create your `.env` file:

```bash
echo "DATABASE_URL=postgresql://your_user:your_password@localhost:5432/code_reviewer" > .env
```


## 🚀 Try it out
```bash
uvicorn main:app --reload
```
Open http://localhost:8000 — you'll see your app running. Paste some code, click the button, it responds.

<img src="images/image.png" alt="webpage" width="700"/>


