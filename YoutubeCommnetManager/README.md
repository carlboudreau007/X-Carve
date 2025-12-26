# YouTube Comment Replier

A Python script that allows you to reply to all comments on a YouTube video using the official YouTube Data API v3.

## ⚠️ Important: Ethical Use

**This script should ONLY be used:**
- On YOUR OWN videos
- For legitimate community engagement
- With personalized, valuable replies
- In compliance with YouTube's Terms of Service

**DO NOT use this for:**
- Spam or mass unsolicited messages
- Generic/automated replies on others' videos
- Any activity that violates YouTube's policies

## Features

- 🔐 Secure OAuth 2.0 authentication
- 📥 Fetches all comments from a video
- 💬 Personalized reply templates with commenter names
- 👀 Preview mode before posting
- ⏱️ Built-in rate limiting
- ✅ Error handling and progress tracking

## Prerequisites

- Python 3.7 or higher
- A Google Cloud Platform account
- YouTube Data API v3 enabled

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Create a new project (or select existing)

3. Enable YouTube Data API v3:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

4. Create OAuth 2.0 Credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Name it (e.g., "YouTube Comment Replier")
   - Click "Create"

5. Download Credentials:
   - Click the download button (⬇️) next to your OAuth client
   - Save the file as `client_secret.json`
   - Place it in the same directory as the script

### 3. Project Structure

```
your-folder/
├── youtube_comment_replier.py
├── requirements.txt
├── client_secret.json (you'll add this)
└── README.md
```

## Usage

### Basic Usage

Run the script:

```bash
python youtube_comment_replier.py
```

You'll be prompted for:
1. **Video URL** - The YouTube video URL (or video ID)
2. **Reply template** - Your reply message

### Reply Template

Use `{name}` in your template to personalize with the commenter's name:

```
Thank you {name} for watching and commenting!
```

### Example Session

```
Enter YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Reply template: Thank you {name} for your comment! 😊

📹 Video ID: dQw4w9WgXcQ
Title: Example Video Title
Channel: Your Channel
Comments: 150

📥 Fetching comments...
✓ Found 150 comments

PREVIEW MODE - Showing first 5 comments
==========================================================
1. John Doe:
   Great video!...
   Reply: Thank you John Doe for your comment! 😊

Reply to all 150 comments? (yes/no): yes

📤 Starting to post replies...
[1/150] Replying to John Doe...
  ✓ Success
...
```

## Rate Limits

The script includes built-in rate limiting:
- 2 seconds between each reply
- Respects YouTube API quotas (10,000 units/day by default)

**Note:** Replying to a comment costs 50 quota units. With the default quota, you can reply to ~200 comments per day.

## First Run Authentication

On first run, the script will:
1. Open your browser for Google authentication
2. Ask you to grant permissions
3. Save credentials to `token.pickle` for future use

## Troubleshooting

### "client_secret.json not found"
- Make sure you've downloaded OAuth credentials from Google Cloud Console
- Place the file in the same directory as the script
- Rename it to exactly `client_secret.json`

### "The request cannot be completed because you have exceeded your quota"
- You've hit the daily YouTube API quota (10,000 units)
- Wait 24 hours or request a quota increase in Google Cloud Console

### "Video not found" or "Cannot fetch comments"
- Check that the video URL is correct
- Ensure comments are enabled on the video
- Verify the video is public or you have access

### Authentication Issues
- Delete `token.pickle` and re-authenticate
- Check that OAuth credentials are for "Desktop app" type

## API Costs

YouTube Data API v3 quota costs:
- Fetching comments: 1 unit per request (100 comments)
- Posting a reply: 50 units per reply

Daily quota: 10,000 units (default)
Maximum replies per day: ~200

## Best Practices

1. **Test First**: Use preview mode and test on a video with few comments
2. **Personalize**: Always customize replies, don't use generic messages
3. **Be Authentic**: Make replies meaningful and relevant
4. **Monitor**: Check replies for errors or issues
5. **Rate Limit**: The script includes delays, but be mindful of volume
6. **Own Content**: Only use on your own videos for community management

## Security Notes

- `client_secret.json` contains sensitive data - don't share it
- `token.pickle` stores your access token - keep it private
- Add both files to `.gitignore` if using version control

```bash
# .gitignore
client_secret.json
token.pickle
```

## License

Use responsibly and in accordance with YouTube's Terms of Service.

## Support

For issues with:
- **YouTube API**: Check [YouTube API Documentation](https://developers.google.com/youtube/v3)
- **Google Cloud**: Visit [Cloud Console Support](https://console.cloud.google.com/support)

---

**Disclaimer**: This script is for educational and legitimate community management purposes only. Users are responsible for complying with YouTube's Terms of Service and API usage policies.
