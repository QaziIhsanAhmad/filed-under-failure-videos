# Free YouTube route: Make.com setup and test (about 10 minutes, once)

How timing works: GitHub releases each day's Short into the feed at 12:00 PKT. The Make scenario runs once a day at 21:00 PKT and uploads whatever is in the feed with Privacy = Public, so the Short goes public at about 21:00 PKT (the same slot Metricool uses now). Nothing depends on a scheduled-publish field. On Saturdays the feed also holds the episode if the large-file test passes.

Make free plan (make.com/pricing): 1,000 credits/month, 2 active scenarios, 15-minute minimum interval, 512 MB data transfer, 5 MB max file size. Expected use: about 2 credits per daily run (1 to check the feed, 1 per upload): roughly 60-70/month for this scenario and about 30-60 for Reels once it runs daily. Confirm the real numbers in each scenario's History after the test.

## A. Reels scenario: cut credit use (1 minute)
"Integration RSS" > clock icon on the RSS module > Run scenario: Every day, at 22:30 > OK > Save.

## B. New YouTube scenario
1. Scenarios > Create a new scenario.
2. Add RSS > Watch RSS feed items. URL: https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/yt/feed.xml . Maximum number of returned items: 3. Choose where to start: All RSS feed items.
3. Add YouTube > Upload a Video. Connection: Add > sign in with the Google account that owns Filed Under Failure > choose that channel.
   - File / video source: the option to upload from a URL; map the RSS item URL.
   - Title = Title; Description = Description; Privacy status = Unlisted (tests only); Made for kids = No; Category = Education if offered.
4. Save (do not switch ON yet).

## C. Tests (after 12:41 PKT today, when both test clips are in the feed)
1. Click Run once. Two uploads are attempted:
   - "Upload test - delete me" (0.1 MB, a Short) proves URL upload works.
   - "Upload test 2 large file - delete me" (62 MB, episode-sized) shows whether Make's 5 MB limit blocks episodes.
2. YouTube Studio > Content: check which test videos arrived, then delete them.
3. Screenshot the scenario History (it shows credits used and any error) and send it to Claude.

## D. Go live
1. Upload a Video > Privacy status = Public. 2. RSS clock > Every day at 21:00. 3. Save and switch ON.
Real Shorts start with the Theranos week (Sat 17 Oct). Earlier days are already scheduled in Metricool and are never put in this feed.
