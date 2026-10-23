"""90-day content calendar for FrontDesk Flows + Xenova Solutions (23 Oct 2026 - 20 Jan 2027).

Output: social/calendar/calendar-90d.json and .csv. One row per content piece.
Feed weeks run Friday->Thursday from 30 Oct; 23-29 Oct rows are the already-queued posts (social/posts/2026-10-23.json).
Each feed line: industry | audience | topic | tool/service | format | hook | cta (blank = brand default).
Weekly feed rhythm: Fri offer, Sat carousel, Sun poll, Mon mistakes/tip, Tue comparison, Wed demo/BTS, Thu checklist.
Sample projects and concept demos must be labelled on-screen. Never invent results, clients or testimonials.
"""
import csv, datetime as dt, json, os

START, FIRST_WEEK, END = dt.date(2026, 10, 23), dt.date(2026, 10, 30), dt.date(2027, 1, 20)
HERE = os.path.dirname(os.path.abspath(__file__))

CTA = {
    "frontdesk": {"default": "DM REVIEW for a free workflow review", "poll": "Vote, and tell us your setup in the comments",
                  "offer": "Book a free workflow review (link in bio)", "save": "Save this and send it to whoever runs ops"},
    "xenova": {"default": "Book a free 30-minute scoping call: xenovasolutions.com/contact", "poll": "Vote, and comment the tool you use today",
               "offer": "Discuss your project: xenovasolutions.com/contact", "save": "Save this for your next planning meeting"},
}
FEED_PLAT = {"frontdesk": "Instagram + Facebook", "xenova": "Instagram + Facebook + LinkedIn"}
VIDEO_PLAT = "Instagram Reel + Facebook Reel + YouTube Short"

FD = """
# W1 30 Oct-5 Nov
Clothing e-commerce|Shopify fashion store owners|Returns requests that run themselves: form, label, refund status|Make.com + Shopify + email|Offer post|Returns season is coming. Is your inbox ready?|offer
Footwear|Online shoe brands|Size exchange flow: offer a swap before a refund|n8n + Shopify + WhatsApp|Carousel|Wrong size should not mean a lost sale.|save
Cross-industry|Small business owners|Which question eats most of your support time?|-|Poll|Where is my order? Can I return it? Do you have my size?|poll
E-commerce|Store owners using automations|Mistake: automations with no failure alert|Any automation tool|Carousel (mistakes)|Your automation failed at 2am. Who found out?|
Healthcare|Clinic managers|Make.com vs n8n for appointment reminders|Make.com vs n8n|Comparison carousel|Same reminder, two tools. Which one fits your clinic?|
Fintech|Fintech ops teams|Chasing missing KYC documents automatically (sample data)|n8n + webhooks + email|Demo walkthrough (concept demo)|Missing documents stall onboarding. Chase them automatically.|
Retail / e-commerce|Store owners|7 things to automate before Black Friday|Shopify + Make.com|Checklist carousel|Black Friday is 4 weeks away. Fix these 7 first.|save
# W2 6-12 Nov
Restaurants|Restaurant owners|Booking confirmations and no-show reminders without a booking app upgrade|Make.com + Google Calendar + SMS|Offer post|Empty tables cost more than a reminder.|offer
Clothing|Fashion brands|Low-stock alerts that reach the right person before a sell-out|n8n + Shopify + Slack|Carousel|You found out it sold out from a customer email.|save
Cross-industry|Owners|Which tool do you automate with today?|Zapier / Make / n8n / none|Poll|Zapier, Make, n8n or copy-paste?|poll
Healthcare|Clinic admins|Mistake: reminders that ignore cancellations|n8n|Carousel (mistakes)|We reminded a patient about an appointment they cancelled.|
E-commerce|Growing stores|Zapier vs Make.com for order-to-CRM sync|Zapier vs Make.com|Comparison carousel|Order comes in. CRM stays empty. Which tool fixes it cheaper?|
Footwear|Shoe retailers|Order status updates on WhatsApp, step by step (sample store)|n8n + WhatsApp Cloud API|Demo walkthrough (sample store)|Five order updates, zero manual messages.|
Tech / SaaS|SaaS founders|Trial-to-paid follow-up checklist|HubSpot free CRM + Make.com|Checklist carousel|Your trial users go quiet on day 3. Here is why.|save
# W3 13-19 Nov
Real estate|Letting agents|Viewing requests routed and confirmed in minutes|GoHighLevel|Offer post|A viewing request at 9pm should not wait till Monday.|offer
E-commerce|Store owners|Abandoned checkout follow-up that does not feel like spam|Shopify + Klaviyo free tier + Make.com|Carousel|Three emails. Not seven.|save
Cross-industry|Owners|How fast do you reply to a new enquiry?|-|Poll|Under 5 minutes, same day, next day, or when we can?|poll
Fintech|Lending / payments ops|Mistake: webhooks with no retry or signature check|Webhooks + n8n|Carousel (mistakes)|A webhook is a door. Do you lock it?|
Agencies|Small agencies|GoHighLevel vs custom n8n for client lead follow-up|GHL vs n8n|Comparison carousel|All-in-one or build your own? Depends on these 4 things.|
Clothing|Fashion brands|Pre-order flow: capture, confirm, notify on arrival (sample store)|Shopify + Make.com + email|Demo walkthrough (sample store)|Sold out is not the end of the sale.|
Healthcare|Clinics|Patient intake form to records: what to check before you automate|Forms + n8n + data minimisation|Checklist carousel|Before patient data moves, answer these 6 questions.|save
# W4 20-26 Nov
E-commerce|Store owners|Black Friday order surge: support automations that hold up|Shopify + helpdesk + Make.com|Offer post|Your order volume doubles. Your team does not.|offer
Footwear|Shoe brands|Returns reason tracking that tells you which size chart is wrong|Make.com + Google Sheets|Carousel|Your returns data is telling you something.|save
Cross-industry|Owners|Biggest Black Friday headache?|-|Poll|Stock, shipping, support or returns?|poll
E-commerce|Store owners|Mistake: discount code automations with no usage cap|Shopify + Make.com|Carousel (mistakes)|One leaked code, 400 orders.|
Retail|Multi-channel sellers|Inventory sync: native integrations vs Make.com vs custom API|Shopify / marketplaces / APIs|Comparison carousel|Two channels, one stock count. Who keeps it right?|
Fintech|Payments teams|Failed-payment recovery flow (sample data)|Stripe webhooks + n8n + email|Demo walkthrough (concept demo)|A failed card is not a lost customer yet.|
E-commerce|Store owners|Black Friday week ops checklist|Shopify + helpdesk|Checklist carousel|Print this before Friday.|save
# W5 27 Nov-3 Dec
E-commerce|Store owners|Cyber Monday: auto-tag VIP and first-time buyers for follow-up|Shopify + CRM + Make.com|Offer post|You got 300 new customers. Now what?|offer
Clothing|Fashion brands|Post-purchase flow: care tips, review ask, size feedback|Klaviyo free tier + Make.com|Carousel|The sale is the start of the relationship.|save
Cross-industry|Owners|Which CRM do you use?|HubSpot / Zoho / GHL / spreadsheet|Poll|HubSpot, Zoho, GoHighLevel or a spreadsheet?|poll
Healthcare|Clinics|Mistake: sending patient details to AI tools without redaction|n8n + AI|Carousel (mistakes)|Before an AI reads it, remove what it does not need.|
Tech / SaaS|SaaS support teams|Zapier vs n8n for support ticket routing|Zapier vs n8n|Comparison carousel|Ticket routing: pay per task or self-host?|
E-commerce|Store owners|Delivery exception alerts: courier delay to customer message (sample store)|Courier API + Make.com|Demo walkthrough (sample store)|Tell them before they ask.|
Restaurants|Restaurant owners|December bookings checklist: deposits, reminders, waitlist|Booking tool + Make.com|Checklist carousel|Party season bookings, without the chaos.|save
# W6 4-10 Dec
Professional services|Accountants and law firms|Client onboarding: documents, e-sign, reminders|Make.com + e-sign + email|Offer post|New client signed. 14 emails later they are onboarded.|offer
Fintech|Fintech founders|Onboarding funnel: where applicants drop off and what to automate|CRM + webhooks|Carousel|Most applicants leave at the same step.|save
Cross-industry|Owners|How many apps hold your customer data?|1-2 / 3-5 / 6+ / no idea|Poll|Be honest. How many?|poll
E-commerce|Store owners|Mistake: automating a broken process|Any tool|Carousel (mistakes)|Automation makes a messy process fail faster.|
Healthcare|Clinics|GoHighLevel vs Make.com for patient follow-ups|GHL vs Make.com|Comparison carousel|Clinic follow-ups: platform or workflow tool?|
Clothing|Fashion brands|Wholesale order intake from email to order sheet (sample data)|n8n + Gmail + Google Sheets|Demo walkthrough (concept demo)|Wholesale orders still arrive as email attachments.|
Cross-industry|Owners|Is it time to automate? 6 signs|Workflow review|Checklist carousel|If 3 of these are true, it is time.|save
# W7 11-17 Dec
E-commerce|Store owners|Christmas cut-off date messages that update themselves|Shopify + Make.com|Offer post|Last order date for Christmas: automatic, everywhere.|offer
Footwear|Shoe brands|Gift receipts and January exchange prep|Shopify + Make.com|Carousel|January exchanges start now.|save
Cross-industry|Owners|What would you automate first in 2027?|-|Poll|Support, sales follow-up, invoicing or stock?|poll
Fintech|Ops teams|Mistake: no audit trail on automated decisions|n8n + logging|Carousel (mistakes)|If you cannot show why it happened, regulators will ask.|
Agencies|Agencies and freelancers|Self-hosted n8n vs n8n Cloud vs Make.com: running costs|n8n / Make.com|Comparison carousel|Cheapest is not always cheapest.|
Healthcare|Clinics|Recall reminders for check-ups (sample clinic)|n8n + calendar + SMS|Demo walkthrough (sample clinic)|Patients forget. Systems do not have to.|
Retail|Store owners|Year-end automation audit checklist|Workflow review|Checklist carousel|Before you add new automations, check the old ones.|save
# W8 18-24 Dec
Cross-industry|Small businesses|Holiday auto-replies that still route urgent messages|Email + Make.com|Offer post|Closed for the holidays does not mean ignore everyone.|offer
E-commerce|Store owners|Review requests after delivery, not after dispatch|Shopify + courier API + Make.com|Carousel|Asking for a review before the parcel arrives? Ouch.|save
Cross-industry|Owners|Do you work over the holidays?|-|Poll|Fully off, checking messages, or full speed?|poll
E-commerce|Store owners|Mistake: one person owns every automation login|Any tool|Carousel (mistakes)|What happens when they are on holiday?|
Tech / SaaS|Startups|Make.com vs custom API integration: when to switch|Make.com vs custom code|Comparison carousel|When your Make bill looks like a salary, read this.|
Restaurants|Restaurants|Waitlist to table-ready SMS flow (sample data)|Make.com + SMS|Demo walkthrough (concept demo)|Your table is ready. Sent by a workflow.|
Cross-industry|Owners|Holiday shutdown checklist for your automations|Workflow review|Checklist carousel|Before you switch off, check these 5 things.|save
# W9 25-31 Dec
E-commerce|Store owners|January returns rush: returns portal plus automatic status updates|Shopify + Make.com|Offer post|The returns rush starts on the 26th.|offer
Clothing|Fashion brands|Turning returns into exchanges with store credit|Shopify + Make.com|Carousel|Keep the revenue. Offer the swap.|save
Cross-industry|Owners|Biggest time-waster this year?|-|Poll|Copy-paste, chasing payments, answering FAQs or scheduling?|poll
Healthcare|Clinics|Mistake: one reminder channel for every patient|SMS / email / WhatsApp|Carousel (mistakes)|Not every patient reads email.|
E-commerce|Store owners|Shopify Flow vs Make.com for store automations|Shopify Flow vs Make.com|Comparison carousel|Free inside Shopify, or flexible outside it?|
Fintech|Fintech support|Support triage: payment issues to the right queue (sample data)|n8n + helpdesk + AI classifier|Demo walkthrough (concept demo)|A failed payment ticket should never wait behind a password reset.|
Cross-industry|Owners|2027 automation plan in one page|Workflow review|Checklist carousel|Plan the year in 20 minutes.|save
# W10 1-7 Jan
Cross-industry|Small businesses|New year workflow review offer|Workflow review|Offer post|Start 2027 with fewer manual steps.|offer
Real estate|Agents|Lead follow-up sequence for portal enquiries|GoHighLevel / Make.com + CRM|Carousel|Portal leads go cold in hours, not days.|save
Cross-industry|Owners|Which goal matters most this quarter?|More leads, faster support, fewer errors, less admin|Poll|Pick one. Just one.|poll
E-commerce|Store owners|Mistake: too many automation tools for one job|Zapier + Make + n8n|Carousel (mistakes)|Three tools, one workflow, no idea which one broke.|
Professional services|Firms|Zapier vs Make.com for document and e-sign workflows|Zapier vs Make.com|Comparison carousel|Paperwork automation: which tool is easier to maintain?|
Footwear|Shoe brands|Back-in-stock notifications by size (sample store)|Shopify + Make.com + email|Demo walkthrough (sample store)|Size 9 is back. Tell only the people who asked.|
Healthcare|Clinics|January waitlist and cancellation fill checklist|Calendar + SMS|Checklist carousel|Cancellations happen. Empty slots do not have to.|save
# W11 8-14 Jan
Fintech|Fintech ops|Customer onboarding status updates without support tickets|Webhooks + email/SMS|Offer post|Where is my application? Answer it before they ask.|offer
Tech / SaaS|SaaS teams|Churn-risk alerts from usage data|Product analytics + CRM + Make.com|Carousel|They stopped logging in 9 days ago. Did anyone notice?|save
Cross-industry|Owners|Would you trust AI to reply to customers?|Yes / with approval / FAQs only / no|Poll|Honest answers only.|poll
E-commerce|Store owners|Mistake: no test orders before switching an automation on|Shopify + any tool|Carousel (mistakes)|Test with a real order. Not with hope.|
Agencies|Agencies|GHL snapshots vs building workflows per client|GoHighLevel|Comparison carousel|Reusable or custom? The maintenance bill decides.|
Clothing|Fashion brands|Influencer gifting tracker: request to dispatch to post (sample data)|Make.com + Google Sheets + Shopify|Demo walkthrough (concept demo)|You sent 40 gifts. How many posted?|
Cross-industry|Owners|Automation handover checklist for your team|Documentation|Checklist carousel|If only one person understands it, it is a risk.|save
# W12 15-20 Jan
Healthcare|Clinics|Treatment-plan follow-ups that bring patients back|n8n + CRM + SMS|Offer post|Booked once, never returned. Why?|offer
E-commerce|Store owners|Customer service macros plus automation: a hybrid approach|Helpdesk + Make.com|Carousel|Not everything needs AI. Some things need a good template.|save
Cross-industry|Owners|What stops you automating?|Cost, time, trust, do not know where to start|Poll|What is really in the way?|poll
Fintech|Fintech teams|Mistake: storing API keys inside workflows|n8n / Make.com credentials|Carousel (mistakes)|Your API key is in a screenshot somewhere.|
Restaurants|Restaurants|Make.com vs Zapier for reservation and review flows|Make.com vs Zapier|Comparison carousel|Small restaurant, small budget. Which tool?|
Cross-industry|Owners|90-day recap: the workflows we showed and what to try first|Workflow review|Carousel recap|12 weeks of workflows in one post.|save
"""

XN = """
# W1 30 Oct-5 Nov
E-commerce|Shopify brands|Custom Shopify app or integration when apps do not fit|Shopify app development|Offer post|You have 14 apps and still export to Excel.|offer
Fintech|Fintech founders|Identixa: how we built KYC (OCR, face match, AML screening)|Identity verification platform (our product)|Case carousel (our project)|What goes into a KYC check, step by step.|
Cross-industry|Business owners|Website, app or automation: what do you need next?|-|Poll|If you could fix one thing next quarter?|poll
Cross-industry|SMEs|Practical tip: write the spec before you get quotes|Discovery and scoping|Tip carousel|Three quotes, three different projects. Here is why.|save
Cross-industry|SMEs|Off-the-shelf SaaS vs custom software: cost over 3 years|Custom software|Comparison carousel|The cheap option is not cheap at year three.|
Tech|Founders|Behind the scenes: how we test before a release|QA and software testing|BTS carousel|What we check before anything goes live.|
Cross-industry|SMEs|Signs your website is costing you leads|Website development|Checklist carousel|If your site does 3 of these, it is losing enquiries.|save
# W2 6-12 Nov
Healthcare|Independent clinics|Clinic website with online booking and an AI assistant (demo site)|Website + AI assistant|Offer post|Patients book at 11pm. Can they?|offer
E-commerce|Online stores|AI product description generator we built for an e-commerce client|AI integration|Case carousel (our project)|Hundreds of products, one tone of voice.|
Cross-industry|Owners|Where does your team lose most time?|Reporting, data entry, support, approvals|Poll|Pick the biggest drain.|poll
Cross-industry|SMEs|Practical tip: measure page speed on mobile, not desktop|Performance optimisation|Tip carousel|Your site is fast on your laptop. Your customers use phones.|save
E-commerce|Store owners|Shopify vs WooCommerce vs headless: which fits your stage?|E-commerce development|Comparison carousel|Platform choice decides your next 3 years.|
Tech|Founders|How we scope an MVP in one call|SaaS / MVP development|BTS carousel|The 6 questions we ask before writing code.|
Cross-industry|SMEs|Signs you have outgrown spreadsheets|Custom internal tools|Checklist carousel|Your spreadsheet has a spreadsheet to explain it.|save
# W3 13-19 Nov
Cross-industry|SMEs|Customer portal: let clients see status, files and invoices|Web application development|Offer post|How many emails are just "any update?"|offer
Transport|Bus operators|BookKaru: Urdu voice booking agent we built|Voice AI agent (our project)|Case carousel (our project)|A booking line that understands Roman Urdu.|
Cross-industry|Owners|Mobile app or mobile website?|-|Poll|Do your customers need an app?|poll
Cross-industry|SMEs|Practical tip: keep a human check on AI replies at first|AI chatbots|Tip carousel|Launch with a safety net.|save
Cross-industry|SMEs|Native app vs cross-platform (Flutter/React Native) vs PWA|Mobile app development|Comparison carousel|Three ways to get on a phone. Very different costs.|
Tech|Teams|How we run maintenance: updates, backups, monitoring|Maintenance and support|BTS carousel|Most site outages are predictable.|
Fintech|Fintech startups|Checklist before you build a fintech MVP|Fintech product development|Checklist carousel|KYC, audit trail, permissions: settle these first.|save
# W4 20-26 Nov
E-commerce|Store owners|Black Friday readiness review: speed, checkout, tracking|E-commerce performance|Offer post|Your store will get its busiest week. Will it hold?|offer
Real estate / marketplaces|Founders|Loinix: building a UK marketplace on Django + Next.js|Marketplace development (our project)|Case carousel (our project)|Two-sided marketplaces have two sets of problems.|
Cross-industry|Owners|Biggest website frustration?|Slow, hard to update, no leads, looks dated|Poll|Be honest about your site.|poll
E-commerce|Store owners|Practical tip: test checkout on a real phone every week in November|QA|Tip carousel|One broken button in Black Friday week.|save
Cross-industry|SMEs|Chatbot vs AI agent vs human support: which tickets go where|AI agents|Comparison carousel|Not every question deserves the same answer path.|
Tech|Teams|How we load-test before a traffic spike|Performance testing|BTS carousel|We break it before your customers do.|
E-commerce|Store owners|Black Friday tech checklist|E-commerce maintenance|Checklist carousel|Print this. Tick it off. Sleep better.|save
# W5 27 Nov-3 Dec
Cross-industry|SMEs|CRM implementation that your team actually uses|CRM implementation|Offer post|You bought a CRM. Your team still uses WhatsApp.|offer
HR|HR teams|ZavHR: the HR management system we built|HRMS / internal software (our project)|Case carousel (our project)|Leave, payroll inputs, attendance: one place.|
Cross-industry|Owners|How do you track customers today?|CRM, spreadsheet, email, memory|Poll|Where do your customer notes live?|poll
Cross-industry|SMEs|Practical tip: define 5 CRM fields before importing anything|CRM implementation|Tip carousel|Messy import, messy CRM forever.|save
Cross-industry|SMEs|HubSpot vs Zoho vs custom CRM|CRM implementation|Comparison carousel|Which CRM fits a 10-person team?|
Tech|Teams|BTS: how we design dashboards people open|UI/UX + dashboards|BTS carousel|A dashboard nobody opens is just decoration.|
Cross-industry|SMEs|Signs you need an internal dashboard|Web app / dashboards|Checklist carousel|Monday reporting takes half a day?|save
# W6 4-10 Dec
Cross-industry|SMEs|Document Q&A (RAG) for your team's files|RAG / AI integration|Offer post|Your answers are in 400 PDFs. Ask them.|offer
Cross-industry|Teams|RAG document Q&A system we built for a client in Finland|RAG (our project)|Case carousel (our project)|How an AI finds the right paragraph, not a guess.|
Cross-industry|Owners|Would you use AI on internal documents?|Yes, maybe, not yet, never|Poll|Policies, contracts, manuals. Would you?|poll
Cross-industry|SMEs|Practical tip: clean your documents before AI reads them|RAG|Tip carousel|Old versions confuse AI too.|save
Cross-industry|SMEs|RAG vs fine-tuning: which one do you need?|AI integration|Comparison carousel|Most businesses need the cheaper one.|
Tech|Teams|BTS: how we evaluate AI answers before launch|AI testing|BTS carousel|We grade the AI before your customers do.|
Cross-industry|SMEs|AI readiness checklist|AI consulting|Checklist carousel|Before you buy AI, check these 7 things.|save
# W7 11-17 Dec
Cross-industry|SMEs|UI/UX refresh for an existing app|UI/UX design|Offer post|Users are not confused. Your interface is.|offer
Fintech|Fintech teams|Identity checks in your product: API plus review dashboard|Identixa (our project)|Case carousel (our project)|Automate the check, keep humans on the edge cases.|
Cross-industry|Owners|What would you rebuild if budget allowed?|Website, app, internal tool, nothing|Poll|One thing. Go.|poll
Cross-industry|SMEs|Practical tip: 5 UX fixes that cost almost nothing|UI/UX|Tip carousel|Small changes, fewer support emails.|save
Cross-industry|SMEs|Website builder vs WordPress vs custom build|Website development|Comparison carousel|What you save now, you might pay later.|
Tech|Teams|BTS: our code review checklist|Software quality|BTS carousel|Every change gets a second pair of eyes.|
Cross-industry|SMEs|Year-end tech audit checklist|Maintenance|Checklist carousel|Licences, backups, access, renewals.|save
# W8 18-24 Dec
Cross-industry|SMEs|Maintenance and support plans: what is included|Maintenance|Offer post|Who fixes it on the 27th of December?|offer
E-commerce|E-commerce|Connecting store, inventory, CRM and support in one flow|Systems integration|Carousel|Four systems, one customer record.|save
Cross-industry|Owners|Biggest tech win this year?|-|Poll|Share yours in the comments.|poll
Cross-industry|SMEs|Practical tip: keep an access list of every system|Security basics|Tip carousel|Who still has access from 2024?|save
Cross-industry|SMEs|In-house developer vs agency vs freelancer|Software development|Comparison carousel|Who should build it? Depends on these 4 things.|
Tech|Teams|BTS: how we hand over a project|Delivery process|BTS carousel|Docs, access, training. Not just code.|
Cross-industry|SMEs|Security basics checklist for small teams|Security / maintenance|Checklist carousel|Five things you can do this week.|save
# W9 25-31 Dec
Cross-industry|SMEs|Planning a 2027 software project: free scoping call|Discovery|Offer post|Plan it now, build it in Q1.|offer
Cross-industry|Teams|What a good project brief contains (template)|Discovery|Carousel|One page that saves weeks.|save
Cross-industry|Owners|What is on your 2027 tech list?|Website, app, AI, automation|Poll|What are you building next year?|poll
Cross-industry|SMEs|Practical tip: budget for maintenance, not just the build|Maintenance|Tip carousel|Software is never finished.|save
Cross-industry|SMEs|Fixed price vs time and materials|Software development|Comparison carousel|Which contract fits your project?|
Tech|Teams|BTS: a week of sprint at Xenova|Delivery process|BTS carousel|Plan, build, review, ship.|
Cross-industry|SMEs|Project kickoff checklist|Discovery|Checklist carousel|Before kickoff, have these ready.|save
# W10 1-7 Jan
Cross-industry|SMEs|AI agent pilot: one job, done well|AI agents|Offer post|Start with one agent and one clear task.|offer
Healthcare|Clinics|Demo clinic website: booking plus AI assistant walkthrough|Website + AI (demo site)|Case carousel (demo)|A demo we built for a fictional clinic.|
Cross-industry|Owners|Would you try an AI voice receptionist?|Yes, maybe, no, already do|Poll|Would you let AI pick up the phone?|poll
Cross-industry|SMEs|Practical tip: track 3 numbers after launch|Analytics|Tip carousel|Launch day is not the finish line.|save
Cross-industry|SMEs|Voice agent vs chatbot vs call answering service|Voice AI|Comparison carousel|Phone, chat or a person?|
Tech|Teams|BTS: how we keep AI agents inside their limits|AI safety / guardrails|BTS carousel|What an agent is not allowed to do.|
Cross-industry|SMEs|Signs your app needs performance work|Performance optimisation|Checklist carousel|Slow is a feature nobody asked for.|save
# W11 8-14 Jan
Fintech|Fintech startups|Fintech onboarding flow: KYC, status updates, support|Fintech development|Offer post|Onboarding is your first product experience.|offer
SaaS|SaaS founders|From MVP to v2: what to rebuild and what to keep|SaaS development|Carousel|Not everything in your MVP needs rewriting.|save
Cross-industry|Owners|Do you test before every release?|Always, sometimes, rarely, what testing?|Poll|No judgement. Mostly.|poll
Cross-industry|SMEs|Practical tip: automated tests for your 5 most important flows|Software testing|Tip carousel|Test the money paths first.|save
Cross-industry|SMEs|Manual QA vs automated testing|Software testing|Comparison carousel|Which bugs each one catches.|
Tech|Teams|BTS: our Playwright test suite in action|Automated testing|BTS carousel|Robots clicking every button, every release.|
SaaS|Founders|SaaS launch checklist|SaaS development|Checklist carousel|Billing, onboarding, support, monitoring.|save
# W12 15-20 Jan
Cross-industry|SMEs|Website + automation bundle: enquiries straight into your CRM|Website + CRM integration|Offer post|Your contact form should do more than send an email.|offer
Cross-industry|SMEs|Answer engine optimisation: getting recommended by AI search|AEO / SEO|Carousel|Customers now ask AI who to hire.|save
Cross-industry|Owners|Where do your customers find you?|Google, AI search, social, referrals|Poll|Where did your last customer come from?|poll
Cross-industry|SMEs|Practical tip: answer real customer questions on your site|AEO / content|Tip carousel|AI search quotes clear answers.|save
Cross-industry|SMEs|SEO vs AEO: what changes, what does not|AEO / SEO|Comparison carousel|It is still SEO. With a twist.|
Cross-industry|SMEs|90-day recap: what we covered and how to pick your next project|All services|Carousel recap|12 weeks, one decision guide.|save
"""

FD_VIDEO = [  # Tue, Thu, Sat; concept/sample demos are labelled on screen
    ("Clothing e-commerce", "Returns request to refund status in Make.com (sample store)", "Make.com + Shopify", "Watch a return go from form to refund status with no inbox."),
    ("Footwear", "Size exchange offered before refund (sample store)", "n8n + Shopify", "Swap, do not refund: the flow in 30 seconds."),
    ("Retail", "Black Friday stock alert to Slack", "n8n + Shopify + Slack", "This alert fires before you sell out."),
    ("Restaurants", "Booking confirmation and reminder flow", "Make.com + Google Calendar", "Two messages that cut no-shows."),
    ("E-commerce", "Order to CRM: Zapier vs Make.com side by side", "Zapier vs Make.com", "Same job, two tools, watch both run."),
    ("Footwear", "WhatsApp order updates (sample store)", "n8n + WhatsApp Cloud API", "Five order updates. Zero typing."),
    ("Real estate", "Viewing request routed and confirmed", "GoHighLevel", "A 9pm enquiry, answered at 9pm."),
    ("E-commerce", "Abandoned checkout: 3-message flow", "Shopify + Make.com", "Three messages, not seven."),
    ("Fintech", "Signed webhook with retries (concept demo)", "n8n + webhooks", "Watch a bad webhook get rejected."),
    ("E-commerce", "Black Friday support triage", "Helpdesk + Make.com", "500 tickets, sorted before your team logs in."),
    ("Footwear", "Returns reasons into a size-chart report", "Make.com + Google Sheets", "Your returns explain your size chart."),
    ("Fintech", "Failed payment recovery (concept demo)", "Stripe webhooks + n8n", "A failed card, recovered automatically."),
    ("E-commerce", "Tag VIP and first-time buyers", "Shopify + Make.com", "300 new customers, sorted in seconds."),
    ("Healthcare", "Redact patient data before AI (sample clinic)", "n8n + AI", "What the AI never sees."),
    ("E-commerce", "Courier delay to proactive customer message", "Courier API + Make.com", "Tell them before they ask."),
    ("Professional services", "Client onboarding: docs, e-sign, reminders", "Make.com + e-sign", "From signed to onboarded without chasing."),
    ("Fintech", "Onboarding drop-off nudge (concept demo)", "CRM + webhooks", "Stuck at step 3? Here is the nudge."),
    ("Clothing", "Wholesale email to order sheet (concept demo)", "n8n + Gmail + Sheets", "Attachments in, clean order rows out."),
    ("E-commerce", "Christmas cut-off banner and auto-replies", "Shopify + Make.com", "One date, updated everywhere."),
    ("Healthcare", "Recall reminders (sample clinic)", "n8n + SMS", "Six-month check-up, booked by a workflow."),
    ("Agencies", "n8n self-hosted vs Make.com: same flow, cost walk-through", "n8n vs Make.com", "Count the operations with us."),
    ("Cross-industry", "Holiday auto-reply that still escalates urgent messages", "Email + Make.com", "Closed, but not unreachable."),
    ("E-commerce", "Review request after delivery confirmed", "Courier API + Make.com", "Ask after it arrives."),
    ("Restaurants", "Waitlist to table-ready SMS (concept demo)", "Make.com + SMS", "Your table is ready, sent by a workflow."),
    ("Clothing", "Return to exchange with store credit", "Shopify + Make.com", "Keep the revenue."),
    ("E-commerce", "Shopify Flow vs Make.com: same task", "Shopify Flow vs Make.com", "Free inside Shopify or flexible outside it?"),
    ("Fintech", "Payment ticket triage with AI classifier (concept demo)", "n8n + AI", "The payment ticket jumps the queue."),
    ("Real estate", "Portal lead follow-up sequence", "GoHighLevel / Make.com", "Portal leads, followed up in minutes."),
    ("Footwear", "Back-in-stock by size (sample store)", "Shopify + Make.com", "Size 9 is back. Only size-9 fans hear."),
    ("Healthcare", "Cancellation fills from a waitlist (sample clinic)", "Calendar + SMS", "Cancelled at 8am, filled by 8:05."),
    ("Fintech", "Application status updates (concept demo)", "Webhooks + SMS", "Where is my application? Answered."),
    ("SaaS", "Churn-risk alert from usage data (concept demo)", "Analytics + CRM", "Nine days quiet. Alert sent."),
    ("Clothing", "Influencer gifting tracker (concept demo)", "Make.com + Sheets + Shopify", "40 gifts sent. Who posted?"),
    ("Healthcare", "Treatment-plan follow-up (sample clinic)", "n8n + CRM + SMS", "Booked once, back for session two."),
    ("Cross-industry", "Credentials done right: no keys in workflows", "n8n / Make.com credentials", "Where your API key should live."),
    ("Restaurants", "Review reply drafts with owner approval", "Make.com + AI + approval step", "AI drafts. You approve."),
]
XN_VIDEO = [  # Mon, Wed
    ("Fintech", "Identixa demo: document OCR and face match", "Identity verification (our project)", "A KYC check, start to finish."),
    ("E-commerce", "Store, inventory, CRM, support: one customer record (diagram)", "Systems integration", "Four systems. One customer."),
    ("Healthcare", "Demo clinic site: booking plus AI assistant", "Website + AI (demo site)", "Book at 11pm. Ask a question. Done."),
    ("Cross-industry", "Mobile speed test: before and after a fix (our site)", "Performance optimisation", "Watch the page load twice."),
    ("Transport", "BookKaru voice agent clip", "Voice AI (our project)", "A booking call in Roman Urdu."),
    ("Cross-industry", "Customer portal walkthrough (concept)", "Web application", "Status, files, invoices. No emails."),
    ("E-commerce", "Black Friday: 60-second store health check", "E-commerce performance", "Four checks before your busiest week."),
    ("Cross-industry", "Chatbot vs agent: same question, two outcomes", "AI agents", "One answers. One acts."),
    ("Cross-industry", "Dashboard that replaces Monday reporting (concept)", "Dashboards", "Half a day of reporting, gone."),
    ("Cross-industry", "CRM fields that matter: 5 to define", "CRM implementation", "Define these before importing anything."),
    ("Cross-industry", "Ask your PDFs: RAG demo (sample documents)", "RAG", "The answer, with the paragraph it came from."),
    ("Cross-industry", "How we grade AI answers before launch", "AI testing", "Pass, fail, or needs a human."),
    ("Cross-industry", "3 UX fixes on a real form (concept redesign)", "UI/UX", "Fewer fields, fewer drop-offs."),
    ("Fintech", "Identity check API plus review queue", "Identixa (our project)", "Automate the check. Review the edge cases."),
    ("Cross-industry", "Who still has access? 2-minute audit", "Security basics", "Remove old logins today."),
    ("Cross-industry", "Project handover: what you should receive", "Delivery process", "Code is not the whole handover."),
    ("Cross-industry", "One-page project brief walkthrough", "Discovery", "The page that saves weeks."),
    ("Cross-industry", "Fixed price vs time and materials in 45 seconds", "Software development", "Which contract fits?"),
    ("Cross-industry", "AI agent with guardrails: what it cannot do", "AI agents", "Limits are a feature."),
    ("Cross-industry", "Voice agent vs chatbot vs call service", "Voice AI", "Phone, chat or a person?"),
    ("Fintech", "Fintech onboarding flow walkthrough (concept)", "Fintech development", "Onboarding is your first product."),
    ("Cross-industry", "Playwright tests clicking through checkout", "Automated testing", "Robots test every release."),
    ("Cross-industry", "Contact form to CRM to follow-up", "Website + CRM integration", "Your form should do more than email you."),
    ("Cross-industry", "AEO: how AI search reads your page", "AEO / SEO", "Clear answers get quoted."),
]
LONG = [  # YouTube long-form, monthly per brand (needs each brand's own channel connected)
    ("frontdesk", dt.date(2026, 11, 14), "E-commerce", "Build a returns and exchange automation for a Shopify store (Make.com, full walkthrough, sample store)", "Make.com + Shopify"),
    ("frontdesk", dt.date(2026, 12, 12), "Cross-industry", "n8n vs Make.com vs Zapier vs GoHighLevel: one workflow built four ways", "Tool comparison"),
    ("frontdesk", dt.date(2027, 1, 9), "Fintech", "Onboarding document chase and status updates with webhooks (concept demo, sample data)", "n8n + webhooks"),
    ("xenova", dt.date(2026, 11, 21), "Fintech", "How a KYC flow works: inside Identixa (OCR, face match, AML)", "Identity verification"),
    ("xenova", dt.date(2026, 12, 19), "Cross-industry", "Website, custom software or automation? A decision guide for SMEs", "Discovery / consulting"),
    ("xenova", dt.date(2027, 1, 16), "Cross-industry", "Ask your documents: building a RAG Q&A system end to end (sample documents)", "RAG / AI integration"),
]


def parse(block):
    return [l.split("|") for l in block.strip().splitlines() if l and not l.startswith("#")]


def main():
    rows = []
    existing = json.load(open(os.path.join(HERE, "..", "posts", "2026-10-23.json")))
    for p in existing:  # already written, rendered and queued
        title = p["slides"][0].get("title", "").replace("\n", " ").replace("*", "")
        rows.append({"date": p["date"], "brand": p["brand"], "kind": "feed", "industry": "-", "audience": "-",
                     "topic": p["id"], "tool": "-", "format": p.get("pillar", "-"), "hook": title,
                     "platform": FEED_PLAT[p["brand"]], "cta": "-", "status": "queued (Make, 18:05 PKT)", "id": p["id"]})
    for brand, block in (("frontdesk", FD), ("xenova", XN)):
        lines = parse(block)
        for i, l in enumerate(lines):
            d = FIRST_WEEK + dt.timedelta(days=i)
            if d > END: break
            ind, aud, topic, tool, fmt, hook, cta = (l + [""] * 7)[:7]
            rows.append({"date": d.isoformat(), "brand": brand, "kind": "feed", "industry": ind, "audience": aud,
                         "topic": topic, "tool": tool, "format": fmt, "hook": hook, "platform": FEED_PLAT[brand],
                         "cta": CTA[brand].get(cta or "default", CTA[brand]["default"]), "status": "planned",
                         "id": f"{brand[0]}-{d:%m%d}"})
    for brand, vids, days in (("frontdesk", FD_VIDEO, (1, 3, 5)), ("xenova", XN_VIDEO, (0, 2))):
        d, k = FIRST_WEEK, 0
        while d <= END and k < len(vids):
            if d.weekday() in days:
                ind, topic, tool, hook = vids[k]
                rows.append({"date": d.isoformat(), "brand": brand, "kind": "short video", "industry": ind, "audience": "Owners and ops leads",
                             "topic": topic, "tool": tool, "format": "Reel / Short (30-60 s, screen recording + captions)",
                             "hook": hook, "platform": VIDEO_PLAT, "cta": CTA[brand]["default"], "status": "planned",
                             "id": f"{brand[0]}v-{d:%m%d}"})
                k += 1
            d += dt.timedelta(days=1)
    for brand, d, ind, topic, tool in LONG:
        rows.append({"date": d.isoformat(), "brand": brand, "kind": "long video", "industry": ind, "audience": "Owners and technical buyers",
                     "topic": topic, "tool": tool, "format": "YouTube video (10-15 min walkthrough)", "hook": topic.split(":")[0],
                     "platform": "YouTube", "cta": CTA[brand]["offer"], "status": "planned (needs brand channel)", "id": f"{brand[0]}l-{d:%m%d}"})
    d = dt.date(2026, 11, 1)
    while d <= END:  # YouTube Community poll mirrors the Sunday feed poll
        for brand in ("frontdesk", "xenova"):
            src = next((r for r in rows if r["date"] == d.isoformat() and r["brand"] == brand and r["kind"] == "feed"), None)
            if src:
                rows.append({**src, "kind": "community poll", "platform": "YouTube Community", "format": "Poll",
                             "status": "planned (needs brand channel)", "id": f"{brand[0]}c-{d:%m%d}"})
        d += dt.timedelta(days=7)
    rows.sort(key=lambda r: (r["date"], r["brand"], r["kind"]))
    json.dump(rows, open(os.path.join(HERE, "calendar-90d.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "calendar-90d.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(len(rows), Counter((r["brand"], r["kind"]) for r in rows), rows[-1]["date"])


if __name__ == "__main__":
    main()
