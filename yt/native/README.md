# Weekly episode in YouTube Studio (about 5 minutes, only while Make cannot carry large files)

Each Saturday's episode has a kit file yt/native/NNN.md with the links and text. Steps:
1. Open the kit file on GitHub. Click the video link and download the .mp4; download the thumbnail .png.
2. studio.youtube.com > Create > Upload videos > select the .mp4.
3. Details: paste Title and Description from the kit. Thumbnail: Upload file > the .png. Playlist: none. Audience: "No, it's not made for kids".
4. Show more: Altered content = the answer in the kit (assessed per video). Tags: paste the tag line. Category: Education. Language: English (United Kingdom). Captions: Upload file > the .srt link in the kit (optional).
5. Next > Next (checks) > Visibility: Schedule > date = the Saturday, time = 9:00 PM (Pakistan time) > Schedule.
6. Reply "scheduled" to Claude (the nightly monitor also checks the channel page afterwards).

Ways to remove this step (free): if the Make large-file test passes, episodes go through Make too. Otherwise the only free fully automatic route is YouTube's own API, which needs a Google Cloud project and a Google compliance audit before uploads can be public; that is optional and slow.
