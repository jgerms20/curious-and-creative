# Curious & Creative – Website & Brand Identity

**Complete website design and brand identity guide for a culturally-rooted creative studio**

---

## 📁 Project Structure

```
Curious-and-Creative/
├── website/
│   ├── index.html                    # Homepage
│   ├── pages/
│   │   ├── about.html                # About page (mission, vision, story)
│   │   ├── team.html                 # Team profiles & creative network
│   │   ├── projects.html             # Project portfolio with filters
│   │   └── contact.html              # Contact form & inquiry
│   ├── css/
│   │   ├── main.css                  # Primary styles (design tokens, components)
│   │   └── responsive.css            # Mobile-first responsive design
│   ├── js/
│   │   └── main.js                   # JavaScript (menu, forms, filters, animations)
│   └── assets/
│       ├── images/                   # Project imagery
│       ├── icons/                    # Icon assets
│       └── fonts/                    # Custom fonts (if needed)
│
└── brand-guide/
    └── BRAND-GUIDE.md                # Comprehensive brand guidelines
```

---

## 🎨 Design Overview

### Visual Identity
- **Logo:** Stylized ampersand (&) symbol in teal, representing the union of curiosity and creativity
- **Color Palette:** 
  - Primary Dark: #0a0e27 (background)
  - Teal Accent: #00d9ff (primary interactive elements)
  - Magenta: #ff006e (secondary accent)
  - Gold: #ffd60a (tertiary accent)
- **Typography:** 
  - Montserrat (sans-serif, body & navigation)
  - Merriweather (serif, headings & display)
- **Aesthetic:** Modern, minimalist with vibrant pops of color; contemporary yet culturally grounded

### Website Features
✅ **Fully Responsive** – Mobile-first design, adapts seamlessly across all devices  
✅ **Fast & Accessible** – WCAG AA compliant, semantic HTML, keyboard navigation  
✅ **Interactive Elements** – Hover effects, smooth scrolling, animated shapes  
✅ **Contact Management** – Functional contact form with validation  
✅ **Project Filtering** – Filter projects by medium (Film, Audio, Digital, Branded)  
✅ **SEO Ready** – Proper heading hierarchy, meta tags, semantic structure  

---

## 📄 Page Descriptions

### Homepage (`index.html`)
- **Hero Section:** Eye-catching headline with animated accent shapes and dual CTAs
- **Featured Projects:** Grid of 6 latest projects with hover effects
- **About Brief:** Quick introduction with key statistics
- **CTA Section:** Inviting call-to-action to get in touch
- **Footer:** Navigation, contact info, social links

### About Page (`pages/about.html`)
- **Mission Statement:** Bold, inspiring declaration of purpose
- **Vision & Values:** Four core values with supporting descriptions
- **Timeline:** Milestones from 2025 founding to present
- **Operating Model:** Lean studio + global creative network + incubator program
- **Inspiration Section:** References to Proximity Media, Monkeypaw, HOORAE, etc.

### Team Page (`pages/team.html`)
- **Core Team Grid:** 8 team member profiles with photos, titles, and bios
- **Creative Network Section:** Description of 50+ global collaborators by discipline
- **Join Section:** Call-to-action for interested creators
- **Global Network Visualization:** Interactive map showing distributed collaborators

### Projects Page (`pages/projects.html`)
- **Filter System:** Toggle between All, Film, Audio, Digital, Branded projects
- **Portfolio Grid:** 8 example projects with:
  - Project image/placeholder
  - Title and medium
  - Year/status
  - Description
  - Metadata tags
  - Link to full project details
- **Responsive Layout:** Adapts from 3-column desktop to single column mobile

### Contact Page (`pages/contact.html`)
- **Contact Form:** Name, email, subject, inquiry type, message fields with validation
- **Contact Information:** Email, phone, location, social media
- **Contact Cards:** Organized sections for different inquiry types
- **FAQ Section:** Common questions about services, budget, partnerships
- **Success Message:** Friendly confirmation after form submission

---

## 🛠️ Technical Stack

- **HTML5:** Semantic markup
- **CSS3:** Custom properties (CSS variables), flexbox, CSS Grid, animations
- **JavaScript (Vanilla):** No dependencies; includes:
  - Mobile menu toggle
  - Form validation & submission
  - Project filtering
  - Smooth scrolling
  - Lazy loading (framework for future implementation)
  - Intersection Observer for fade-in animations
  - Keyboard accessibility (Escape to close menus)

### Browser Support
- Chrome/Edge 88+
- Firefox 78+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android)

---

## 🚀 Getting Started

### View the Website
1. Open `index.html` in a web browser
2. Navigate between pages using the navigation menu
3. Test responsiveness with browser DevTools (F12)

### Customize Content
All content is in HTML files and can be edited directly:

**Update Project Examples:**
- Open `pages/projects.html`
- Edit project titles, descriptions, mediums
- Update image filenames in `src` attributes

**Update Team Members:**
- Open `pages/team.html`
- Edit team member names, titles, bios
- Modify avatar background colors

**Update Contact Info:**
- Search for "hello@curiousandcreative.com" in all HTML files
- Replace with your actual email
- Update phone number: "+1-555-0100"
- Update address: "Brooklyn, New York"

---

## 📦 Deployment

### Option 1: Static Hosting (Recommended)
- **Netlify:** Drag & drop the `website` folder
- **Vercel:** Connect git repo or upload files
- **GitHub Pages:** Push to `gh-pages` branch
- **Traditional Hosting:** FTP upload to web server

### Option 2: Local Server (Development)
```bash
# Using Python (built-in)
python -m http.server 8000

# Using Node.js (if installed)
npx http-server

# Using Ruby
ruby -run -ehttpd . -p8000
```
Then visit `http://localhost:8000`

### Option 3: Build with SSG (Future)
For scalability, consider moving to:
- **Hugo** (fast, simple)
- **Jekyll** (great for blogs)
- **Next.js/Gatsby** (full-featured React apps)
- **11ty** (lightweight, flexible)

---

## 🎯 Customization Guide

### Colors
Edit the CSS variables in `css/main.css`:
```css
:root {
    --primary-dark: #0a0e27;
    --accent-teal: #00d9ff;
    --accent-magenta: #ff006e;
    --accent-gold: #ffd60a;
}
```

### Typography
Change fonts in HTML `<head>` section:
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;700&display=swap" rel="stylesheet">
```
Then update CSS variable:
```css
--font-primary: 'YourFont', sans-serif;
```

### Hero Images
Replace placeholder with real images:
```html
<!-- In index.html, replace hero-placeholder div with: -->
<img src="assets/images/hero.jpg" alt="Hero image">
```

### Add New Pages
1. Create new HTML file in `pages/` folder
2. Copy structure from existing page
3. Update navigation links in `index.html` and all pages
4. Add route to JavaScript active link function

---

## 📋 Brand Guidelines Reference

**See `brand-guide/BRAND-GUIDE.md` for:**
- Complete brand identity specifications
- Logo usage guidelines
- Typography standards
- Color palette definitions
- Voice & tone guidelines
- Visual style examples
- Design system documentation

---

## ✅ Quality Checklist

- [x] Responsive design (mobile, tablet, desktop)
- [x] Fast load times (no external dependencies)
- [x] Accessibility (WCAG AA, keyboard nav, alt text)
- [x] Cross-browser compatibility
- [x] SEO-friendly structure
- [x] Contact form validation
- [x] Project filtering functionality
- [x] Smooth animations (with prefers-reduced-motion support)
- [x] Consistent branding across all pages
- [x] Mobile hamburger menu
- [x] Footer with links & contact info

---

## 🔄 Updates & Maintenance

### Regular Updates
- **Content:** Update projects, team bios, testimonials quarterly
- **Images:** Replace placeholder images with real photography
- **News:** Add blog section for studio announcements
- **Case Studies:** Create detailed project case study pages

### SEO Optimization
- Add descriptive meta tags to each page
- Create XML sitemap (`sitemap.xml`)
- Add `robots.txt` file
- Optimize image alt text
- Implement schema.org structured data

### Analytics
- Add Google Analytics tracking code
- Monitor visitor behavior and project interest
- Track form submissions and inquiries

### Performance
- Compress and optimize images (use WebP format)
- Minify CSS/JS for production
- Implement caching headers
- Consider CDN for global delivery

---

## 🎯 Future Enhancements

**Phase 2 (In Development):**
- [ ] Project detail pages with full case studies
- [ ] Blog section for articles & insights
- [ ] Team member detail pages
- [ ] Testimonials/client quotes carousel
- [ ] Newsletter signup
- [ ] Video integration (YouTube, Vimeo)

**Phase 3 (Future):**
- [ ] Membership/login system
- [ ] Incubator program application portal
- [ ] Creator portfolio gallery
- [ ] Real-time project updates
- [ ] Live chat/support widget
- [ ] Multi-language support

---

## 📞 Support & Contact

**For brand or design questions:**
- Email: brand@curiousandcreative.com
- Reference: `brand-guide/BRAND-GUIDE.md`

**For website development questions:**
- Check inline code comments
- Review CSS variables and structure
- Test in DevTools

**For project collaborations:**
- Contact: hello@curiousandcreative.com
- Phone: +1 (555) 010-0100

---

## 📄 License & Attribution

- **Fonts:** Montserrat & Merriweather via Google Fonts (Open Source)
- **Design Inspiration:** Proximity Media, Monkeypaw Productions, HOORAE, Sixthirtysix
- **Website Code:** Custom HTML/CSS/JS (Curious & Creative)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | April 2025 | Initial website launch with 5 main pages, full brand guide, and responsive design |

---

**Last Updated:** April 17, 2025

For the most current version and any updates, visit the project repository or contact the team.
