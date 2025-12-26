# YouTube Comment Reply Monitor

Monitor replies to **YOUR comments** on **OTHER people's videos** and get alerted when specific keywords are mentioned!

## 🎯 What Does This Do?

This script helps you stay on top of conversations you've started on YouTube by:

1. **Scanning your comment history** on other people's videos
2. **Checking all replies** to your comments  
3. **Matching keywords** from a customizable list
4. **Alerting you** when someone uses those keywords in a reply

Perfect for:
- 💬 Following up on discussions
- 🔍 Tracking mentions of specific topics
- 🚨 Detecting spam or trolls
- 📊 Monitoring engagement with your comments
- 🤝 Finding collaboration opportunities

---

## 📋 Prerequisites

- Python 3.7 or higher
- Google Cloud project with YouTube Data API v3 enabled
- OAuth 2.0 credentials (`client_secret.json`)

**See SETUP_GUIDE.md if you need help with Google Cloud setup!**

---

## 🚀 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up credentials:**
   - Place your `client_secret.json` in the same folder
   - (Same file used for the comment replier script)

3. **Run the script:**
   ```bash
   python youtube_reply_monitor.py
   ```

---

## 📝 How to Use

### Basic Usage

```bash
python youtube_reply_monitor.py
```

You'll be prompted for:
- **Days back to search**: How far back to check (default: 30 days)
- **Max comments to check**: How many of your recent comments to scan (default: 50)

### Example Session

```
YouTube Comment Reply Monitor with Keyword Matching
================================================================================
✓ Successfully authenticated with YouTube API
✓ Loaded 35 keywords from keywords.json
👤 Monitoring comments for: Your Channel Name

How many days back to search? [default: 30]: 7
Maximum comments to check? [default: 50]: 20

================================================================================
🔍 Scanning for replies to your comments on OTHER people's videos...
================================================================================

Keywords monitoring: thanks, question, help, link, source, spam, bot
Looking back: 7 days
Max comments to check: 20

📥 Fetching your recent comments...
   Found 20 of your comments

🔍 Filtering for comments on OTHER people's videos...
   Found 15 comments on other people's videos

================================================================================
📬 Checking for replies with matching keywords...
================================================================================

[1/15] Checking comment on:
    Video: How to Build a Gaming PC in 2024 - Complete Guide
    Channel: Tech Reviews Daily
    Replies: 3

    🎯 MATCH FOUND! ===========================================================
    Keywords: thanks, help
    From: TechGuru42
    When: 2 days ago
    Reply: Thanks for this! Your point about the PSU was really helpful...
    Likes: 12
    Video URL: https://youtube.com/watch?v=abc123xyz
    =========================================================================

✓ SCAN COMPLETE
================================================================================
Comments checked: 15
Total replies found: 45
Replies matching keywords: 8
================================================================================
```

---

## ⚙️ Customizing Keywords

### Edit keywords.json

The script automatically creates a `keywords.json` file with default keywords. Customize it:

```json
{
  "keywords": [
    "thanks",
    "question",
    "help",
    "link",
    "your custom keyword here"
  ],
  "case_sensitive": false,
  "description": "Your custom description"
}
```

### Keyword Ideas by Use Case

**Track Engagement:**
```json
["thanks", "helpful", "great point", "interesting", "learned"]
```

**Find Questions:**
```json
["?", "question", "how", "what", "why", "help"]
```

**Detect Spam:**
```json
["subscribe", "check out my", "click here", "free", "winner"]
```

**Monitor Debates:**
```json
["disagree", "wrong", "actually", "source", "proof", "evidence"]
```

**Business Opportunities:**
```json
["collaboration", "partner", "work together", "contact", "email"]
```

**Brand Monitoring:**
```json
["YourBrandName", "competitor name", "product name"]
```

---

## 🔧 Advanced Features

### Case Sensitivity

Set `"case_sensitive": true` in keywords.json to match exact case:
- `"SPAM"` will match "SPAM" but not "spam"
- Useful for acronyms or specific brand names

### Filtering by Time

The script automatically filters comments by date based on your input:
- `days_back: 7` - Last week only
- `days_back: 30` - Last month (default)
- `days_back: 90` - Last 3 months

---

## 📊 Understanding the Results

### What Gets Checked?

✅ **Included:**
- Your comments on OTHER people's videos
- All replies to those comments
- Public comments only

❌ **Excluded:**
- Comments on YOUR OWN videos (use YouTube Studio for those)
- Private/deleted comments
- Comments older than your search range

### Why No Results?

If you see "0 comments found":
1. You haven't commented on others' videos recently
2. Your comments are older than the search range
3. You only comment on your own videos

---

## 🎯 Use Cases & Examples

### 1. **Content Creator Monitoring**
```json
{
  "keywords": ["tutorial", "how to", "guide", "explain", "link"],
  "description": "Find people asking for more content"
}
```

### 2. **Tech Support Follow-up**
```json
{
  "keywords": ["help", "error", "issue", "problem", "fix", "worked"],
  "description": "Track if your advice helped people"
}
```

### 3. **Spam Detection**
```json
{
  "keywords": ["subscribe to me", "check my channel", "click here", "free robux"],
  "description": "Detect spam replies to report"
}
```

### 4. **Research & Citations**
```json
{
  "keywords": ["source", "citation", "study", "research", "data", "proof"],
  "description": "Find academic discussions"
}
```

### 5. **Community Management**
```json
{
  "keywords": ["rude", "offensive", "report", "inappropriate", "delete"],
  "description": "Catch negative interactions"
}
```

---

## 🔒 API Quota Usage

**Costs per run:**
- Fetching your comments: ~1 unit per 100 comments
- Checking replies: ~1 unit per comment with replies
- **Typical run (50 comments)**: 50-100 units

**Daily quota:** 10,000 units (default)
- You can run this script ~100-200 times per day
- Much lighter than the comment replier script

---

## 🐛 Troubleshooting

### "No comments on other people's videos"
- Make sure you've actually commented on videos that aren't yours
- Try increasing `max_comments` to search more history
- Increase `days_back` if your comments are older

### "API quota exceeded"
- Wait 24 hours for quota reset
- Reduce `max_comments` parameter
- Request quota increase in Google Cloud Console

### "Error 403: Forbidden"
- Check that YouTube Data API v3 is enabled
- Verify your OAuth consent screen settings
- Delete `token.pickle` and re-authenticate

---

## 💡 Tips & Best Practices

1. **Run Regularly**: Set up a daily/weekly schedule to catch new replies
2. **Targeted Keywords**: Focus on 5-10 highly relevant keywords
3. **Adjust Time Range**: 
   - Daily monitoring: `days_back: 1`
   - Weekly digest: `days_back: 7`
   - Monthly review: `days_back: 30`
4. **Save Results**: Take screenshots or notes of important matches
5. **Respond Promptly**: Engage with replies while discussions are active

---

## 🔄 Automation Ideas

### Linux/Mac Cron Job (Daily at 9 AM)
```bash
0 9 * * * cd /path/to/script && python3 youtube_reply_monitor.py
```

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 9:00 AM
4. Action: Start Program
5. Program: `python`
6. Arguments: `C:\path\to\youtube_reply_monitor.py`

---

## 📈 Future Enhancements

Potential features (you can add these!):
- Export results to CSV/Excel
- Email/Discord notifications for matches
- Track reply sentiment (positive/negative)
- Generate statistics over time
- Auto-reply to certain keywords

---

## 🆚 Difference from YouTube Studio

**YouTube Studio shows:**
- Comments on YOUR videos only
- All notifications (likes, subscribers, etc.)

**This script shows:**
- Replies to YOUR comments on OTHER people's videos
- Filtered by your custom keywords
- Focused on conversations you started elsewhere

---

## 🤝 Related Scripts

- **youtube_comment_replier.py** - Reply to comments on YOUR videos
- **This script** - Monitor replies to YOUR comments on other videos

Both use the same `client_secret.json` file!

---

## 📚 Resources

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Comment Management Guide](https://support.google.com/youtube/answer/9706180)
- [API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)

---

## ⚖️ Terms of Use

- Use responsibly and ethically
- Respect others' privacy
- Follow YouTube's Terms of Service
- Don't spam or harass based on keyword matches
- This is for personal monitoring, not mass surveillance

---

**Happy monitoring!** 🎉

Edit `keywords.json` to customize your experience and stay on top of your YouTube conversations!
