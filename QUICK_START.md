# 🚀 HireLens - Quick Start Guide

## 🔧 **PERMANENT FIX FOR "FAILED TO FETCH" ERROR**

### **Step 1: Start Backend Server**
Double-click on: `run_backend.bat` (in project folder)

Wait for this message:
```
Application startup complete.
Uvicorn running on http://0.0.0.0:8000
```

### **Step 2: Start Frontend**
In another terminal:
```bash
cd frontend
npm run dev
```

### **Step 3: Open Browser**
Go to: `http://localhost:5173`

---

## 🎯 **What This Fixes:**
- ✅ No more "Failed to fetch" errors
- ✅ Backend status indicator in UI
- ✅ Automatic retry logic
- ✅ Clear error messages with solutions

---

## 📋 **Troubleshooting:**

### **If backend won't start:**
1. Make sure Python is installed
2. Run: `pip install -r requirements.txt`
3. Try: `python auto_start_backend.py`

### **If frontend shows "Backend offline":**
1. Check if backend terminal is running
2. Look for green status indicator
3. Click "Click here to start backend" button

### **If still not working:**
1. Restart both backend and frontend
2. Clear browser cache
3. Check if port 8000 is free

---

## 🔄 **Every Time You Start Windsurf:**
1. Double-click `run_backend.bat`
2. Wait for startup complete
3. Refresh browser page

That's it! No more errors! 🎉
