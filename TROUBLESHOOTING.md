# 🔧 Troubleshooting Guide

Having issues? Here are solutions to common problems.

---

## Installation Issues

### Problem: `npm install` fails

**Solution 1: Check Node.js version**
```bash
node --version
```
You need Node.js v14 or higher. If lower, download from nodejs.org

**Solution 2: Clear npm cache**
```bash
npm cache clean --force
npm install
```

**Solution 3: Delete node_modules and try again**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Problem: "Cannot find module" errors

**Solution:** Make sure all files are in the correct locations as shown in PROJECT-STRUCTURE.md

---

## Running the App

### Problem: `npm run dev` fails

**Solution 1: Port already in use**
The app tries to use port 3000. If it's in use:

Edit `vite.config.js` and change the port:
```javascript
server: {
  port: 3001,  // Changed from 3000
  open: true
}
```

**Solution 2: Missing dependencies**
```bash
npm install
npm run dev
```

### Problem: App won't open in browser

**Solution:** Manually open your browser and go to:
```
http://localhost:3000
```

### Problem: Blank white screen

**Solution 1: Check browser console**
- Press F12 to open developer tools
- Look for error messages in the Console tab
- Common fix: Hard refresh with Ctrl+Shift+R (Cmd+Shift+R on Mac)

**Solution 2: Clear browser cache**
- Chrome: Ctrl+Shift+Delete → Clear browsing data
- Firefox: Ctrl+Shift+Delete → Clear recent history
- Safari: Cmd+Option+E

---

## Styling Issues

### Problem: Styles not loading / App looks unstyled

**Solution 1: Rebuild the app**
```bash
npm run dev
```
Wait for "ready in XXXms" message before opening browser

**Solution 2: Check Tailwind configuration**
Ensure `tailwind.config.js` has correct content paths:
```javascript
content: [
  "./index.html",
  "./src/**/*.{js,ts,jsx,tsx}",
],
```

**Solution 3: Verify index.css**
Make sure `src/index.css` has Tailwind directives:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Icons Not Showing

### Problem: Lucide icons not displaying

**Solution:** Reinstall lucide-react:
```bash
npm uninstall lucide-react
npm install lucide-react@0.263.1
```

---

## Data/State Issues

### Problem: My data disappears when I refresh

**This is normal!** The app currently stores data in memory only. When you refresh, it resets.

**Future enhancement:** To persist data, you could add:
- localStorage
- Backend database
- Export/Import functionality

### Problem: Features not working correctly

**Solution 1: Hard refresh**
- Windows/Linux: Ctrl+Shift+R
- Mac: Cmd+Shift+R

**Solution 2: Clear browser storage**
- Open Developer Tools (F12)
- Go to Application tab
- Clear storage
- Refresh page

---

## Build Issues

### Problem: `npm run build` fails

**Solution 1: Check for errors in code**
```bash
npm run dev
```
If dev works but build doesn't, check console for specific errors

**Solution 2: Clear dist folder**
```bash
rm -rf dist
npm run build
```

### Problem: Production build not working

**Solution:** Make sure you're serving the build correctly:
```bash
npm run build
npm run preview
```

---

## Browser Compatibility

### Supported Browsers
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Problem: Features not working in older browsers

**Solution:** Update your browser to the latest version

---

## Performance Issues

### Problem: App is slow or laggy

**Solution 1: Too much data**
If you have hundreds of entries, consider:
- Clearing old data (delete old entries)
- Limiting displayed entries

**Solution 2: Browser extensions**
Disable browser extensions temporarily to test

**Solution 3: Computer performance**
- Close other browser tabs
- Close other applications
- Restart your computer

---

## Development Tips

### Viewing in Different Screen Sizes

**Chrome DevTools:**
1. Press F12
2. Click device toggle icon (Ctrl+Shift+M)
3. Select device or enter custom dimensions

### Making Changes

**Hot Module Replacement (HMR):**
When you save files, changes appear automatically. If not:
```bash
# Stop server (Ctrl+C)
# Restart
npm run dev
```

### Debugging

**Console Logs:**
Add console.logs to mental-health-app.jsx:
```javascript
console.log('Current mood entries:', moodEntries);
```

**React DevTools:**
Install React DevTools browser extension for better debugging

---

## Common Error Messages

### "Cannot read property of undefined"

**Cause:** Trying to access data that doesn't exist yet

**Solution:** Check if data exists before using it:
```javascript
{moodEntries.length > 0 && moodEntries.map(...)}
```

### "Maximum update depth exceeded"

**Cause:** Infinite loop in useEffect or state updates

**Solution:** Check useEffect dependencies and ensure no circular updates

### "Failed to compile"

**Cause:** Syntax error in code

**Solution:** Check the error message for file and line number. Fix the syntax error.

---

## File Structure Problems

### Problem: Import errors

**Make sure file structure matches:**
```
mental-health-app/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── src/
    ├── main.jsx
    ├── mental-health-app.jsx
    └── index.css
```

### Problem: Module not found

**Check imports in main.jsx:**
```javascript
import MentalHealthApp from './mental-health-app';  // No .jsx needed
import './index.css';
```

---

## Getting More Help

### Check Console
Always check browser console (F12 → Console) for error messages

### Check Terminal
Look at terminal where `npm run dev` is running for build errors

### Documentation
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

### Community Help
- Stack Overflow
- Reddit: r/reactjs
- Discord: Reactiflux

---

## Emergency Reset

If nothing works, start fresh:

```bash
# 1. Delete everything except source files
rm -rf node_modules package-lock.json dist

# 2. Reinstall
npm install

# 3. Try running
npm run dev
```

---

## Still Having Issues?

**Checklist:**
- [ ] Node.js v14+ installed?
- [ ] All files in correct locations?
- [ ] Ran `npm install`?
- [ ] No syntax errors in code?
- [ ] Browser is up to date?
- [ ] Checked browser console for errors?
- [ ] Tried hard refresh (Ctrl+Shift+R)?

**If all else fails:**
Re-download the project files and start from scratch.

---

**Remember:** Most issues can be solved by:
1. Checking error messages
2. Hard refresh (Ctrl+Shift+R)
3. Reinstalling dependencies (`npm install`)
4. Restarting the dev server

Good luck! 🍀
