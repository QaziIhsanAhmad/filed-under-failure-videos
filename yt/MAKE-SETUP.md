# Free YouTube route: Make.com setup (about 10 minutes, once)

Why this route: Make's free plan has 1,000 credits/month, 2 active scenarios, a 15-minute minimum interval, 512 MB transfer and a 5 MB file limit. A daily Short is under 4.5 MB and uses about 2-3 credits a day. The 67 MB weekly episode is over the limit, so it is scheduled natively in YouTube Studio from a ready kit (yt/native/NNN.md), about 5 minutes a week. YouTube's own API is not used because uploads from unverified API projects stay private until a Google audit.

Budget: Reels scenario at once a day (~60 credits/month) + this scenario at once a day (~90) = ~150 of 1,000.

## A. Save credits on the Reels scenario (do this first)
1. Open "Integration RSS" > click the clock on the RSS module > Run scenario: "Every day", Time: 22:30. Save.

## B. Create the YouTube scenario
1. Scenarios > Create a new scenario.
2. Add RSS > "Watch RSS feed items". URL:
   https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/yt/feed.xml
   Maximum number of returned items: 3. OK. Choose where to start: "All RSS feed items" (the feed only ever contains today's item).
3. Add YouTube > "Upload a Video". Connection: Add, sign in with the Google account that owns Filed Under Failure, pick that channel.
   - Video source / File: choose URL (download from URL) and map the RSS item's URL.
   - Title: map Title. Description: map Description.
   - Privacy status: Unlisted for the first test run; change to Public after the test.
   - Made for kids: No. Category: Education (27), if offered.
4. Clock on the RSS module: "Every day", Time: 18:00. Save. Switch ON.
5. Test now: click "Run once". It should upload the 6-second clip "Upload test - delete me" as Unlisted. Check YouTube Studio > Content, then delete the test video.
6. Change Privacy status to Public. Save. Send Claude a screenshot of the scenario's History.

From then on: each day at 12:00 PKT GitHub releases that day's Short into the feed; Make uploads it publicly at 18:00 PKT; GitHub records the live link hourly in yt/published.json.
