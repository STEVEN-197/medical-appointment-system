# Streamlit Setup Guide - Medical Appointment Scheduling System

## 🚀 Run Locally with Streamlit

### Step 1: Prerequisites
Make sure you have:
- **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
- **Git** installed ([Download](https://git-scm.com/))
- **Gemini API Key** from [Google AI Studio](https://aistudio.google.com)

### Step 2: Clone the Repository

```bash
git clone https://github.com/STEVEN-197/medical-appointment-system.git
cd medical-appointment-system
```

### Step 3: Create Virtual Environment (Recommended)

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `google-generativeai` - Gemini AI SDK
- `python-dotenv` - Environment variable management

### Step 5: Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**NEVER commit your real `.env` file to GitHub!**

### Step 6: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at: **http://localhost:8501**

---

## 🎮 Using the App

### Test Credentials (Auto-seeded)

A sample doctor is already in the system:
- **Doctor**: Dr. Arjun Rao (Cardiologist)
- **Email**: `arjun@medibook.local`
- **Password**: `doctor123`
- **Available slots**: Today, 10am-4pm (hourly)

### Create Test Patient

1. **Sidebar** → Click "Register"
2. **Select Role**: Patient
3. **Fill Form**:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Password: `test123`
   - Age: `30`
   - Gender: `Male`
   - Preferred Specialty: `Cardiology`
4. **Click**: "Create Account"
5. You're now logged in!

### Browse & Book Appointment

1. **Sidebar** → "Browse Doctors"
2. See Dr. Arjun Rao with experience, location, and consultation mode
3. **Click**: "Book Appointment"
4. **Select Date**: Today
5. **Select Time**: Any available slot (10am-4pm)
6. **Confirm** booking
7. **View** appointment in "My Appointments"

### Try AI Assistant

1. **Sidebar** → "AI Assistant"
2. **Type**: "I need a cardiologist in the morning"
3. **Click**: "Ask MediBook AI"
4. AI recommends the best matching doctor + time slot

---

## 🌐 Deploy to Streamlit Cloud

### Step 1: Create Streamlit Cloud Account

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign up with your GitHub account
3. Grant access to your repositories

### Step 2: Deploy App

1. **Click**: "Create app"
2. **Select Repository**: `STEVEN-197/medical-appointment-system`
3. **Select Branch**: `main`
4. **Main File Path**: `app.py`
5. **Click**: "Deploy"

Streamlit will automatically build & deploy your app. **Wait 2-3 minutes.**

### Step 3: Set API Key Secret

1. Go to your deployed app URL
2. **Click** menu (⋯) → "Settings"
3. **Secrets** section → Click "Manage"
4. **Add Secret**:
   ```
   GEMINI_API_KEY = your_actual_key_here
   ```
5. **Save** and app will restart automatically

Your app is now live! Share the URL with others.

---

## 🐳 Deploy with Docker

### Step 1: Build Docker Image

```bash
docker build -t medibook .
```

### Step 2: Run Container

```bash
docker run \
  -e GEMINI_API_KEY="your_api_key_here" \
  -p 8501:8501 \
  medibook
```

Access at: http://localhost:8501

### Step 3: Deploy to Cloud (AWS/GCP/Heroku)

**Example for Heroku:**

```bash
heroku login
heroku create my-medibook-app
heroku config:set GEMINI_API_KEY="your_api_key_here"
git push heroku main
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**: Install requirements again
```bash
pip install -r requirements.txt
```

### Issue: "GEMINI_API_KEY not set"

**Solution**: Check `.env` file exists and has correct key
```bash
cat .env  # Linux/macOS
type .env # Windows
```

If missing:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### Issue: "Port 8501 already in use"

**Solution**: Use different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: "API key invalid" in Streamlit Cloud

**Solution**: Go to app Settings → Secrets, verify key is correct (no extra spaces)

---

## 📊 Performance Tips

1. **Cache Data**: Streamlit caches function results
   ```python
   @st.cache_data
   def get_doctors():
       return controller.get_doctors()
   ```

2. **Use Session State**: Store data between reruns
   ```python
   if 'current_user' not in st.session_state:
       st.session_state.current_user = None
   ```

3. **Optimize AI Calls**: Gemini API has rate limits
   ```python
   @st.cache_data(ttl=300)  # Cache for 5 minutes
   def get_recommendation():
       return ai_service.recommend_slot(...)
   ```

---

## 📈 Development Workflow

### Hot Reload

Streamlit automatically reloads when you save files:

```bash
streamlit run app.py
# Edit app.py
# Save (Ctrl+S or Cmd+S)
# App refreshes automatically in browser
```

### Debugging

```python
import streamlit as st

# Print to console
print("Debug message")  # Shows in terminal

# Display in Streamlit
st.write("Debug value:", variable_name)
st.write(st.session_state)  # Show all session state
```

---

## 📚 Environment Variables

Create `.env` with:

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
STREAMLIT_CLIENT_LOGGER_LEVEL=warning
PYTHONUNBUFFERED=1
```

---

## 🔐 Security Checklist

- ✅ Never commit `.env` file
- ✅ Use environment variables for secrets
- ✅ Never hardcode API keys
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Set Streamlit secrets in Cloud UI, not in code
- ✅ Use HTTPS in production
- ✅ Validate user input

---

## 📱 Mobile Access

Streamlit Cloud apps are mobile-responsive. Just open the URL on your phone!

For better mobile UX, Streamlit automatically:
- Hides sidebar on small screens
- Stacks columns vertically
- Makes buttons larger

---

## 🚀 Next Steps

1. **Clone** the repo
2. **Setup** environment variables
3. **Run** locally with `streamlit run app.py`
4. **Test** the features
5. **Deploy** to Streamlit Cloud when ready
6. **Share** your live app link!

---

## 📞 Need Help?

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Gemini API Docs**: [ai.google.dev](https://ai.google.dev)
- **GitHub Issues**: Open an issue in the repo
- **Stack Overflow**: Tag `streamlit` + `python`

---

**Happy coding! 🎉**
