# Deployment Checklist

## Pre-Deployment Testing

### Browser Testing
- [ ] Test homepage in Chrome
- [ ] Test homepage in Firefox
- [ ] Test homepage in Safari
- [ ] Test homepage in Edge

### Responsive Testing
- [ ] Desktop (1920px width)
- [ ] Tablet (768px width)
- [ ] Mobile (375px width, iPhone size)
- [ ] Large mobile (480px width)

### Navigation Testing
- [ ] Home link works
- [ ] Dagtilbud menu opens/closes
- [ ] Foreninger menu opens/closes
- [ ] Informationer menu opens/closes
- [ ] All submenu links work
- [ ] Mobile hamburger menu works
- [ ] Mobile menu closes after selection

### Content Testing
- [ ] Homepage hero image displays
- [ ] Homepage content is readable
- [ ] Dagpleje page loads
- [ ] Dagpleje image displays
- [ ] LUIF page loads
- [ ] LUIF image displays
- [ ] All links point to correct pages

### Mobile Testing
- [ ] Hamburger menu button visible
- [ ] Hamburger menu functional
- [ ] No horizontal scrolling
- [ ] Text is readable
- [ ] Buttons are touchable
- [ ] Images responsive

### Performance Testing
- [ ] Pages load quickly
- [ ] CSS file loads (6.6 KB)
- [ ] Media files load
- [ ] No console errors (F12)
- [ ] No 404 errors

### Cross-Browser Testing
- [ ] Check different browsers
- [ ] Check different OSs (Windows, Mac, Linux)
- [ ] Check mobile browsers

## Pre-Deployment Checks

### Code Quality
- [ ] `python3 src/build.py` runs without errors
- [ ] No HTML syntax errors
- [ ] No CSS syntax errors
- [ ] All links in JSON reference existing pages
- [ ] No broken image paths

### File Structure
- [ ] All generated files present
- [ ] Directory structure correct
- [ ] No temporary files included
- [ ] Git repository clean

### Content
- [ ] All content accurate
- [ ] No placeholder text left
- [ ] All images are correct
- [ ] No typos in titles or descriptions
- [ ] Meta descriptions present

## Build Process

- [ ] Run final build: `python3 src/build.py`
- [ ] Verify no errors in output
- [ ] Check file sizes are reasonable
- [ ] Spot check generated HTML files

## Deployment Steps

### Option 1: Static Hosting (Netlify, Vercel)
- [ ] Create account on hosting platform
- [ ] Connect Git repository
- [ ] Set build command: `cd src && python3 build.py`
- [ ] Set publish directory: `.` (root)
- [ ] Deploy
- [ ] Test live site

### Option 2: Manual Upload (FTP/SFTP)
- [ ] Connect to server via FTP/SFTP
- [ ] Navigate to web root
- [ ] Upload all HTML files
- [ ] Upload assets folder
- [ ] Upload media folder
- [ ] Verify directory structure
- [ ] Test website

### Option 3: GitHub Pages
- [ ] Push to GitHub
- [ ] Enable GitHub Pages in settings
- [ ] Set source to main branch
- [ ] Wait for build to complete
- [ ] Test at yourdomain.github.io

### Option 4: Docker (Cloud Platforms)
- [ ] Build Docker image
- [ ] Push to container registry
- [ ] Deploy to cloud platform
- [ ] Verify DNS settings
- [ ] Test live site

## Post-Deployment Testing

### Verify All Pages Work
- [ ] Homepage loads
- [ ] All main pages load
- [ ] All subpages load
- [ ] No 404 errors

### Check Links
- [ ] Internal links work
- [ ] External links work
- [ ] Navigation links work
- [ ] Footer links work

### Performance Check
- [ ] Pages load quickly
- [ ] Images display properly
- [ ] CSS applies correctly
- [ ] JavaScript functions (dropdown menus)

### Mobile Check
- [ ] Mobile responsive
- [ ] Touch menus work
- [ ] No horizontal scrolling
- [ ] Text is readable

### SEO Check
- [ ] Page titles present
- [ ] Meta descriptions present
- [ ] Structured data (optional)
- [ ] Sitemap.xml (optional)

## DNS & Domain Setup

- [ ] Domain registered
- [ ] DNS records pointing to server
- [ ] SSL certificate installed (HTTPS)
- [ ] www redirect configured (if needed)
- [ ] Email working (if applicable)

## Monitoring

### Set Up Monitoring
- [ ] Website uptime monitoring
- [ ] Error logging
- [ ] Analytics (Google Analytics optional)
- [ ] Backup system in place

### Regular Maintenance
- [ ] Weekly: Review error logs
- [ ] Monthly: Update content as needed
- [ ] Monthly: Test all links
- [ ] Quarterly: Security review
- [ ] Quarterly: Performance review

## Documentation

- [ ] README.md is up to date
- [ ] QUICKSTART.md reviewed
- [ ] ARCHITECTURE.md reviewed
- [ ] Team trained on update process
- [ ] Backup procedure documented

## Rollback Plan

- [ ] Keep backup of previous version
- [ ] Document rollback procedure
- [ ] Have emergency contact list
- [ ] Test rollback procedure

## Sign-Off

- [ ] All checks completed
- [ ] Client approval obtained
- [ ] Deploy authorized
- [ ] Go live! 🚀

---

## Common Issues & Solutions

### Issue: Images not showing
**Solution:** Check media paths in site-data.json are correct

### Issue: CSS not applying
**Solution:** Verify CSS file path in HTML (../../assets/styles.css for nested pages)

### Issue: Links broken
**Solution:** Run build script to regenerate HTML with correct paths

### Issue: Mobile menu not working
**Solution:** Check JavaScript in generated HTML, verify CSS media queries

### Issue: 404 errors
**Solution:** Check if page exists in site-data.json and build.py generated it

---

**Date Started:** ___________
**Date Completed:** ___________
**Deployed By:** ___________
**Approved By:** ___________

