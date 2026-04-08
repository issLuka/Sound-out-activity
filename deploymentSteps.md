# Sound-Out-Activity: Complete Web App Deployment Guide

**Last Updated:** April 2026  
**Goal:** Get your Sound-Out app live on the internet (Railway) and prepared for future self-hosting

---

## Table of Contents

1. [Before You Start](#before-you-start)
2. [PHASE 1: Install Docker & Test Locally](#phase-1-install-docker--test-locally)
3. [PHASE 2: Deploy to Railway (Cloud)](#phase-2-deploy-to-railway-cloud)
4. [PHASE 3: Prepare for Self-Hosting (Future)](#phase-3-prepare-for-self-hosting-future)
5. [Free/Cheap Deployment Options](#freecheap-deployment-options)
6. [Cost Tracker](#cost-tracker)
7. [Troubleshooting Reference](#troubleshooting-reference)
8. [Quick Reference: Common Commands](#quick-reference-common-commands)

---

## Before You Start

### What You Need
- A laptop/desktop (Windows, Mac, or Linux)
- GitHub account with your Sound-Out-Activity repo already pushed
- 30 minutes for Phase 1
- 15 minutes for Phase 2
- An internet connection

### What You Don't Need (Yet)
- A credit card (Railway free trial is "$5 credit, no card required")
- A home server/NAS
- Deep technical knowledge (this guide is step-by-step)

### Key Definitions

**Docker**: A tool that packages your app + Python + all dependencies into a portable "box" so it runs the same everywhere (laptop, Railway servers, home server).

**Dockerfile**: A text file with instructions for Docker on how to build that box.

**Container**: The running instance of that box (like starting the app).

**Image**: The saved blueprint before running (like a template).

**Gunicorn**: A professional web server. Flask's built-in server is for development only; Gunicorn handles real traffic.

**Railway**: A cloud hosting platform where your Docker container runs (they manage servers for you).

**IMPORTANT**: Each phase depends on the previous one. Start with Phase 1.

---

# PHASE 1: Install Docker & Test Locally

## Step 1.1: Download & Install Docker

### Mac or Windows
1. Go to https://www.docker.com/products/docker-desktop
2. Download **Docker Desktop**
3. Run installer
4. Follow prompts (use default settings)
5. Restart your computer
6. Open a terminal/command prompt

#### Verify it's installed:
```
docker --version
```

**Expected output:**
```
Docker version 27.0.0, build 1234567
```

If you see a version number, you're good! If not, restart your computer and try again.

---

### Linux (Ubuntu/Debian)
1. Open Terminal
2. Copy-paste this entire block and hit Enter:

```
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
```

3. Log out and back in (or restart terminal)
4. Verify:
```
docker --version
```

**Expected output:** Docker version number

---

## Step 1.2: Create Dockerfile

In your project root (where you see `frontend/`, `pyScripts/`, `png/` folders), create a new file named **`Dockerfile`** (exactly that name, no extension, capital D).

### How to create it:
**VS Code**: `Ctrl+N` → paste content below → `Ctrl+Shift+S` → save as `Dockerfile` in project root

### Content of Dockerfile:

```dockerfile
# Use Python 3.11 slim (smaller image)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK data (needed by e2k/g2p_en)
RUN python -m nltk.downloader punkt averaged_perceptron_tagger -d /usr/local/share/nltk_data

# Copy entire project
COPY . .

# Expose port 5000
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "pyScripts.pyApp:app"]
```

**What each line does:**
- `FROM python:3.11-slim` — Start with Python 3.11 (lightweight version)
- `WORKDIR /app` — Everything inside container happens in `/app`
- `COPY requirements.txt .` — Copy your dependencies list
- `RUN pip install` — Install all Python packages
- `RUN python -m nltk` — Pre-download NLTK data (saves time later)
- `COPY . .` — Copy your entire project into container
- `EXPOSE 5000` — Tell Docker app uses port 5000
- `CMD` — Start command: Gunicorn runs your Flask app

---

## Step 1.3: Create .dockerignore

Create a file named **`.dockerignore`** in your project root (same level as Dockerfile).

### Content:

```
.git
.venv
.vscode
__pycache__
*.pyc
.gitignore
.DS_Store
png/
*.png
.env
node_modules
```

**Why?** This tells Docker to exclude large files so the container stays small and builds fast.

---

## Step 1.4: Check requirements.txt

Open `requirements.txt` and make sure it has `gunicorn`:

```
grep gunicorn requirements.txt
```

**If you see `gunicorn==...`**, you're done with this step.

**If NOT** (nothing printed), add this line to the TOP of `requirements.txt`:

```
gunicorn==23.0.0
```

Open the file, add that line at the beginning, save.

---

## Step 1.5: Build Your Docker Image Locally

Open a terminal/command prompt, navigate to your project root, then run:

```
docker build -t sound-out:1.0 .
```

**What happens:**
- Docker reads your Dockerfile
- Downloads Python 3.11 base image (~200 MB, only happens once)
- Installs all dependencies from requirements.txt (~5-10 minutes first time)
- Creates a "blueprint" (image) named `sound-out` with tag `1.0`

**Expected output (end of build):**
```
...
Successfully built abc123def456
Successfully tagged sound-out:1.0
```

If you see an error, go to [Troubleshooting Reference](#troubleshooting-reference) and search for your error message.

---

## Step 1.6: Run Your Container Locally

Still in terminal, run:

```
docker run -p 5000:5000 sound-out:1.0
```

**What happens:**
- Docker starts your container
- Flask app starts running
- You see logs like:
```
[2025-04-08 12:34:56 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2025-04-08 12:34:56 +0000] [1] [INFO] Using worker: sync
```

---

## Step 1.7: Test Your App in Browser

**Open your browser** and go to:

```
http://localhost:5000
```

You should see your welcome page.

### Test these features:
1. ✅ Click "Generate Worksheet"
2. ✅ Enter a few English words (one per line), e.g.:
   ```
   cat
   dog
   bird
   ```
3. ✅ Click "Generate"
4. ✅ Verify you see Katakana translations
5. ✅ Verify you see 5 levels displayed
6. ✅ Click "Download" and verify a .txt file downloads
7. ✅ Go back to welcome page

**If all work**, proceed to Step 1.8. **If any fail**, skip to [Troubleshooting Reference](#troubleshooting-reference).

---

## Step 1.8: Stop Your Container

Back in terminal, press:

```
Ctrl+C
```

The app stops. You're done with Phase 1! ✅

---

# PHASE 2: Deploy to Railway (Cloud)

## What is Railway?

Railway is a cloud hosting platform. You give them your code (via GitHub), they build and run your Docker container on their servers, and give you a live URL. You can test with users immediately without setting up anything complex.

**Cost for You Right Now:**
- First 30 days: $5 free credit (no card required)
- For 10-50 light users: Likely free or very cheap
- If it grows: Pay as you grow ($5-50+/month depending on usage)

---

## Step 2.1: Create Railway Account

1. Go to https://railway.app
2. Click **"Start For Free"** button
3. Click **"Continue With GitHub"**
4. Authorize Railway to access your GitHub
5. You'll land on the Railway dashboard

**You get $5 in free credits for 30 days** (no credit card required).

---

## Step 2.2: Push Your Code to GitHub

Make sure your Dockerfile and .dockerignore are committed to GitHub:

```
git add Dockerfile
git add .dockerignore
git add requirements.txt
git commit -m "Add Docker setup for cloud deployment"
git push
```

**Verify in GitHub**: Go to your repo on github.com, you should see `Dockerfile` and `.dockerignore` in the file list.

---

## Step 2.3: Deploy via Railway Dashboard

1. Go back to https://railway.app/dashboard
2. Click **"New Project"** (big button, top-right area)
3. Click **"Deploy from GitHub Repo"**
4. Select your **Sound-Out-Activity** repo
5. Click **"Deploy Now"**

**What happens next:**
- Railway builds your Docker image (2-5 minutes)
- Deploys it to Railway servers
- Assigns your app a live URL

---

## Step 2.4: Get Your Live URL

1. In Railway dashboard, click on your project
2. Click **"Deployments"** tab
3. Find the successful deployment (green checkmark)
4. Look for **"Domain"** section—you'll see a URL like:
   ```
   https://sound-out-activity-production-xxxxx.up.railway.app
   ```
5. **Copy that URL** and open it in a browser

**You're live!** 🎉

---

## Step 2.5: Test Your Live App

Open the URL you got and test:
- ✅ Welcome page loads
- ✅ Generate worksheet works
- ✅ Katakana conversion works
- ✅ All 5 levels show
- ✅ Download works

If something doesn't work, see [Troubleshooting: Railway Deployment Issues](#railway-deployment-issues).

---

## Step 2.6: Share Your Live App

Give your Railway URL to friends/colleagues:
```
"Try it here: https://sound-out-activity-production-xxxxx.up.railway.app"
```

They can use it in any browser (Chrome, Firefox, Edge, Safari, Opera).

---

## Step 2.7: Monitor Your App (Optional)

You can check performance anytime:

1. Log into https://railway.app/dashboard
2. Click your project
3. **Logs** tab — see if anything errors
4. **Deployments** tab — see deployment history
5. **Metrics** tab — see memory/CPU usage

For 10-50 users, you'll barely use any resources.

---

## Step 2.8: Set Up Auto-Deploy (Recommended)

Now, whenever you `git push` to GitHub, Railway automatically rebuilds and deploys.

1. In Railway dashboard, click your project
2. Click **"Settings"** tab
3. Enable **"GitHub Auto-Deploy"** (if not already on)

That's it! You're now set up for automatic deployments.

---

# PHASE 3: Prepare for Self-Hosting (Future)

*You don't need to do this now. But read it and bookmark it for when you buy your NAS in 1-1.5 years.*

---

## What Self-Hosting Means

Instead of Railway's servers running your app, YOUR home server runs it. You control everything.

**Advantages:**
- No monthly fees (just electricity)
- Full control over data/privacy
- Educational (learn DevOps/sysadmin skills)

**Disadvantages:**
- You manage server maintenance/updates
- No automatic backups
- Limited by home internet speed
- No redundancy if server goes down

---

## Hardware You'll Need (Future)

When you're ready to buy:
- Linux-capable NAS or Raspberry Pi (~$200-1000 one-time)
- Spare laptop running Linux (works too)
- Home internet with at least 5 Mbps upload speed
- Ethernet connection to router (WiFi okay but slower)

---

## Step 3.1: Install Docker on Your Home Server

Same process as Step 1.1, but on your Linux server (NAS, Raspberry Pi, etc.):

```
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
```

---

## Step 3.2: Get Your App on Home Server

### Option A: Clone from GitHub (Easiest)

SSH into your home server:

```
ssh user@your-server-ip
```

Then:

```
git clone https://github.com/YOUR_USERNAME/Sound-out-activity.git
cd Sound-out-activity
docker build -t sound-out:1.0 .
docker run -p 5000:5000 sound-out:1.0
```

### Option B: Transfer Docker Image

(Advanced—skip if Option A works)

```
# On laptop:
docker save sound-out:1.0 | gzip > sound-out.tar.gz

# Transfer file to home server (e.g., with SCP):
scp sound-out.tar.gz user@home-server-ip:/home/user/

# On home server:
docker load < sound-out.tar.gz
```

---

## Step 3.3: Access From Internet

### 3.3.1: Port Forwarding (Router Setup)

1. Open your router settings (usually 192.168.1.1 or 192.168.0.1)
2. Find **Port Forwarding** section
3. Create rule:
   - **External Port:** 80 (HTTP)
   - **Internal IP:** Your server's local IP (e.g., 192.168.1.50)
   - **Internal Port:** 5000
4. Repeat for Port 443 (HTTPS)

---

### 3.3.2: Get a Domain Name (Optional)

1. Buy domain (namecheap.com, google domains, etc.) — ~$10/year
2. Point DNS records to your home IP (your ISP gives you a static or dynamic IP)
3. **Dynamic DNS** (if your home IP changes):
   - Use service like no-ip.com or duckdns.org (free)
   - Updates your domain when your home IP changes

---

### 3.3.3: Set Up SSL Certificate (HTTPS)

Use Let's Encrypt (free):

```
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com
```

Then configure Nginx as reverse proxy.

---

## Step 3.4: Make App Always-On (Systemd Service)

Create `/etc/systemd/system/sound-out.service`:

```ini
[Unit]
Description=Sound Out Activity Web App
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/Sound-out-activity
ExecStart=/usr/bin/docker run -p 5000:5000 sound-out:1.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```
sudo systemctl daemon-reload
sudo systemctl enable sound-out.service
sudo systemctl start sound-out.service
```

Now app auto-starts on server reboot.

---

## Step 3.5: Monitor Your Home Server

Check app status anytime:

```
sudo systemctl status sound-out.service
sudo journalctl -u sound-out.service -f  # Live logs
docker logs <container-id>  # Docker logs
```

---

# Free/Cheap Deployment Options

You have several options for deploying with minimal/no cost while you're testing with a handful of users:

## Option A: Railway Free Trial ⭐ **RECOMMENDED**
- **Cost**: Free for 30 days ($5 credit, no credit card required)
- **Pros**: Easy setup, auto-deploys from GitHub, good for 10-50 users, then scales to paid if needed
- **Cons**: After 30 days, requires payment ($1 minimum/month + usage)
- **Good for**: Your use case (handful of test users → scaling)

## Option B: Render Free Tier
- **Cost**: Free, with limits (512 MB RAM, spins down after 50 min inactivity)
- **Pros**: Always free, decent for light use
- **Cons**: Slow spin-up times, limited resources
- **Good for**: Casual testing, not for daily use

## Option C: Google Cloud Run
- **Cost**: Free tier with daily quota (~2.5M requests/month)
- **Pros**: Very scalable if needed later
- **Cons**: More complex setup, requires Google account
- **Good for**: Future scaling potential

## Option D: Replit (Simplest)
- **Cost**: Free tier available
- **Pros**: One-click deployment, very beginner-friendly
- **Cons**: Slower than dedicated platforms
- **Good for**: Quick testing

**Recommendation for you**: Use **Railway Free Trial** now for 30 days. Test with real users, then decide if/when to scale.

---

# Cost Tracker

## Phase 1: Local Testing
- **Cost**: $0
- **Time**: Free (you already own laptop)

## Phase 2: Railway Cloud Hosting (Next 1-1.5 years)

| Use Case | Monthly Cost | How Long |
|---|---|---|
| Free trial (first 30 days) | $0 ($5 credit) | 1 month |
| Light use (10-50 users, low traffic) | $5-20/month | Until you're ready to self-host |
| Medium use (50-200 users) | $20-50/month | — |
| Heavy use (500+ users) | $50-100+/month | — |

**Total estimate for 1.5 years on Railway**: $90-900 depending on growth

---

## Phase 3: Self-Hosting (Year+ from now)

| Item | Cost | One-Time? |
|---|---|---|
| NAS or home server | $200-1000 | One-time |
| Domain name | $10/year | Yearly |
| Electricity (extra) | $10-30/month | Monthly |
| SSL certificate (Let's Encrypt) | $0 | Free |
| **Total first year** | **~$260-1180** | — |
| **Total per year after** | **~$130/year** | — |

---

# Troubleshooting Reference

## Docker Installation Issues

### Error: "Docker command not found"
**Solution:**
1. You didn't install Docker yet (Step 1.1)
2. OR you installed but didn't restart computer
3. Restart computer and try again: `docker --version`

---

### Error on Mac: "Apple Silicon/M1 incompatibility"
**Solution:**
Your Mac uses Apple Silicon. Install Docker Desktop for Mac ARM64 (not Intel):
- Go to https://www.docker.com/products/docker-desktop
- Download "Mac with Apple Silicon" version

---

### Error on Linux: "Permission denied while trying to connect to Docker daemon"
**Solution:**
You didn't add your user to docker group. Run:
```
sudo usermod -aG docker $USER
```
Then log out and back in (or restart terminal).

---

## Docker Build Issues

### Error: "requirements.txt not found"
**Solution:**
- Your Dockerfile and requirements.txt must be in SAME directory
- Check you're running `docker build -t sound-out:1.0 .` from your project ROOT
- Project root = where you see `frontend/`, `pyScripts/`, `png/` folders

---

### Error: "No module named 'e2k'"
**Problem:** e2k didn't install during build.

**Solution:**
1. Make sure `requirements.txt` has `e2k==0.6.2`
2. Rebuild without cache:
   ```
   docker build --no-cache -t sound-out:1.0 .
   ```

---

### Error: "ModuleNotFoundError: No module named 'soundOutTranslationScript'"
**Problem:** Python path is wrong.

**Solution:**
Check `pyScripts/pyApp.py` has:
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

If it says `sys.path.insert(0, 'pyScripts')`, change to above.

---

### Build takes 10+ minutes
**This is normal!** First build downloads and installs everything. Subsequent builds are faster due to caching.

---

## Docker Run Issues

### Error: "Address already in use"
**Problem:** Port 5000 is already in use (another app running).

**Solution 1 (Quick):**
```
docker run -p 5001:5000 sound-out:1.0
```
Then access `http://localhost:5001` instead.

**Solution 2 (Proper):**
Find and stop the app using port 5000:
```
# Find what's using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows
```

---

### Error: Container starts then immediately exits
**Check logs:**
```
docker run sound-out:1.0  # Don't use -d flag, see live logs
```

Look for error messages. Common ones:
- `ModuleNotFoundError` → missing dependency in requirements.txt
- `FileNotFoundError` → wrong path to files
- `Connection refused` → port already in use

---

### App starts but page is blank/shows 404
**Check logs:**
```
docker run -it sound-out:1.0  # Run interactively and watch logs
```

Common reasons:
- Flask is looking for files in wrong directory (check static folder path in pyApp.py)
- `frontend/` files not being found → check pyApp.py's `static_folder` setting

Should be something like:
```python
app = Flask(__name__, static_folder=os.path.join(project_root, 'frontend'), static_url_path="/frontend")
```

---

## Railway Deployment Issues

### Build fails on Railway Dashboard
**Check logs:**
1. Click project → **Deployments** tab
2. Click failed deployment
3. Click **Build Logs** — read error messages

**Common fixes:**
- Missing dependency in requirements.txt
- Gunicorn not installed
- Python syntax error in your code
- Path issues (Dockerfile trying to copy non-existent files)

---

### App deployed but shows "500 Internal Server Error"
**Check Railway logs:**
1. Click project → **Logs** tab
2. Look for error messages (red text)

**Common reasons:**
- NLTK data not downloaded (add this to Dockerfile):
  ```dockerfile
  RUN python -m nltk.downloader punkt averaged_perceptron_tagger
  ```
- Flask path issue (database file, static files)
- Environment variable missing

---

### Railway keeps terminating my app (red X)
**Check logs for "Out of Memory"**

**Solution:**
Your app exceeds Railway's memory limit. Options:
1. Upgrade to paid plan (more RAM allocated)
2. Optimize code to use less memory
3. Pre-process large NLTK data outside of runtime

---

### I modified code but Railway is showing old version
**Solution:**
Railway pulls from GitHub. Make sure you:
1. Committed changes: `git add .` then `git commit -m "message"`
2. Pushed to GitHub: `git push`
3. Wait 2-5 minutes for Railway to auto-deploy

**Force redeploy in Railway:**
1. Click project
2. Click **Deployments** tab
3. Click **Redeploy** button on most recent deployment

---

### Custom domain not working on Railway
**Setup:**
1. Railway project → **Settings** tab
2. Find **Custom Domain** section
3. Enter your domain (e.g., `soundout.yourdomain.com`)
4. Railway gives you a **CNAME record**
5. Go to your domain's DNS provider (namecheap, godaddy, etc.)
6. Add CNAME record Railway provides
7. Wait 5-30 minutes for DNS to propagate

---

## Local Testing Issues

### App works locally but features don't work
**Checklist:**
1. Check browser console for JavaScript errors (F12 → Console tab)
2. Check Flask logs in terminal for Python errors
3. Make sure all frontend files are included in project (check `frontend/` folder)

---

### Download doesn't work
**Problem:** File permission or Flask path issue.

**Check:**
1. Flask is trying to save/download to correct directory
2. Directory is writable (`chmod 755 directory_name`)
3. File is being created successfully (check logs)

---

## General "Nothing Works" Checklist

If you're stuck:

1. **Restart everything:**
   ```
   Ctrl+C  # Stop Docker container
   docker kill $(docker ps -q)  # Kill all containers
   docker build --no-cache -t sound-out:1.0 .  # Fresh build
   docker run -p 5000:5000 sound-out:1.0  # Start fresh
   ```

2. **Check your code didn't break:**
   - Did you modify `pyScripts/pyApp.py` recently?
   - Test locally first before pushing to GitHub

3. **Check dependencies are correct:**
   - Flask
   - e2k
   - g2p_en
   - gunicorn
   - nltk

4. **Ask yourself:**
   - Did I follow EVERY step in order?
   - Did I commit+push to GitHub after changes?
   - Did I wait long enough for Railway to deploy?

---

## Getting Help

If you're truly stuck:

1. **Read error message carefully** — it usually tells you what's wrong
2. **Google the error** — likely someone had same issue
3. **Check Docker logs:**
   ```
   docker logs <container_id>
   ```
4. **Check Railway logs** — different from Docker (see above)
5. **Post on Stack Overflow** — include error message + exact steps you followed

---

# Quick Reference: Common Commands

## Docker Commands You'll Use
```
# Build (first time or after big changes)
docker build -t sound-out:1.0 .

# Run locally
docker run -p 5000:5000 sound-out:1.0

# Stop container
Ctrl+C  # In terminal where it's running

# See running containers
docker ps

# See all containers (running + stopped)
docker ps -a

# View logs of stopped container
docker logs <container_id>

# Kill all containers
docker kill $(docker ps -q)

# Delete image (after you're done testing)
docker rmi sound-out:1.0
```

## Git Commands You'll Use
```
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest from GitHub
git pull
```

---

# Checklist: You're Done When...

## Phase 1 Complete ✅
- [ ] Docker installed (`docker --version` works)
- [ ] Dockerfile created in project root
- [ ] .dockerignore created
- [ ] gunicorn added to requirements.txt
- [ ] `docker build` succeeds
- [ ] `docker run` starts without errors
- [ ] Browser shows your app at `http://localhost:5000`
- [ ] All features tested (generate, download, etc.)

## Phase 2 Complete ✅
- [ ] Railway account created
- [ ] Code pushed to GitHub (Dockerfile + .dockerignore visible)
- [ ] Railway deployment successful (green checkmark)
- [ ] Live URL working
- [ ] All features tested in browser
- [ ] URL shared with 2-3 test users

## Phase 3 (Future) Ready ✅
- [ ] You've read Phase 3
- [ ] You've bookmarked this file for when you buy NAS
- [ ] You know you'll follow same steps but on home server

---

# Final Thoughts

You can do this! Here's what makes it achievable:

1. **You already have code working** (the Python script + Flask app)
2. **Docker just packages it** (no code changes needed)
3. **Railway just runs it** (no complicated setup)
4. **This guide covers everything** (just follow steps in order)

Each phase is independent—you can pause between them. No rush.

**When your app is live and working, you'll have:**
- ✅ A live URL you can share (no more local hosting)
- ✅ A Docker container you can migrate to self-hosting later
- ✅ A portfolio project (great for showing DevOps/deployment knowledge)
- ✅ A scalable foundation (if it grows bigger)

---

**Now go create your Dockerfile and test locally. You've got this! 🚀**
