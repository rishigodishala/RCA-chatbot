# 🧪 Manual Testing Guide - RCA Technical Chatbot

## Complete Frontend & Integration Testing Checklist

This guide will help you thoroughly test all features of the transformed RCA chatbot.

---

## 🎯 Testing Prerequisites

### **1. Ensure Application is Running**
```bash
cd /Users/godishalarishi/chatbot
streamlit run app.py
```

### **2. Open in Browser**
- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.0.17:8501

### **3. Prepare Test Materials**
- Have 2-3 test images ready (any format: jpg, png)
- Prepare sample problem descriptions
- Keep this checklist open while testing

---

## ✅ TEST SUITE 1: UI Components & Navigation

### **Test 1.1: Initial Page Load**
- [ ] Page loads without errors
- [ ] Title displays: "AI-Driven Technical Problem-Solving Chatbot"
- [ ] Sidebar is visible
- [ ] Chat input box is present
- [ ] No error messages displayed

**Expected Result:** Clean, professional interface loads successfully

---

### **Test 1.2: RCA Workflow Selector**
- [ ] Dropdown shows "Select RCA Methodology"
- [ ] Click dropdown - shows 3 options: 8D, 5-Why, A3
- [ ] Select "8D" - selection updates
- [ ] Select "5-Why" - selection updates
- [ ] Select "A3" - selection updates
- [ ] Methodology info box updates with each selection

**Expected Result:** All three methodologies selectable, info updates correctly

---

### **Test 1.3: Sidebar Information**
- [ ] Sidebar shows selected methodology
- [ ] "About This Methodology" section displays
- [ ] Content changes when methodology changes
- [ ] Metrics section is visible (initially empty)

**Expected Result:** Sidebar provides contextual information

---

## ✅ TEST SUITE 2: Chat Interface & AI Responses

### **Test 2.1: Starting an Investigation (8D Workflow)**

**Steps:**
1. Select "8D" methodology
2. Type "start" in chat input
3. Press Enter

**Verify:**
- [ ] Welcome message appears
- [ ] Message mentions "8D Root Cause Analysis"
- [ ] First question asks about the problem
- [ ] Message formatting is clean and readable

**Expected Result:** AI welcomes user and asks for problem description

---

### **Test 2.2: Problem Context Questions**

**Step 1: Problem Description**
- Type: "Production line equipment failing, causing 15% downtime"
- Press Enter

**Verify:**
- [ ] Your message appears in chat
- [ ] AI responds within 5-10 seconds
- [ ] AI acknowledges the problem
- [ ] AI asks about timing (when it occurred)
- [ ] Response is contextual and relevant

**Step 2: Timing Information**
- Type: "Started 2 weeks ago, occurs 3-4 times daily"
- Press Enter

**Verify:**
- [ ] AI acknowledges timing
- [ ] AI asks about impact/severity
- [ ] Response shows understanding of timeline

**Step 3: Impact Assessment**
- Type: "High severity - production delays, quality issues, safety concerns"
- Press Enter

**Verify:**
- [ ] AI acknowledges severity
- [ ] AI begins RCA investigation
- [ ] First RCA question is generated
- [ ] Question is specific and relevant

**Expected Result:** AI guides through context collection smoothly

---

### **Test 2.3: RCA Investigation Questions**

**Continue answering questions (7 total):**

For each question:
- [ ] AI question is clear and specific
- [ ] Question relates to root cause analysis
- [ ] Question builds on previous answers
- [ ] AI provides analysis after each response
- [ ] Analysis includes insights and next steps
- [ ] Progress percentage increases

**Sample Responses to Use:**
1. "We noticed vibration in the motor before failures"
2. "Maintenance was performed 3 weeks ago"
3. "Similar equipment in other lines works fine"
4. "Error logs show temperature spikes"
5. "Operators reported unusual noise"
6. "Inspection revealed worn bearings"
7. "Root cause appears to be inadequate lubrication schedule"

**Expected Result:** AI conducts intelligent, adaptive investigation

---

### **Test 2.4: Investigation Completion**
- [ ] After 7 RCA questions, AI indicates completion
- [ ] Message says "Investigation complete"
- [ ] AI suggests generating report
- [ ] Sidebar metrics show 100% progress

**Expected Result:** Clear indication investigation is finished

---

## ✅ TEST SUITE 3: Sidebar Metrics & Progress

### **Test 3.1: Metrics Display**

**During Investigation:**
- [ ] "Investigation Metrics" section appears in sidebar
- [ ] Shows "Problem Severity" (0-100)
- [ ] Shows "Root Cause Confidence" (0-100)
- [ ] Shows "Solution Feasibility" (0-100)
- [ ] Shows "Investigation Progress" (0-100%)

**Verify Updates:**
- [ ] Metrics update after each response
- [ ] Progress increases incrementally
- [ ] Values are reasonable (not all zeros or 100s)
- [ ] Formatting is clean and readable

**Expected Result:** Real-time metrics tracking throughout investigation

---

## ✅ TEST SUITE 4: Image Upload Feature

### **Test 4.1: Image Upload Widget**
- [ ] "Upload Evidence Images" section visible
- [ ] File uploader accepts multiple files
- [ ] Supported formats listed (PNG, JPG, JPEG)

**Expected Result:** Image upload interface is accessible

---

### **Test 4.2: Upload Single Image**

**Steps:**
1. Click "Browse files"
2. Select one test image
3. Upload

**Verify:**
- [ ] Image uploads successfully
- [ ] Thumbnail or filename displayed
- [ ] No error messages
- [ ] Can continue chatting after upload

**Expected Result:** Single image uploads without issues

---

### **Test 4.3: Upload Multiple Images**

**Steps:**
1. Click "Browse files"
2. Select 2-3 test images
3. Upload

**Verify:**
- [ ] All images upload successfully
- [ ] All thumbnails/filenames displayed
- [ ] Images are tracked in session
- [ ] Can remove images if needed

**Expected Result:** Multiple images handled correctly

---

### **Test 4.4: Image in Context**

**During investigation:**
- Upload an image
- Continue answering questions

**Verify:**
- [ ] Chat continues normally
- [ ] Images remain visible
- [ ] AI doesn't break or error
- [ ] Images will be included in report

**Expected Result:** Images integrate seamlessly with investigation

---

## ✅ TEST SUITE 5: Report Generation

### **Test 5.1: Text Report Generation**

**After completing investigation:**
1. Click "Generate Text Report" button

**Verify:**
- [ ] Button is clickable
- [ ] Report generates within 2-3 seconds
- [ ] Text area displays full report
- [ ] Report includes:
  - [ ] Problem context
  - [ ] Investigation methodology (8D/5-Why/A3)
  - [ ] Conversation history
  - [ ] Root cause analysis
  - [ ] Recommendations
  - [ ] Metrics summary
- [ ] Report is well-formatted
- [ ] All sections are complete

**Expected Result:** Comprehensive text report generated

---

### **Test 5.2: PDF Report Generation**

**Steps:**
1. Click "Generate PDF Report" button

**Verify:**
- [ ] Button is clickable
- [ ] PDF generates within 3-5 seconds
- [ ] Download button appears
- [ ] Click download - PDF file downloads
- [ ] Open PDF - content is readable
- [ ] PDF includes:
  - [ ] Title and date
  - [ ] Problem context
  - [ ] Metrics chart/visualization
  - [ ] Investigation summary
  - [ ] Recommendations
  - [ ] Professional formatting

**Expected Result:** Professional PDF report downloads successfully

---

### **Test 5.3: Report with Images**

**If images were uploaded:**
- [ ] Text report mentions evidence images
- [ ] PDF report includes image thumbnails or references
- [ ] Image count is accurate

**Expected Result:** Evidence images incorporated in reports

---

## ✅ TEST SUITE 6: All Three RCA Methodologies

### **Test 6.1: 5-Why Workflow**

**Steps:**
1. Refresh page (or click "New Investigation")
2. Select "5-Why" methodology
3. Type "start"
4. Complete investigation with different problem

**Verify:**
- [ ] Welcome message mentions "5-Why"
- [ ] Questions focus on iterative "why" analysis
- [ ] AI asks "why" questions progressively
- [ ] Report format is 5-Why specific
- [ ] Sidebar shows 5-Why methodology info

**Expected Result:** 5-Why methodology works distinctly

---

### **Test 6.2: A3 Workflow**

**Steps:**
1. Refresh page
2. Select "A3" methodology
3. Type "start"
4. Complete investigation with different problem

**Verify:**
- [ ] Welcome message mentions "A3"
- [ ] Questions align with A3 format
- [ ] AI focuses on one-page problem-solving approach
- [ ] Report format is A3 specific
- [ ] Sidebar shows A3 methodology info

**Expected Result:** A3 methodology works distinctly

---

## ✅ TEST SUITE 7: Edge Cases & Error Handling

### **Test 7.1: Empty Messages**
- [ ] Try sending empty message - should be prevented or handled
- [ ] Try sending only spaces - should be handled

**Expected Result:** Graceful handling of invalid input

---

### **Test 7.2: Very Long Messages**
- [ ] Send a very long message (500+ words)
- [ ] AI should process and respond appropriately
- [ ] No truncation or errors

**Expected Result:** Long messages handled correctly

---

### **Test 7.3: Special Characters**
- [ ] Send message with special characters: @#$%^&*()
- [ ] Send message with emojis: 🔧⚙️🛠️
- [ ] AI should handle gracefully

**Expected Result:** Special characters don't break the system

---

### **Test 7.4: Rapid Messages**
- [ ] Send multiple messages quickly (3-4 in succession)
- [ ] AI should queue and respond to each
- [ ] No messages lost or duplicated

**Expected Result:** Message queue handled properly

---

### **Test 7.5: Page Refresh During Investigation**
- [ ] Start investigation
- [ ] Answer 2-3 questions
- [ ] Refresh page
- [ ] Check if conversation persists or resets

**Expected Result:** Session state behavior is predictable

---

### **Test 7.6: Large Image Upload**
- [ ] Try uploading very large image (>10MB)
- [ ] Should either upload or show size limit error
- [ ] No application crash

**Expected Result:** Large files handled gracefully

---

## ✅ TEST SUITE 8: Session Management

### **Test 8.1: Multiple Investigations**
- [ ] Complete one investigation
- [ ] Start new investigation (refresh or new session)
- [ ] Previous data should be cleared
- [ ] New investigation starts fresh

**Expected Result:** Clean session management

---

### **Test 8.2: Browser Back/Forward**
- [ ] Use browser back button during investigation
- [ ] Use browser forward button
- [ ] Check if state is maintained or reset

**Expected Result:** Navigation doesn't break application

---

## ✅ TEST SUITE 9: Performance & Responsiveness

### **Test 9.1: Response Time**
- [ ] AI responses arrive within 5-10 seconds
- [ ] No excessive delays
- [ ] Loading indicators work (if present)

**Expected Result:** Acceptable response times

---

### **Test 9.2: UI Responsiveness**
- [ ] Resize browser window - UI adapts
- [ ] Test on mobile device (if available)
- [ ] Sidebar collapses on small screens
- [ ] Chat remains usable

**Expected Result:** Responsive design works

---

### **Test 9.3: Memory Usage**
- [ ] Complete long investigation (10+ messages)
- [ ] Browser doesn't slow down
- [ ] No memory leaks apparent

**Expected Result:** Stable performance throughout

---

## ✅ TEST SUITE 10: Integration Testing

### **Test 10.1: RAG Engine**

**During investigation:**
- [ ] AI responses reference RCA methodologies
- [ ] AI mentions specific techniques (8D steps, 5-Why, A3 format)
- [ ] Responses show knowledge of best practices

**Expected Result:** RAG successfully retrieves methodology knowledge

---

### **Test 10.2: Complete End-to-End Flow**

**Full workflow test:**
1. [ ] Select methodology
2. [ ] Start investigation
3. [ ] Answer all context questions
4. [ ] Upload 2 evidence images
5. [ ] Answer all RCA questions
6. [ ] Generate text report
7. [ ] Generate PDF report
8. [ ] Download PDF
9. [ ] Verify all data in report

**Expected Result:** Seamless end-to-end experience

---

## 📊 Testing Summary Template

After completing all tests, fill out this summary:

### **Overall Results:**
- Total Tests: ___
- Passed: ___
- Failed: ___
- Blocked: ___

### **Critical Issues Found:**
1. ___
2. ___
3. ___

### **Minor Issues Found:**
1. ___
2. ___
3. ___

### **Recommendations:**
1. ___
2. ___
3. ___

### **Ready for Production?**
- [ ] Yes - All critical tests passed
- [ ] No - Critical issues need fixing
- [ ] Partial - Minor issues acceptable

---

## 🎯 Success Criteria

**Application is considered fully tested and ready when:**
- ✅ All three RCA methodologies work correctly
- ✅ AI generates intelligent, context-aware responses
- ✅ Image upload functions properly
- ✅ Reports generate successfully (text and PDF)
- ✅ No critical bugs or errors
- ✅ Performance is acceptable
- ✅ User experience is smooth

---

## 📝 Notes Section

Use this space to record observations, issues, or suggestions:

```
[Your notes here]
```

---

**Testing Date:** ___________  
**Tester Name:** ___________  
**Application Version:** 1.0.0  
**Status:** ___________
