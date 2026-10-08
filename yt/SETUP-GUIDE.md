# Filed Under Failure: free YouTube publishing, final setup guide
All times are Pakistan time (PKT). Everything here is free: Make.com free plan, GitHub Actions on a public repo, YouTube Studio.

## How it works
1. Each day's Short is listed in yt/ledger.json. At 12:00 PKT a GitHub job puts it into the production feed (9 hours before upload, so a late GitHub run cannot make it miss the slot; an item stays in the feed until a result is recorded).
2. At 21:00 PKT your Make scenario reads the feed and uploads the video to YouTube as Public.
3. Make immediately reports the result to GitHub (video ID and upload status, or the error). GitHub records it in the ledger.
4. Every hour GitHub also checks the public channel page and records live video IDs. A video missing from the page is "unverified", never "failed".
5. If Make reported an error, or reported nothing by 23:30, GitHub checks the channel twice. Only if the video is still not there does it re-release it under a new ID ("<id>-r1"), so Make's "already seen" memory cannot silently skip a failed upload. After 2 retries it stops and asks you.
Old posts already scheduled in Metricool (8 to 16 Oct) are never put in this feed.

Feeds:
- TEST feed (test clips only): https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/yt/test-feed.xml
- PRODUCTION feed: https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/yt/feed.xml

Make free plan limits: 1,000 credits/month, 2 active scenarios, 5 MB max file size, 5-minute max run time, 512 MB transfer. Expected use: about 3 credits per day for this scenario (feed check, upload, report) plus about 1 per day for Reels: roughly 120 per month.

## Step 1. GitHub token for result reports (3 minutes)
github.com > profile picture > Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token.
- Name: make-youtube-results. Expiration: 1 year.
- Repository access: Only select repositories > QaziIhsanAhmad/filed-under-failure-videos.
- Permissions > Repository permissions > Contents: Read and write. Nothing else.
- Generate, copy the token. Paste it only into Make (Step 3). Never send it in chat.

## Step 2. Reels scenario: once a day (1 minute)
Make > "Integration RSS" > clock icon on the RSS module > Run scenario: Every day, 22:30 > OK > Save.
Make > profile > Profile > Time zone: Asia/Karachi (so all scenario times are PKT).

## Step 3. Build the YouTube scenario (8 minutes)
Scenarios > Create a new scenario. Name it "FUF YouTube uploads".
Module 1. RSS > Watch RSS feed items
- URL: the TEST feed URL above (for now). Maximum number of returned items: 3. When asked where to start: All RSS feed items.
Module 2. YouTube > Upload a Video
- Connection: Add > sign in with the Google account that owns Filed Under Failure > allow.
- Video: choose the option to upload from a URL and map module 1 "URL".
- Title: map module 1 "Title". Description: map module 1 "Description".
- Privacy status: Unlisted (test only). Made for kids: No. Category: Education if offered.
Module 3. HTTP > Make a request (success report)
- URL: https://api.github.com/repos/QaziIhsanAhmad/filed-under-failure-videos/dispatches
- Method: POST. Headers: Authorization = Bearer <your token>; Accept = application/vnd.github+json
- Body type: Raw, Content type: JSON. Request content (map the items in curly brackets by clicking them):
  {"event_type":"yt-uploaded","client_payload":{"guid":"{{1.id}}","videoId":"{{2.id}}","uploadStatus":"{{2.status.uploadStatus}}","privacy":"{{2.status.privacyStatus}}"}}
  (1.id = module 1 "id"/guid; 2.id = module 2 video ID; status fields from module 2 output.)
Error handler (failure report): right-click module 2 > Add error handler > HTTP > Make a request, same URL, method and headers, request content:
  {"event_type":"yt-failed","client_payload":{"guid":"{{1.id}}","error":"{{error.message}}"}}
  then after it add the "Ignore" directive (so one failure does not stop the scenario).
Save. Do not switch it on yet.

## Step 4. Test (2 minutes) and cleanup
1. Click Run once. It processes the two test clips: "Upload test - delete me" (0.1 MB) and "Upload test 2 large file - delete me" (62 MB, episode-sized).
2. Results arrive in GitHub automatically (yt/tests.json). Claude reads them: success, video ID, upload status, or the exact error (e.g. the 5 MB limit or the 5-minute run limit).
3. YouTube Studio > Content: delete both test videos. Tell Claude "test deleted"; Claude then empties the test feed.

## Step 5. Go live (1 minute, only after Claude confirms the test passed)
1. Module 1 URL: change to the PRODUCTION feed. Where to start: All RSS feed items (the production feed only ever holds due items).
2. Module 2 Privacy status: Public.
3. Clock on module 1: Every day, 21:00. Save. Switch ON.
First real uploads start with the Theranos week (Sat 17 Oct).

## Weekly episode (only while the large-file test fails): YouTube Studio, about 5 minutes
Claude sends a kit link each week (yt/native/NNN.md) with the files and text.
1. Download the .mp4 and thumbnail .png from the kit links.
2. studio.youtube.com > Create > Upload videos > select the .mp4.
3. Paste Title and Description. Thumbnail: Upload file. Audience: No, it's not made for kids.
4. Show more: Altered content: use the answer in the kit (each video is assessed against YouTube's rules; ours normally do not need disclosure because they use a generic synthetic narrator, original graphics and original music, with no real person shown saying anything and no realistic invented scenes). Tags: paste. Category: Education. Captions: upload the .srt from the kit.
5. Next > Next > Visibility: Schedule > the Saturday, 9:00 PM > Schedule. Reply "scheduled".
Free way to remove this: if the large-file test passes, episodes go through Make like the Shorts.

## Recovery
- A Short did not appear: nothing to do; GitHub reconciles and re-releases it once it confirms it is missing. Claude asks you only if it gives up after 2 retries.
- Make turned the scenario off after errors: open it, check History, switch it back on.
- Token expired (yearly): create a new one (Step 1) and replace it in both HTTP modules.
- Credits low: Make > Organization > Usage; expected about 120/month of 1,000.
- To pause publishing: switch the scenario off. Nothing is lost; items wait in the feed.
