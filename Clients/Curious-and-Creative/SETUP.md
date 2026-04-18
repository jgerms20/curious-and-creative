# Quick Setup – Curious & Creative Website

## 🚀 Get Your Site Live in 5 Minutes

### Step 1: Create GitHub Repository
1. Go to **https://github.com/new**
2. Name: `curious-and-creative`
3. Description: "Creative studio website"
4. Make it **Public**
5. Click "Create repository"

### Step 2: Push Code to GitHub

```bash
# From the website folder root:
cd /home/user/curious-and-creative-agency/Clients/Curious-and-Creative/website

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Curious & Creative website"

# Add your GitHub repo as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/curious-and-creative.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. Go to your repo: https://github.com/YOUR_USERNAME/curious-and-creative
2. Click **Settings** (top right)
3. Click **Pages** (left sidebar)
4. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main** / **/(root)**
5. Click **Save**

**Your site will be live at:** `https://YOUR_USERNAME.github.io/curious-and-creative`

### Step 4: Custom Domain (Optional)
1. Go to **Settings > Pages**
2. Add custom domain (e.g., `www.curiousandcreative.com`)
3. Point your domain registrar to GitHub Pages (see GitHub instructions)

---

## 📝 Quick Edits Before Launch

### Update Contact Info
Search for these in all HTML files and replace:
- `hello@curiousandcreative.com` → Your actual email
- `+1-555-0100` → Your phone
- `Brooklyn, New York` → Your location

### Update Team Names
In `pages/team.html`:
- Change "Janel" and "You" to actual names
- Add bios

### Add Images (Optional but Recommended)
Create `assets/images/` folder with:
- `project-1.jpg` through `project-6.jpg` (or more)
- Team photos (optional, currently using gradient placeholders)

---

## ✅ Pre-Launch Checklist

- [ ] GitHub repo created
- [ ] Code pushed to main branch
- [ ] GitHub Pages enabled
- [ ] Site is live (check https://YOUR_USERNAME.github.io/curious-and-creative)
- [ ] Contact info updated
- [ ] Team names updated
- [ ] All links working (test each page)
- [ ] Mobile responsive (check on phone)

---

## 🔧 Make Updates

After launching, updates are simple:

```bash
cd website
# Make your edits to HTML/CSS/JS files
git add .
git commit -m "Update: brief description of changes"
git push
```

Changes go live automatically within seconds.

---

## 🎯 Next Steps

1. **Add Images** – Replace placeholder gradients with real project photography
2. **Add Projects** – Update `pages/projects.html` with real project details
3. **Add Blog** (Optional) – Create a `pages/blog.html` for news/updates
4. **Setup Newsletter** (Optional) – Add email signup (Mailchimp, Substack, etc.)
5. **Add Analytics** (Optional) – Google Analytics tracking code

---

## 📞 Reference Files

- **README.md** – Full project documentation
- **brand-guide/BRAND-GUIDE.md** – Complete branding guidelines
- **PROJECT-SUMMARY.md** – Deliverables overview

Everything is production-ready. Just push and launch!
