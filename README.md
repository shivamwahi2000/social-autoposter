# Social Media Auto-Poster

Posts daily to **LinkedIn** and **Instagram** using AI-generated content. Runs free on GitHub Actions.

## How it works

```
GitHub Actions (daily 9 AM UTC)
  → Picks a random topic from config/topics.json
  → Fetches a relevant article from RSS feeds
  → Gemini Flash generates:
       • LinkedIn post  (professional, ~200 words)
       • Instagram caption (casual, emojis + hashtags)
  → Unsplash provides a relevant image for Instagram
  → Posts to both platforms via their APIs
```

---

## One-time setup (30 minutes)

### 1. Get a Gemini API key (free)

1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API key**
3. Copy the key

---

### 2. LinkedIn API setup

1. Go to https://developer.linkedin.com → **Create App**
2. Under **Products**, request **Share on LinkedIn** and **Sign In with LinkedIn**
3. Under **Auth**, add `https://www.linkedin.com/developers/tools/oauth/redirect` as a redirect URI
4. Use the OAuth 2.0 token generator to generate an access token with scopes:
   - `w_member_social` (personal profile posting)
   - `w_organization_social` (page posting — only if you manage a LinkedIn Page)
5. Copy your **Access Token**
6. If posting to a LinkedIn Page (not personal profile): find your **Organization ID** from the page URL (`linkedin.com/company/<ID>`)

> LinkedIn access tokens expire after **60 days**. You'll need to refresh them periodically.

---

### 3. Instagram (Meta Graph API) setup

**Requirements:** Instagram Business or Creator account linked to a Facebook Page.

1. Go to https://developers.facebook.com → **Create App** → choose **Business**
2. Add **Instagram Graph API** product
3. Under **Instagram Graph API > Getting Started**, connect your Instagram account
4. Generate a **User Access Token** with these permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
5. Get your **Instagram User ID**:
   ```
   GET https://graph.facebook.com/v19.0/me/accounts?access_token=YOUR_TOKEN
   ```
   Then:
   ```
   GET https://graph.facebook.com/v19.0/{page-id}?fields=instagram_business_account&access_token=YOUR_TOKEN
   ```
6. Copy the `instagram_business_account.id` — that is your `INSTAGRAM_USER_ID`

> Long-lived tokens last **60 days**. Use the token refresh endpoint to extend them.

---

### 4. Unsplash API key (free)

1. Go to https://unsplash.com/developers → **New Application**
2. Copy the **Access Key**
3. Free tier: 50 requests/hour (plenty for 1 post/day)

---

### 5. GitHub repository setup

1. Push this folder to a new GitHub repository
2. Go to **Settings → Secrets and variables → Actions**
3. Add these repository secrets:

| Secret | Value |
|---|---|
| `GEMINI_API_KEY` | Your Gemini API key |
| `LINKEDIN_ACCESS_TOKEN` | LinkedIn OAuth token |
| `LINKEDIN_ORG_ID` | LinkedIn Page org ID (optional — omit for personal profile) |
| `INSTAGRAM_ACCESS_TOKEN` | Instagram Graph API token |
| `INSTAGRAM_USER_ID` | Instagram Business account ID |
| `UNSPLASH_ACCESS_KEY` | Unsplash access key |

4. Go to **Actions** tab → enable workflows if prompted
5. To test immediately: go to **Actions → Daily Social Media Post → Run workflow**

---

## Local testing

```bash
cd social-autoposter
cp .env.example .env
# Fill in your keys in .env

pip install -r requirements.txt

# Load env vars and run
export $(cat .env | xargs)
cd src && python main.py
```

---

## Customization

### Change topics or RSS feeds

Edit [config/topics.json](config/topics.json) — add/remove topics and RSS feed URLs.

### Change posting time

Edit the cron schedule in [.github/workflows/daily_post.yml](.github/workflows/daily_post.yml):
```yaml
- cron: '30 3 * * *'   # 9:00 AM IST
- cron: '0 14 * * *'   # 9:00 AM EST
```

Use https://crontab.guru to find your UTC offset.

### Post to only one platform

Simply don't add the secrets for the platform you want to skip — the script detects missing credentials and skips gracefully.

---

## Project structure

```
social-autoposter/
├── .github/
│   └── workflows/
│       └── daily_post.yml       # GitHub Actions cron job
├── src/
│   ├── main.py                  # Entry point
│   ├── content_generator.py     # Gemini Flash — generates posts
│   ├── rss_fetcher.py           # Pulls articles from RSS feeds
│   ├── image_fetcher.py         # Fetches images from Unsplash
│   ├── linkedin_poster.py       # LinkedIn API
│   └── instagram_poster.py      # Meta Graph API
├── config/
│   └── topics.json              # Topics and RSS feeds to pull from
├── requirements.txt
├── .env.example
└── README.md
```
