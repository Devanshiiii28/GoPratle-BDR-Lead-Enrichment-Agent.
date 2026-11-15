# Assignment requirement mapping

| Recruiter requirement | Included in this no-API MVP | Constraint |
|---|---|---|
| Company + city trigger | App form | Not a Google Sheets event trigger |
| Find Founder/HR/Events lead online | Google and LinkedIn search links | Human must research; no autonomous web lookup |
| Pull profile/contact information | Manual fields | Must be source-verified by operator |
| Tailored 3-line GoPratle pitch | Rule-based contextual template | No LLM/API |
| Log back into Sheet | CSV database + CSV export | Import into Sheets manually |
| Outreach message | Email draft | Human sends after review |
| Schedule follow-up | Follow-up date + due queue | No background scheduler |
| Detect reply / automate follow-up | Status can be manually updated | Reply detection requires Gmail integration |
| Workflow JSON / agent config / GitHub | app.py + README + this mapping | Custom script implementation |
