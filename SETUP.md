# Setup Guide - Mental Health Companion App

## Table of Contents
1. [Quick Start](#quick-start)
2. [Detailed Setup Instructions](#detailed-setup-instructions)
3. [Troubleshooting](#troubleshooting)
4. [Advanced Configuration](#advanced-configuration)

---

## Quick Start

### Method 1: Direct Browser Opening (Simplest)
1. Download all files to a folder on your computer
2. Double-click `complete-app.html`
3. The app should open in your default browser
4. Start using immediately!

**Note:** If icons don't load or features don't work, try Method 2.

---

## Detailed Setup Instructions

### Method 2: Using a Local Web Server (Recommended)

Local servers provide better reliability and avoid browser security restrictions.

#### Option A: Python (Built into most systems)

**For Python 3 (most common):**
```bash
# Navigate to the app folder
cd /path/to/mental-health-app

# Start the server
python -m http.server 8000

# Open your browser and go to:
# http://localhost:8000/complete-app.html
```

**For Python 2 (older systems):**
```bash
python -m SimpleHTTPServer 8000
```

#### Option B: Node.js HTTP Server

**First-time setup:**
```bash
# Install http-server globally (one time only)
npm install -g http-server
```

**Running the server:**
```bash
# Navigate to the app folder
cd /path/to/mental-health-app

# Start the server
http-server

# Open your browser and go to:
# http://localhost:8080/complete-app.html
```

#### Option C: VS Code Live Server (For Developers)

1. Install Visual Studio Code
2. Install the "Live Server" extension
3. Open the app folder in VS Code
4. Right-click on `complete-app.html`
5. Select "Open with Live Server"
6. The app opens automatically in your browser

#### Option D: PHP (If you have PHP installed)

```bash
# Navigate to the app folder
cd /path/to/mental-health-app

# Start PHP server
php -S localhost:8000

# Open: http://localhost:8000/complete-app.html
```

---

## File Structure Explanation

```
mental-health-app/
│
├── complete-app.html          # Main file - open this in browser
│   └── Contains: All HTML structure
│
├── mental-health-app.jsx      # React component source
│   └── Contains: All app logic and features
│
├── package.json               # Project configuration
│   └── Contains: Dependencies and scripts
│
├── README.md                  # Main documentation
│   └── Contains: Feature list and overview
│
└── SETUP.md                   # This file
    └── Contains: Detailed setup instructions
```

---

## Troubleshooting

### Problem: Icons Not Showing

**Solution 1:** Check Internet Connection
- The app loads icons from CDN (requires internet)
- Verify you're connected to the internet

**Solution 2:** Clear Browser Cache
```
Chrome: Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac)
Firefox: Ctrl+Shift+Delete
Safari: Cmd+Option+E
```

**Solution 3:** Try a Different Browser
- Chrome (recommended)
- Firefox
- Edge
- Safari

### Problem: App Shows Blank Page

**Solution 1:** Check JavaScript is Enabled
1. Open browser settings
2. Search for "JavaScript"
3. Ensure it's enabled

**Solution 2:** Check Browser Console
1. Press F12 (or right-click → Inspect)
2. Go to "Console" tab
3. Look for error messages
4. Share errors if seeking help

**Solution 3:** Use Local Server
- Direct file opening may have security restrictions
- Use one of the server methods above

### Problem: Features Not Working

**Solution:** Try these in order:
1. Refresh the page (Ctrl+R or Cmd+R)
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Close and reopen the browser
4. Clear cache and cookies
5. Try incognito/private mode
6. Use a local server instead

### Problem: Data Disappears

**This is expected behavior!**
- Data is stored in memory only
- Refreshing or closing the page clears data
- See "Data Persistence" section below for solutions

---

## Advanced Configuration

### Adding Data Persistence (LocalStorage)

To save data between sessions, you can modify the code:

1. Open `mental-health-app.jsx`
2. Add this code near the top of the component:

```javascript
// Load data on component mount
useEffect(() => {
  const savedGratitude = localStorage.getItem('gratitudeEntries');
  const savedMood = localStorage.getItem('moodEntries');
  const savedJournal = localStorage.getItem('journalEntries');
  const savedGoals = localStorage.getItem('goals');
  const savedHabits = localStorage.getItem('habits');
  
  if (savedGratitude) setGratitudeEntries(JSON.parse(savedGratitude));
  if (savedMood) setMoodEntries(JSON.parse(savedMood));
  if (savedJournal) setJournalEntries(JSON.parse(savedJournal));
  if (savedGoals) setGoals(JSON.parse(savedGoals));
  if (savedHabits) setHabits(JSON.parse(savedHabits));
}, []);

// Save data whenever it changes
useEffect(() => {
  localStorage.setItem('gratitudeEntries', JSON.stringify(gratitudeEntries));
}, [gratitudeEntries]);

useEffect(() => {
  localStorage.setItem('moodEntries', JSON.stringify(moodEntries));
}, [moodEntries]);

useEffect(() => {
  localStorage.setItem('journalEntries', JSON.stringify(journalEntries));
}, [journalEntries]);

useEffect(() => {
  localStorage.setItem('goals', JSON.stringify(goals));
}, [goals]);

useEffect(() => {
  localStorage.setItem('habits', JSON.stringify(habits));
}, [habits]);
```

### Customizing Colors

The app uses Tailwind CSS. To change colors:

1. Open `mental-health-app.jsx`
2. Find color classes (e.g., `bg-purple-500`, `text-blue-600`)
3. Replace with Tailwind colors:
   - `purple` → `blue`, `green`, `red`, `pink`, etc.
   - Numbers: `50` (lightest) to `900` (darkest)

**Example:**
```javascript
// Change from purple to blue
className="bg-purple-500" → className="bg-blue-500"
className="text-purple-600" → className="text-blue-600"
```

### Adding New Affirmations

1. Open `mental-health-app.jsx`
2. Find the `affirmations` array
3. Add new quotes:

```javascript
const affirmations = [
  "I am worthy of love and respect",
  "Your new affirmation here",
  "Another affirmation",
  // Add as many as you want
];
```

### Adding New Journal Prompts

1. Find the `journalPrompts` array
2. Add new prompts:

```javascript
const journalPrompts = [
  "What made me smile today?",
  "Your new prompt here",
  "Another prompt",
];
```

### Adding New Self-Care Activities

1. Find the `selfCareActivities` array
2. Add new activities:

```javascript
const selfCareActivities = [
  { activity: "Your activity", icon: "🎯", category: "Physical" },
  // Categories: Physical, Mental, Social, Emotional
];
```

---

## Deployment Options

### Option 1: GitHub Pages (Free Hosting)

1. Create a GitHub repository
2. Upload all files
3. Go to Settings → Pages
4. Select branch and save
5. Your app will be live at: `https://yourusername.github.io/repo-name`

### Option 2: Netlify (Free Hosting)

1. Create account at netlify.com
2. Drag and drop your folder
3. Your app goes live instantly
4. Get a free URL: `https://your-app.netlify.app`

### Option 3: Vercel (Free Hosting)

1. Create account at vercel.com
2. Import your GitHub repository
3. Deploy automatically
4. Get a free URL: `https://your-app.vercel.app`

---

## System Requirements

### Minimum Requirements
- **Browser:** Any modern browser (Chrome, Firefox, Safari, Edge)
- **Internet:** Required for CDN resources (icons, React, Tailwind)
- **JavaScript:** Must be enabled
- **Storage:** ~5 MB for cache

### Recommended
- **Browser:** Chrome or Firefox (latest version)
- **Internet:** Stable connection
- **Screen:** 1024x768 or larger (works on mobile too)

---

## Support

### Getting Help

1. **Check Console Errors:** Press F12 → Console tab
2. **Try Different Browser:** Test in Chrome or Firefox
3. **Clear Cache:** Remove old cached files
4. **Use Local Server:** More reliable than direct file opening

### Common Questions

**Q: Do I need to install anything?**
A: No! Just open the HTML file. React and other libraries load from CDN.

**Q: Can I use this offline?**
A: Not completely - it needs internet for CDN resources. You could download libraries locally for offline use.

**Q: Is my data private?**
A: Yes! Everything stays in your browser. Nothing is sent to any server.

**Q: Can I share this with others?**
A: Absolutely! Just share the files or deploy to a hosting service.

**Q: How do I update the app?**
A: Download the new version and replace the old files.

---

## Contributing

Want to improve the app? Here's how:

1. Make your changes to `mental-health-app.jsx`
2. Test thoroughly in multiple browsers
3. Document your changes
4. Share with the community!

---

## License

MIT License - Free to use, modify, and distribute.

---

**Need more help? Check README.md or browser console for errors!**
