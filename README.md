# GoPratle BDR Lead Enrichment & Outreach Agent — No-API MVP

## Included functionality
- Company + city trigger in the app.
- Search links to Google and LinkedIn for manual public-source research.
- Manual capture of a verified Founder / HR / Events / Partnerships contact.
- Rule-based, context-personalized three-line GoPratle pitch.
- Outreach email draft (review/copy manually; never auto-sent).
- Local CSV lead database.
- Status management (New, Researching, Draft, Contacted, Replied, etc.).
- Follow-up date queue and due counter.
- CSV and JSON export for handoff to Google Sheets.

## Important limitations
No API keys are used. Therefore this app cannot autonomously search the web, scrape or verify profile/contact details, receive a Google Sheets trigger, send email, monitor replies, or run background scheduled follow-ups. It creates search links and requires human research. Do not present manually entered data as verified unless you checked the source.

## Windows setup
Open this folder in VS Code → Terminal → New Terminal:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Demo
1. Add company `Zomato`, city `Gurugram`.
2. Open the Google/LinkedIn research links.
3. Manually enter a contact only if verified; otherwise leave fields blank.
4. Add research notes and source URLs.
5. Generate the pitch and save the lead.
6. Show the database, change status to Contacted, and show follow-up tracker.
7. Export CSV and import it into Google Sheets (File → Import → Upload).
8. Show the generated outreach draft, but use a test inbox and send manually only after review.

## Suggested screen-recording narrative
"This is a no-API custom-script MVP. A company and city initiate the lead workflow. The app provides research entry points, captures a source-backed decision-maker, generates a GoPratle-specific pitch, logs the record locally, and tracks follow-up status. CSV export supports a Google Sheets handoff. Live enrichment, automatic email delivery and reply monitoring are intentionally not claimed in this no-API version."
