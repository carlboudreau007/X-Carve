#!/usr/bin/env python3
"""
YouTube Comment Reply Monitor

This script checks replies to YOUR comments on OTHER people's videos
and searches for specific keywords defined in a JSON configuration file.
"""

import json
import os
import pickle
import re
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

# YouTube API settings
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

class YouTubeReplyMonitor:
    def __init__(self, keywords_file='keywords.json'):
        self.youtube = None
        self.keywords_file = keywords_file
        self.keywords = self.load_keywords()
        self.my_channel_id = None
        self.authenticate()
        self.get_my_channel_id()
    
    def authenticate(self):
        """Authenticate with YouTube API using OAuth 2.0"""
        creds = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('client_secret.json'):
                    print("\n❌ ERROR: 'client_secret.json' not found!")
                    print("\nPlease set up OAuth credentials first.")
                    print("See SETUP_GUIDE.md for instructions.\n")
                    exit(1)
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        print("✓ Successfully authenticated with YouTube API\n")
    
    def load_keywords(self):
        """Load keywords from JSON file"""
        if not os.path.exists(self.keywords_file):
            # Create default keywords file if it doesn't exist
            default_keywords = {
                "keywords": [
                    "thanks",
                    "thank you",
                    "great point",
                    "agree",
                    "disagree",
                    "question",
                    "help",
                    "tutorial",
                    "link",
                    "source"
                ],
                "case_sensitive": False,
                "description": "Keywords to monitor in replies to your comments"
            }
            with open(self.keywords_file, 'w') as f:
                json.dump(default_keywords, f, indent=2)
            print(f"📝 Created default keywords file: {self.keywords_file}")
            return default_keywords
        
        try:
            with open(self.keywords_file, 'r') as f:
                keywords_data = json.load(f)
                print(f"✓ Loaded {len(keywords_data.get('keywords', []))} keywords from {self.keywords_file}\n")
                return keywords_data
        except json.JSONDecodeError:
            print(f"❌ Error reading {self.keywords_file}. Using default keywords.")
            return {"keywords": [], "case_sensitive": False}
    
    def get_my_channel_id(self):
        """Get the authenticated user's channel ID"""
        try:
            request = self.youtube.channels().list(
                part='id,snippet',
                mine=True
            )
            response = request.execute()
            
            if response['items']:
                self.my_channel_id = response['items'][0]['id']
                channel_name = response['items'][0]['snippet']['title']
                print(f"👤 Monitoring comments for: {channel_name}")
                print(f"   Channel ID: {self.my_channel_id}\n")
            else:
                print("❌ Could not retrieve your channel information.")
                exit(1)
        except HttpError as e:
            print(f"❌ Error fetching channel info: {e}")
            exit(1)
    
    def get_comment_thread_with_replies(self, video_id):
        """Get all comments from a video, including nested replies"""
        try:
            all_comments = []
            next_page_token = None
            
            while True:
                request = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token,
                    textFormat='plainText'
                )
                response = request.execute()
                
                for item in response['items']:
                    # Get top-level comment
                    top_comment = item['snippet']['topLevelComment']['snippet']
                    all_comments.append({
                        'comment_id': item['snippet']['topLevelComment']['id'],
                        'author': top_comment['authorDisplayName'],
                        'author_channel_id': top_comment.get('authorChannelId', {}).get('value', ''),
                        'text': top_comment['textDisplay'],
                        'published': top_comment['publishedAt'],
                        'parent_id': None,
                        'is_reply': False
                    })
                    
                    # Get replies if they exist
                    if 'replies' in item:
                        for reply_item in item['replies']['comments']:
                            reply = reply_item['snippet']
                            all_comments.append({
                                'comment_id': reply_item['id'],
                                'author': reply['authorDisplayName'],
                                'author_channel_id': reply.get('authorChannelId', {}).get('value', ''),
                                'text': reply['textDisplay'],
                                'published': reply['publishedAt'],
                                'parent_id': reply['parentId'],
                                'is_reply': True
                            })
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                
                time.sleep(0.3)
            
            return all_comments
        except HttpError as e:
            return []
    
    def find_replies_to_my_comments_in_thread(self, video_id):
        """Find all replies to the user's comments in a video thread"""
        all_comments = self.get_comment_thread_with_replies(video_id)
        
        # Find all comments made by the user
        my_comment_ids = set()
        for comment in all_comments:
            if comment['author_channel_id'] == self.my_channel_id:
                my_comment_ids.add(comment['comment_id'])
        
        # Find replies to user's comments
        replies_to_me = []
        for comment in all_comments:
            if comment['is_reply'] and comment['parent_id'] in my_comment_ids:
                # Find the parent comment
                parent_comment = next((c for c in all_comments if c['comment_id'] == comment['parent_id']), None)
                if parent_comment:
                    replies_to_me.append({
                        'reply': comment,
                        'my_comment': parent_comment
                    })
        
        return replies_to_me
    
    def get_my_comments(self, max_results=100):
        """Fetch the user's recent comments"""
        try:
            request = self.youtube.commentThreads().list(
                part='snippet',
                allThreadsRelatedToChannelId=self.my_channel_id,
                maxResults=min(max_results, 100),
                order='time',
                textFormat='plainText'
            )
            response = request.execute()
            
            my_comments = []
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                # Only include comments I made (not comments on my videos)
                if comment['authorChannelId']['value'] == self.my_channel_id:
                    my_comments.append({
                        'comment_id': item['snippet']['topLevelComment']['id'],
                        'thread_id': item['id'],
                        'video_id': comment['videoId'],
                        'text': comment['textDisplay'],
                        'published': comment['publishedAt'],
                        'video_owner_channel_id': comment.get('channelId', '')
                    })
            
            return my_comments
        except HttpError as e:
            print(f"❌ Error fetching your comments: {e}")
            return []
    
    def get_video_info(self, video_id):
        """Get video title and channel information"""
        try:
            request = self.youtube.videos().list(
                part='snippet',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]['snippet']
                return {
                    'title': video['title'],
                    'channel': video['channelTitle'],
                    'channel_id': video['channelId']
                }
            return None
        except HttpError as e:
            return None
    
    def get_replies_to_comment(self, comment_id):
        """Get all replies to a specific comment"""
        try:
            request = self.youtube.comments().list(
                part='snippet',
                parentId=comment_id,
                textFormat='plainText',
                maxResults=100
            )
            response = request.execute()
            
            replies = []
            for item in response['items']:
                reply = item['snippet']
                replies.append({
                    'author': reply['authorDisplayName'],
                    'text': reply['textDisplay'],
                    'published': reply['publishedAt'],
                    'likes': reply['likeCount']
                })
            
            return replies
        except HttpError as e:
            # Comment might not have replies or might be deleted
            return []
    
    def check_keywords_in_text(self, text):
        """Check if text contains any of the monitored keywords"""
        keywords = self.keywords.get('keywords', [])
        case_sensitive = self.keywords.get('case_sensitive', False)
        
        if not case_sensitive:
            text = text.lower()
            keywords = [k.lower() for k in keywords]
        
        found_keywords = []
        for keyword in keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def reply_to_comment(self, comment_id, reply_text):
        """Post a reply to a specific comment"""
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
            print(f"❌ Error posting reply: {e}")
            return False
    
    def format_time_ago(self, timestamp):
        """Convert ISO timestamp to human-readable time ago"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.now(dt.tzinfo)
            diff = now - dt
            
            if diff.days > 365:
                return f"{diff.days // 365} year(s) ago"
            elif diff.days > 30:
                return f"{diff.days // 30} month(s) ago"
            elif diff.days > 0:
                return f"{diff.days} day(s) ago"
            elif diff.seconds > 3600:
                return f"{diff.seconds // 3600} hour(s) ago"
            elif diff.seconds > 60:
                return f"{diff.seconds // 60} minute(s) ago"
            else:
                return "just now"
        except:
            return timestamp
    
    def monitor_replies(self, days_back=30, max_comments=50, include_reply_threads=True):
        """Main function to monitor replies and check for keywords"""
        print("=" * 80)
        print("🔍 Scanning for replies to your comments on OTHER people's videos...")
        print("=" * 80)
        print(f"\nKeywords monitoring: {', '.join(self.keywords.get('keywords', []))}")
        print(f"Looking back: {days_back} days")
        print(f"Max comments to check: {max_comments}")
        if include_reply_threads:
            print(f"Mode: Including replies to YOUR replies (full thread tracking)")
        else:
            print(f"Mode: Top-level comments only")
        print()
        
        # Get user's recent comments
        print("📥 Fetching your recent comments...")
        my_comments = self.get_my_comments(max_results=max_comments)
        print(f"   Found {len(my_comments)} of your comments\n")
        
        if not my_comments:
            print("❌ No comments found.")
            return
        
        # Filter for comments on other people's videos only
        print("🔍 Filtering for comments on OTHER people's videos...")
        others_videos_comments = []
        video_ids_to_check = set()
        
        for comment in my_comments:
            video_info = self.get_video_info(comment['video_id'])
            if video_info and video_info['channel_id'] != self.my_channel_id:
                comment['video_info'] = video_info
                others_videos_comments.append(comment)
                video_ids_to_check.add(comment['video_id'])
                time.sleep(0.1)  # Small delay to respect rate limits
        
        print(f"   Found {len(others_videos_comments)} comments on other people's videos")
        print(f"   Across {len(video_ids_to_check)} different videos\n")
        
        if not others_videos_comments:
            print("ℹ️  You haven't commented on other people's videos recently.")
            return
        
        # Check each comment for replies with keywords
        print("=" * 80)
        print("📬 Checking for replies with matching keywords...")
        print("=" * 80)
        
        matches_found = 0
        total_replies = 0
        match_details = []  # Store match details for summary
        
        if include_reply_threads:
            # New method: Get all comments from each video and find replies to user's comments
            print("\n🔄 Using deep thread scanning (this may take longer)...\n")
            
            processed_videos = set()
            for idx, comment in enumerate(others_videos_comments, 1):
                video_id = comment['video_id']
                
                # Skip if we already processed this video
                if video_id in processed_videos:
                    continue
                processed_videos.add(video_id)
                
                print(f"[Video {len(processed_videos)}/{len(video_ids_to_check)}] Scanning entire thread:")
                print(f"    Video: {comment['video_info']['title'][:60]}...")
                print(f"    Channel: {comment['video_info']['channel']}")
                
                # Get all replies to user's comments in this video (including nested)
                replies_to_me = self.find_replies_to_my_comments_in_thread(video_id)
                total_replies += len(replies_to_me)
                
                if replies_to_me:
                    print(f"    Found {len(replies_to_me)} replies to your comments in this thread")
                    
                    # Check each reply for keywords
                    for reply_data in replies_to_me:
                        reply = reply_data['reply']
                        my_comment = reply_data['my_comment']
                        
                        found_keywords = self.check_keywords_in_text(reply['text'])
                        
                        if found_keywords:
                            matches_found += 1
                            
                            # Determine if user's comment was a reply itself
                            comment_type = "reply" if my_comment['is_reply'] else "comment"
                            
                            # Store for summary
                            match_details.append({
                                'video_title': comment['video_info']['title'],
                                'channel': comment['video_info']['channel'],
                                'video_url': f"https://youtube.com/watch?v={video_id}",
                                'your_comment': my_comment['text'],
                                'your_comment_type': comment_type,
                                'reply_author': reply['author'],
                                'reply_text': reply['text'],
                                'reply_time': self.format_time_ago(reply['published']),
                                'reply_likes': 0,  # Not available in this API response
                                'keywords': found_keywords,
                                'comment_id': reply['comment_id']
                            })
                            
                            print("\n    " + "🎯 KEYWORD MATCH FOUND! " + "=" * 50)
                            print(f"    📍 VIDEO: {comment['video_info']['title']}")
                            print(f"    📺 CHANNEL: {comment['video_info']['channel']}")
                            print(f"    🔗 LINK: https://youtube.com/watch?v={video_id}")
                            print()
                            print(f"    💬 YOUR ORIGINAL {comment_type.upper()}:")
                            print(f"       \"{my_comment['text'][:150]}{'...' if len(my_comment['text']) > 150 else ''}\"")
                            print()
                            print(f"    ↳ 💭 REPLY FROM: {reply['author']}")
                            print(f"       ⏰ {self.format_time_ago(reply['published'])}")
                            print(f"       🔑 Keywords found: {', '.join(found_keywords)}")
                            print(f"       📝 Reply text:")
                            print(f"       \"{reply['text']}\"")
                            print("    " + "=" * 70)
                else:
                    print(f"    No replies found")
                
                # Delay between videos
                time.sleep(0.5)
        else:
            # Original method: Only check direct replies to top-level comments
            for idx, comment in enumerate(others_videos_comments, 1):
                print(f"\n[{idx}/{len(others_videos_comments)}] Checking comment on:")
                print(f"    Video: {comment['video_info']['title'][:60]}...")
                print(f"    Channel: {comment['video_info']['channel']}")
                
                # Get replies to this comment
                replies = self.get_replies_to_comment(comment['comment_id'])
                total_replies += len(replies)
                
                if replies:
                    print(f"    Replies: {len(replies)}")
                    
                    # Check each reply for keywords
                    for reply in replies:
                        found_keywords = self.check_keywords_in_text(reply['text'])
                        
                        if found_keywords:
                            matches_found += 1
                            
                            # Store for summary
                            match_details.append({
                                'video_title': comment['video_info']['title'],
                                'channel': comment['video_info']['channel'],
                                'video_url': f"https://youtube.com/watch?v={comment['video_id']}",
                                'your_comment': comment['text'],
                                'your_comment_type': 'comment',
                                'reply_author': reply['author'],
                                'reply_text': reply['text'],
                                'reply_time': self.format_time_ago(reply['published']),
                                'reply_likes': reply['likes'],
                                'keywords': found_keywords,
                                'comment_id': comment['comment_id']
                            })
                            
                            print("\n    " + "🎯 KEYWORD MATCH FOUND! " + "=" * 50)
                            print(f"    📍 VIDEO: {comment['video_info']['title']}")
                            print(f"    📺 CHANNEL: {comment['video_info']['channel']}")
                            print(f"    🔗 LINK: https://youtube.com/watch?v={comment['video_id']}")
                            print()
                            print(f"    💬 YOUR ORIGINAL COMMENT:")
                            print(f"       \"{comment['text'][:150]}{'...' if len(comment['text']) > 150 else ''}\"")
                            print()
                            print(f"    ↳ 💭 REPLY FROM: {reply['author']}")
                            print(f"       ⏰ {self.format_time_ago(reply['published'])}")
                            print(f"       👍 {reply['likes']} likes")
                            print(f"       🔑 Keywords found: {', '.join(found_keywords)}")
                            print(f"       📝 Reply text:")
                            print(f"       \"{reply['text']}\"")
                            print("    " + "=" * 70)
                else:
                    print(f"    Replies: 0")
                
                # Small delay between API calls
                if idx < len(others_videos_comments):
                    time.sleep(0.5)
        
        # Summary
        print("\n" + "=" * 80)
        print("✓ SCAN COMPLETE")
        print("=" * 80)
        print(f"Comments checked: {len(others_videos_comments)}")
        print(f"Total replies found: {total_replies}")
        print(f"Replies matching keywords: {matches_found}")
        print("=" * 80)
        
        # Detailed summary of all matches
        if match_details:
            print("\n" + "=" * 80)
            print("📋 SUMMARY OF ALL MATCHES")
            print("=" * 80)
            
            for i, match in enumerate(match_details, 1):
                print(f"\n{'─' * 80}")
                print(f"MATCH #{i}")
                print(f"{'─' * 80}")
                print(f"📺 Video: {match['video_title']}")
                print(f"🎬 Channel: {match['channel']}")
                print(f"🔗 URL: {match['video_url']}")
                print()
                print(f"💬 Your original {match['your_comment_type']}:")
                print(f"   \"{match['your_comment'][:200]}{'...' if len(match['your_comment']) > 200 else ''}\"")
                print()
                print(f"💭 {match['reply_author']} replied ({match['reply_time']}")
                if match.get('reply_likes', 0) > 0:
                    print(f"   👍 {match['reply_likes']} likes")
                print(f"   \"{match['reply_text']}\"")
                print()
                print(f"🔑 Matched keywords: {', '.join(match['keywords'])}")
            
            print("\n" + "=" * 80)
            print(f"Total matches found: {len(match_details)}")
            print("=" * 80)
            
            # Interactive reply option
            print("\n" + "=" * 80)
            print("💬 INTERACTIVE REPLY MODE")
            print("=" * 80)
            reply_mode = input("\nWould you like to reply to any of these? (yes/no): ").strip().lower()
            
            if reply_mode in ['yes', 'y']:
                while True:
                    try:
                        match_num = input(f"\nWhich match # would you like to reply to? (1-{len(match_details)}, or 'done' to finish): ").strip()
                        
                        if match_num.lower() in ['done', 'exit', 'quit', 'q']:
                            print("\n✓ Exiting reply mode")
                            break
                        
                        match_idx = int(match_num) - 1
                        
                        if 0 <= match_idx < len(match_details):
                            selected_match = match_details[match_idx]
                            
                            print("\n" + "─" * 80)
                            print(f"Replying to Match #{match_num}")
                            print("─" * 80)
                            print(f"Video: {selected_match['video_title']}")
                            print(f"Their comment: \"{selected_match['reply_text']}\"")
                            print()
                            
                            reply_text = input("Your reply (or 'cancel' to skip): ").strip()
                            
                            if reply_text.lower() in ['cancel', 'skip']:
                                print("Skipped.")
                                continue
                            
                            if reply_text:
                                print(f"\n📤 Posting reply...")
                                if self.reply_to_comment(selected_match['comment_id'], reply_text):
                                    print(f"✅ Successfully posted reply!")
                                    print(f"🔗 View at: {selected_match['video_url']}")
                                else:
                                    print(f"❌ Failed to post reply")
                            else:
                                print("Empty reply, skipped.")
                        else:
                            print(f"Invalid match number. Please enter 1-{len(match_details)}")
                    
                    except ValueError:
                        print("Please enter a valid number or 'done'")
                    except KeyboardInterrupt:
                        print("\n\n✓ Exiting reply mode")
                        break
    
    def export_results(self, output_file='reply_monitor_results.json'):
        """Export monitoring results to JSON file"""
        # This could be enhanced to save results for tracking over time
        pass


def main():
    print("=" * 80)
    print("YouTube Comment Reply Monitor with Keyword Matching")
    print("=" * 80)
    print("\nThis tool monitors replies to YOUR comments on OTHER people's videos")
    print("and alerts you when specific keywords are mentioned.\n")
    
    # Initialize monitor
    monitor = YouTubeReplyMonitor()
    
    # Get user preferences
    try:
        days_back = int(input("How many days back to search? [default: 30]: ").strip() or "30")
    except ValueError:
        days_back = 30
    
    try:
        max_comments = int(input("Maximum comments to check? [default: 50]: ").strip() or "50")
    except ValueError:
        max_comments = 50
    
    # Ask about thread scanning mode
    print("\n🔄 Thread Scanning Mode:")
    print("   [1] Standard - Only find replies to your top-level comments (faster)")
    print("   [2] Deep Scan - Find replies to ALL your comments including your replies (slower, more thorough)")
    mode_choice = input("Choose mode [1 or 2, default: 2]: ").strip() or "2"
    include_reply_threads = (mode_choice == "2")
    
    print()
    
    # Run the monitor
    monitor.monitor_replies(days_back=days_back, max_comments=max_comments, include_reply_threads=include_reply_threads)
    
    print("\n💡 TIP: Edit 'keywords.json' to customize the keywords you're monitoring!")


if __name__ == '__main__':
    main()
