/**
 * Filed Under Failure – YouTube Analytics export (free: Google Apps Script, runs in the channel owner's own Google account).
 * Writes the last 28 days per video (views, watch time, average view %, subscribers, impressions, CTR where YouTube
 * provides them) to the Google Sheet "FUF YouTube Analytics", shared read-only with kaziehsan111@gmail.com so the
 * scheduled tasks can read it. Runs daily at about 06:00 Pakistan time.
 *
 * One-time setup (signed in as the channel owner, xenovasolutionsofficial@gmail.com):
 *   1. script.google.com > New project > paste this file.
 *   2. Left sidebar "Services" (+) > add "YouTube Analytics API" and "YouTube Data API v3".
 *   3. Select function "setup" > Run > allow access.
 */
var SHEET_NAME = 'FUF YouTube Analytics';
var SHARE_WITH = 'kaziehsan111@gmail.com';

function setup() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('exportAnalytics').timeBased().everyDays(1).atHour(6).inTimezone('Asia/Karachi').create();
  exportAnalytics();
}

function sheet_() {
  var files = DriveApp.getFilesByName(SHEET_NAME);
  var ss = files.hasNext() ? SpreadsheetApp.open(files.next()) : SpreadsheetApp.create(SHEET_NAME);
  try { ss.addViewer(SHARE_WITH); } catch (e) {}
  return ss;
}

function query_(metrics, dims, start, end, extra) {
  var opt = { ids: 'channel==MINE', startDate: start, endDate: end, metrics: metrics };
  if (dims) opt.dimensions = dims;
  for (var k in (extra || {})) opt[k] = extra[k];
  return YouTubeAnalytics.Reports.query(opt);
}

function write_(ss, name, report, note) {
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clear();
  sh.getRange(1, 1).setValue('updated ' + new Date().toISOString() + (note ? ' | ' + note : ''));
  if (!report || !report.columnHeaders) return;
  var head = report.columnHeaders.map(function (h) { return h.name; });
  var rows = report.rows || [];
  sh.getRange(2, 1, 1, head.length).setValues([head]);
  if (rows.length) sh.getRange(3, 1, rows.length, head.length).setValues(rows);
}

function exportAnalytics() {
  var ss = sheet_();
  var tz = 'UTC', end = Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd');
  var start = Utilities.formatDate(new Date(Date.now() - 28 * 864e5), tz, 'yyyy-MM-dd');
  var base = 'views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares';
  write_(ss, 'videos_28d', query_(base, 'video', start, end, { sort: '-views', maxResults: 200 }));
  write_(ss, 'daily_28d', query_(base, 'day', start, end, { sort: 'day' }));
  write_(ss, 'country_28d', query_('views,estimatedMinutesWatched,averageViewPercentage,subscribersGained', 'country', start, end, { sort: '-views', maxResults: 25 }));
  write_(ss, 'traffic_28d', query_('views,estimatedMinutesWatched', 'insightTrafficSourceType', start, end, { sort: '-views' }));
  // Thumbnail impressions and click-through rate (only reported by YouTube for some videos/dates).
  try {
    write_(ss, 'impressions_28d', query_('videoThumbnailImpressions,videoThumbnailImpressionsClickRate', 'video', start, end, { sort: '-videoThumbnailImpressions', maxResults: 200 }));
  } catch (e) {
    write_(ss, 'impressions_28d', null, 'not available from the API: ' + e.message);
  }
  // Video titles for readability.
  var ids = (ss.getSheetByName('videos_28d').getRange('A3:A').getValues() || []).map(function (r) { return r[0]; }).filter(String);
  var titles = [['videoId', 'title', 'publishedAt']];
  for (var i = 0; i < ids.length; i += 50) {
    var res = YouTube.Videos.list('snippet', { id: ids.slice(i, i + 50).join(',') });
    (res.items || []).forEach(function (v) { titles.push([v.id, v.snippet.title, v.snippet.publishedAt]); });
  }
  var sh = ss.getSheetByName('titles') || ss.insertSheet('titles');
  sh.clear(); sh.getRange(1, 1, titles.length, 3).setValues(titles);
}
