#!/usr/bin/env python3
"""
YouTube Comment Replier Script

IMPORTANT: Use this script responsibly and ethically
- Only reply to comments on YOUR OWN videos
- Ensure replies are personalized and valuable
- Comply with YouTube's Terms of Service
- Avoid spam or automated mass messaging
- Consider rate limits and API quotas
"""

import re
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle

# YouTube API settings
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

class YouTubeCommentReplier:
    def __init__(self):
        self.youtube = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with YouTube API using OAuth 2.0"""
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('client_secret.json'):
                    print("\n❌ ERROR: 'client_secret.json' not found!")
                    print("\nTo use this script, you need to:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create a project and enable YouTube Data API v3")
                    print("3. Create OAuth 2.0 credentials (Desktop app)")
                    print("4. Download the credentials as 'client_secret.json'")
                    print("5. Place it in the same directory as this script\n")
                    exit(1)
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future runs
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        print("✓ Successfully authenticated with YouTube API\n")
    
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume it's already a video ID
        return url
    
    def get_video_info(self, video_id):
        """Get basic video information"""
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                return None
            
            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'channel': video['snippet']['channelTitle'],
                'comment_count': video['statistics'].get('commentCount', '0')
            }
        except HttpError as e:
            print(f"❌ Error fetching video info: {e}")
            return None
    
    def get_all_comments(self, video_id):
        """Fetch all top-level comments from a video"""
        comments = []
        next_page_token = None
        
        print("📥 Fetching comments...")
        
        while True:
            try:
                request = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token,
                    textFormat='plainText'
                )
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'id': item['id'],
                        'comment_id': item['snippet']['topLevelComment']['id'],
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likes': comment['likeCount'],
                        'published': comment['publishedAt']
                    })
                
                next_page_token = response.get('nextPageToken')
                print(f"  Fetched {len(comments)} comments so far...")
                
                if not next_page_token:
                    break
                
                time.sleep(0.5)  # Rate limiting
                
            except HttpError as e:
                print(f"❌ Error fetching comments: {e}")
                break
        
        return comments
    
    def reply_to_comment(self, comment_id, reply_text):
        """Reply to a specific comment"""
        try:
            request = self.youtube.comments().insert(
                part='snippet',
                body={
                    'snippet': {
                        'parentId': comment_id,
                        'textOriginal': reply_text
                    }
                }
            )
            response = request.execute()
            return True
        except HttpError as e:
            print(f"  ❌ Error posting reply: {e}")
            return False
    
    def filter_duplicate_users(self, comments):
        """Remove duplicate comments from the same user, keeping only the first one"""
        seen_users = set()
        unique_comments = []
        duplicate_count = 0
        
        for comment in comments:
            author = comment['author']
            if author not in seen_users:
                seen_users.add(author)
                unique_comments.append(comment)
            else:
                duplicate_count += 1
        
        return unique_comments, duplicate_count
    
    def run(self, video_url, reply_template, preview=True, allow_duplicates=False):
        """Main function to reply to all comments"""
        # Extract video ID
        video_id = self.extract_video_id(video_url)
        print(f"📹 Video ID: {video_id}\n")
        
        # Get video info
        video_info = self.get_video_info(video_id)
        if not video_info:
            print("❌ Could not fetch video information. Check the URL.")
            return
        
        print(f"Title: {video_info['title']}")
        print(f"Channel: {video_info['channel']}")
        print(f"Comments: {video_info['comment_count']}\n")
        
        # Fetch all comments
        comments = self.get_all_comments(video_id)
        
        if not comments:
            print("❌ No comments found or unable to fetch comments.")
            return
        
        print(f"\n✓ Found {len(comments)} total comments\n")
        
        # Filter duplicate users unless explicitly allowed
        if not allow_duplicates:
            original_count = len(comments)
            comments, duplicate_count = self.filter_duplicate_users(comments)
            print(f"🔍 Filtering duplicate users...")
            print(f"   Total comments: {original_count}")
            print(f"   Unique users: {len(comments)}")
            print(f"   Duplicate comments removed: {duplicate_count}\n")
        
        # Preview mode
        if preview:
            print("=" * 60)
            print("PREVIEW MODE - Showing first 5 comments to reply to")
            print("=" * 60)
            for i, comment in enumerate(comments[:5], 1):
                print(f"\n{i}. {comment['author']}:")
                print(f"   {comment['text'][:100]}...")
                print(f"   Reply: {reply_template.format(name=comment['author'])}")
            
            print("\n" + "=" * 60)
            response = input(f"\nReply to {len(comments)} unique users? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Cancelled.")
                return
        
        # Reply to comments
        print("\n📤 Starting to post replies...\n")
        success_count = 0
        failed_count = 0
        
        for i, comment in enumerate(comments, 1):
            reply_text = reply_template.format(name=comment['author'])
            print(f"[{i}/{len(comments)}] Replying to {comment['author']}...")
            
            if self.reply_to_comment(comment['comment_id'], reply_text):
                success_count += 1
                print(f"  ✓ Success")
            else:
                failed_count += 1
            
            # Rate limiting - wait between posts
            if i < len(comments):
                time.sleep(2)  # 2 seconds between replies
        
        print("\n" + "=" * 60)
        print(f"✓ Complete!")
        print(f"  Successfully replied: {success_count}")
        print(f"  Failed: {failed_count}")
        if not allow_duplicates:
            print(f"  Duplicate users skipped: {duplicate_count}")
        print("=" * 60)


def main():
    print("=" * 60)
    print("YouTube Comment Replier")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Use responsibly and ethically!")
    print("   - Only use on YOUR OWN videos")
    print("   - Personalize your replies")
    print("   - Respect YouTube's Terms of Service\n")
    
    # Initialize
    replier = YouTubeCommentReplier()
    
    # Get video URL
    video_url = input("Enter YouTube video URL: ").strip()
    
    # Get reply template
    print("\nEnter your reply message template.")
    print("Use {name} to personalize with commenter's name.")
    print("Example: Thank you {name} for watching and commenting!\n")
    reply_template = input("Reply template: ").strip()
    
    if not reply_template:
        reply_template = "Thank you for your comment!"
    
    # Ask about duplicate handling
    print("\n📋 Duplicate Comment Handling:")
    print("   Some users may have commented multiple times.")
    duplicate_choice = input("Reply to each user only once? (yes/no) [default: yes]: ").strip().lower()
    allow_duplicates = duplicate_choice in ['no', 'n']
    
    # Run with preview
    replier.run(video_url, reply_template, preview=True, allow_duplicates=allow_duplicates)


if __name__ == '__main__':
    main()
