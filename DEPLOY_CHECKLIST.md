# Deployment Checklist

Follow these steps to deploy your crypto pipeline online (takes ~20 minutes).

## ✅ Step 1: Get Credentials (5 min)

### Upstash Kafka
- [ ] Go to https://upstash.com
- [ ] Sign in with GitHub
- [ ] Create Cluster
- [ ] Copy: Bootstrap Servers, Username, Password
- [ ] Create topic: `crypto-trades`

### Neon PostgreSQL
- [ ] Go to https://neon.tech
- [ ] Sign in with GitHub
- [ ] Create Project: `crypto-pipeline`
- [ ] Copy connection string

## ✅ Step 2: Initialize Database (2 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python scripts/setup_database.py
```

## ✅ Step 3: Test Locally (3 min)

```bash
# Terminal 1
python src/producer.py

# Terminal 2
python src/consumer.py

# Terminal 3
streamlit run src/dashboard.py
```

Visit http://localhost:8501 - if you see data, you're good!

## ✅ Step 4: Deploy Producer & Consumer (5 min)

### Option A: Render (Recommended)
- [ ] Go to https://render.com
- [ ] Sign in with GitHub
- [ ] New **Background Worker** (NOT Web Service!) → Connect your repo
- [ ] Service 1: `crypto-producer`
  - Start Command: `python src/producer.py`
  - Add env vars (Kafka credentials)
- [ ] Service 2: `crypto-consumer`
  - Start Command: `python src/consumer.py`
  - Add env vars (Kafka + Database)

### Option B: Railway
- [ ] Go to https://railway.app
- [ ] New Project → Deploy from GitHub
- [ ] Add 2 services with start commands above
- [ ] Add environment variables

## ✅ Step 5: Deploy Dashboard (5 min)

- [ ] Go to https://streamlit.io/cloud
- [ ] Sign in with GitHub
- [ ] New app → Select your repo
- [ ] Main file: `src/dashboard.py`
- [ ] Add secrets in Advanced settings
- [ ] Deploy

## ✅ Step 6: Verify (2 min)

- [ ] Check Render/Railway logs - producer/consumer running
- [ ] Check Upstash dashboard - messages flowing
- [ ] Check Neon dashboard - data being written
- [ ] Visit Streamlit URL - dashboard showing live data

## 🎉 Done!

Your pipeline is now live and running 24/7 for free!

**Your URLs:**
- Dashboard: `https://your-app.streamlit.app`
- Producer: Check Render/Railway dashboard
- Consumer: Check Render/Railway dashboard

## Need Help?

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions and troubleshooting.
