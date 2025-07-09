# Competitive Programming Profile Data Collector

This repository automates the collection of your competitive programming profile data from **Codeforces** and **LeetCode**, storing it in a structured format within your GitHub repository.

---

## 🎯 Purpose of Data Collection

The primary goal of collecting this data is to build a **personal data dashboard**. This dashboard provides a comprehensive and evolving overview of your competitive programming journey. By centralizing this information, you can:

- **📈 Visualize Progress and Trends**  
  Track your rating changes, submission patterns, problem-solving distribution across difficulties, and overall performance over time. This helps in identifying strengths and areas for improvement.

- **📊 Analyze Performance Metrics**  
  Gain insights into your problem-solving speed, accuracy, and consistency. Understand which types of problems you excel at and where you might need more practice.

- **🏆 Showcase Achievements**  
  Create a dynamic portfolio of your competitive programming accomplishments, which can be valuable for personal reflection, sharing with peers, or demonstrating skills to potential employers.

- **📚 Identify Learning Opportunities**  
  By analyzing your submission history and problem statistics, you can pinpoint specific topics or problem types where you frequently struggle, guiding your future learning efforts.

---

## 📦 Data Collected

Currently, this repository collects the following data:

### ✅ Codeforces:
- User Information (Rating, Rank, Max Rating, etc.)
- Submission Status (details of all your submissions)

### ✅ LeetCode:
- User Profile Statistics (Total Solved, Solved by Difficulty, Ranking, etc.)
- Recent Accepted Submissions (a list of your most recent successful problem attempts)

---

## ⚙️ Automation with GitHub Actions

The data collection process is fully automated using **GitHub Actions**.

- A workflow runs **every hour**, executing a Python script `update_profile_data.py`
- It fetches the latest data from the respective APIs
- Updates are committed to the `data/` directory in this repository
- Ensures your dashboard always has fresh information

---

## 🚀 Setup

To set up this automation for your own profile:

1. **Fork this repository**

2. **Update `update_profile_data.py`:**  
   Edit the file in your forked repository:
   ```python
   CODEFORCES_HANDLE = "your_codeforces_handle"
   LEETCODE_USERNAME = "your_leetcode_username"
