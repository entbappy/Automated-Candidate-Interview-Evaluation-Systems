# Installation Guide

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Environment Setup](#environment-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.12 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for dependencies and database

### External Requirements
- **OpenAI API Key**: Required for LLM functionality
- **Internet Connection**: For API calls to OpenAI

---

## Installation Methods

### Method 1: UV Package Manager (⚡ Fastest - Recommended)

[UV](https://docs.astral.sh/uv/) is a modern, fast Python package manager written in Rust.

#### Step 1: Install UV
```bash
pip install uv
```

#### Step 2: Create Virtual Environment
```bash
uv venv interview_eval_env
```

#### Step 3: Activate Virtual Environment
```bash
# On Windows
interview_eval_env\Scripts\activate

# On macOS/Linux
source interview_eval_env/bin/activate
```

#### Step 4: Install Dependencies
```bash
uv pip install -r requirements.txt
```

**Benefits:**
- ⚡ 10-100x faster than pip
- 🔒 Better dependency resolution
- 🎯 Deterministic installs

---

### Method 2: Conda (Recommended for Beginners)

#### Step 1: Create Environment
```bash
conda create -n interview_eval_env python=3.12 -y
```

#### Step 2: Activate Environment
```bash
conda activate interview_eval_env
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Benefits:**
- 📦 Great for scientific Python
- 🔄 Easy environment management
- 🐍 Conda-forge packages available

---

### Method 3: venv (Built-in Python)

#### Step 1: Create Virtual Environment
```bash
python -m venv interview_eval_env
```

#### Step 2: Activate Environment
```bash
# On Windows
interview_eval_env\Scripts\activate

# On macOS/Linux
source interview_eval_env/bin/activate
```

#### Step 3: Upgrade pip
```bash
pip install --upgrade pip
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

**Benefits:**
- ✅ No external tools needed
- 💻 Works on all platforms
- 🚀 Lightweight

---

## Environment Setup

### 1. Create .env File
Create a `.env` file in the project root directory:

```bash
# Windows
echo. > .env

# macOS/Linux
touch .env
```

### 2. Add Configuration
Add your OpenAI API key to the `.env` file:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Generate API Key
If you don't have an OpenAI API key:
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new secret key
5. Copy and paste it into your `.env` file

**⚠️ Security Warning**: Never commit `.env` to version control!

---

## Verification

### Verify Python Installation
```bash
python --version
# Expected output: Python 3.12.x or higher
```

### Verify Dependencies
```bash
pip list
```

You should see packages like:
- `fastapi`
- `uvicorn`
- `autogen-agentchat`
- `openai`
- `pydantic`

### Test FastAPI Installation
```bash
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
```

### Run Application
```bash
uvicorn app:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Open browser to `http://localhost:8000` - you should see the interview UI.

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Ensure your virtual environment is activated and dependencies are installed.
```bash
# Verify virtual environment
which python  # macOS/Linux
where python  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: `OpenAI API Key not found`

**Solution**: Check your `.env` file.
```bash
# Verify .env exists
ls -la .env  # macOS/Linux
dir .env     # Windows

# Check content (don't share in public!)
cat .env
```

### Issue: `Port 8000 already in use`

**Solution**: Use a different port.
```bash
uvicorn app:app --reload --port 8001
```

### Issue: `Chroma database not found`

**Solution**: Initialize the database.
```bash
python all-utils/main.py
```

### Issue: WebSocket connection fails

**Solution**: Ensure WebSocket endpoint is accessible.
```bash
# Check if server is running on correct port
curl http://localhost:8000
```

### Issue: Slow dependency installation

**Solution**: Use UV instead of pip.
```bash
pip install uv
uv pip install -r requirements.txt
```

---

## Next Steps

After successful installation:
1. Read [Configuration Guide](CONFIGURATION.md)
2. Review [Architecture Guide](ARCHITECTURE.md)
3. Check [API Reference](API_REFERENCE.md)
4. Start the application: `uvicorn app:app --reload`

---

## Getting Help

If you encounter issues:
1. Check this troubleshooting section
2. Review error messages carefully
3. Check [Development Guide](DEVELOPMENT.md)
4. Open an issue on GitHub with:
   - Your Python version
   - Full error message
   - Steps to reproduce

