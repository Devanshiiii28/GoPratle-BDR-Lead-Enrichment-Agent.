import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, date, timedelta
import uuid
import urllib.parse

st.set_page_config(page_title="GoPratle BDR Agent", page_icon="🤝", layout="wide")
DATA = Path("data")
DATA.mkdir(exist_ok=True)
DB = DATA / "leads.csv"

COLS = ["id","created_at","company","city","decision_maker","designation","linkedin_url",
        "business_email","research_notes","source_urls","pitch","outreach_message",
        "follow_up_date","status","last_action"]

def load():
    if DB.exists():
        df = pd.read_csv(DB, dtype=str).fillna("")
        for c in COLS:
            if c not in df.columns: df[c] = ""
        return df[COLS]
    return pd.DataFrame(columns=COLS)

def save(df):
    df[COLS].to_csv(DB, index=False)

def pitch_for(company, city, person, notes):
    hello = f"Hi {person}," if person else "Hi there,"
    context = notes.strip() if notes.strip() else f"I came across {company} in {city} and wanted to introduce a potential event-support partner."
    return (f"{hello} GoPratle connects event hosts with vetted planners, DJs, and professional event crew.\n"
            f"{context} We can help simplify the process of finding reliable event talent and vendors.\n"
            "Would you be open to a short conversation to explore whether GoPratle could support your upcoming events?")

def email_for(person, company, pitch):
    greeting = f"Hi {person}," if person else "Hi there,"
    body = "\n".join(pitch.splitlines()[1:])
    return f"Subject: Event support partnership for {company}\n\n{greeting}\n\n{body}\n\nBest,\nGoPratle Team"

def search_links(company, city):
    q = urllib.parse.quote_plus(f'"{company}" "{city}" founder OR HR OR events OR partnerships')
    return {
        "Google search": f"https://www.google.com/search?q={q}",
        "LinkedIn people search": f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote_plus(company+' '+city+' events HR founder')}",
        "Company search": f"https://www.google.com/search?q={urllib.parse.quote_plus(company+' '+city+' official website')}"
    }

df = load()
st.title("🤝 GoPratle BDR Lead Enrichment & Outreach Agent")
st.caption("No-API custom-script MVP | Local CSV database | Human-reviewed outreach")

with st.sidebar:
    st.header("Workflow")
    st.markdown("1. Add company + city\n2. Open research links\n3. Enter verified lead details\n4. Generate tailored pitch\n5. Save to lead log\n6. Track outreach and follow-up")
    st.caption("No external API keys are used. Research/contact details must be verified manually.")

# Dashboard
today = date.today()
def due_count(frame):
    n = 0
    for _, r in frame.iterrows():
        try:
            if r["follow_up_date"] and date.fromisoformat(r["follow_up_date"]) <= today and r["status"] not in ["Replied","Closed","Not interested"]:
                n += 1
        except ValueError: pass
    return n

st.subheader("Lead pipeline")
a,b,c,d = st.columns(4)
a.metric("Total leads", len(df))
b.metric("New / research", int((df["status"]=="New").sum()) if len(df) else 0)
c.metric("Contacted", int((df["status"]=="Contacted").sum()) if len(df) else 0)
d.metric("Follow-ups due", due_count(df))

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add & enrich lead", "📋 Lead database", "⏰ Follow-up tracker", "📦 Export"])

with tab1:
    st.subheader("1. Trigger: company name + city")
    with st.form("new_lead"):
        x,y = st.columns(2)
        company = x.text_input("Company name *", placeholder="Zomato")
        city = y.text_input("City *", placeholder="Gurugram")
        submitted = st.form_submit_button("Start lead research", type="primary")
    if submitted:
        if not company.strip() or not city.strip():
            st.error("Company name and city are required.")
        else:
            st.session_state["research_company"] = company.strip()
            st.session_state["research_city"] = city.strip()
            st.success("Research task created. Use the search links below to verify a relevant contact.")

    comp = st.session_state.get("research_company","")
    cty = st.session_state.get("research_city","")
    if comp and cty:
        st.markdown("### 2. Research decision-maker")
        st.warning("Open these search links, verify a Founder / HR / Events / Partnerships lead, then enter only information you can substantiate. This no-API build does not scrape websites or invent contacts.")
        for label,url in search_links(comp,cty).items():
            st.markdown(f"- [{label}]({url})")
        with st.form("enrich"):
            person = st.text_input("Decision-maker name (if verified)")
            designation = st.text_input("Designation")
            linkedin = st.text_input("Public LinkedIn profile URL")
            email = st.text_input("Public business email (only if verified)")
            notes = st.text_area("Research notes / relevant event context", placeholder="Record the source-backed reason this person/company may be relevant.")
            sources = st.text_area("Source URLs (one per line)")
            generate = st.form_submit_button("Generate pitch & save lead", type="primary")
        if generate:
            pitch = pitch_for(comp,cty,person,notes)
            message = email_for(person,comp,pitch)
            new = {
                "id":str(uuid.uuid4())[:8], "created_at":datetime.now().isoformat(timespec="seconds"),
                "company":comp,"city":cty,"decision_maker":person,"designation":designation,
                "linkedin_url":linkedin,"business_email":email,"research_notes":notes,
                "source_urls":sources,"pitch":pitch,"outreach_message":message,
                "follow_up_date":(today+timedelta(days=2)).isoformat(),
                "status":"Draft - review required","last_action":"Lead researched and draft created"
            }
            df = pd.concat([df,pd.DataFrame([new])],ignore_index=True)
            save(df)
            st.session_state["last_created"] = new
            st.success("Lead logged in the local database.")
    if "last_created" in st.session_state:
        r=st.session_state["last_created"]
        st.markdown("### 3. Generated GoPratle pitch")
        st.info(r["pitch"])
        st.markdown("### Outreach draft (not sent)")
        st.code(r["outreach_message"])
        st.caption(f"Suggested follow-up: {r['follow_up_date']}")

with tab2:
    st.subheader("Lead database")
    if len(df):
        st.dataframe(df[["company","city","decision_maker","designation","business_email","status","follow_up_date"]],use_container_width=True,hide_index=True)
        chosen = st.selectbox("Select lead to update", df["id"].tolist(), format_func=lambda i: f"{df.loc[df.id==i,'company'].iloc[0]} — {i}")
        row = df[df.id==chosen].iloc[0]
        st.write(f"**{row['company']} — {row['city']}**")
        status_options=["New","Researching","Draft - review required","Contacted","Replied","Not interested","Closed"]
        current=row["status"] if row["status"] in status_options else "Draft - review required"
        new_status=st.selectbox("Update status",status_options,index=status_options.index(current))
        action=st.text_input("Last action / note",value=row["last_action"])
        new_follow=st.date_input("Follow-up date",value=date.fromisoformat(row["follow_up_date"]) if row["follow_up_date"] else today+timedelta(days=2))
        if st.button("Save lead update"):
            df.loc[df.id==chosen,"status"]=new_status
            df.loc[df.id==chosen,"last_action"]=action
            df.loc[df.id==chosen,"follow_up_date"]=new_follow.isoformat()
            save(df); st.success("Lead updated."); st.rerun()
    else: st.info("No leads yet. Add a company in the first tab.")

with tab3:
    st.subheader("Follow-up tracker")
    if len(df):
        rows=[]
        for _,r in df.iterrows():
            try: due=bool(r["follow_up_date"]) and date.fromisoformat(r["follow_up_date"]) <= today and r["status"] not in ["Replied","Closed","Not interested"]
            except ValueError: due=False
            if due: rows.append(r)
        if rows:
            st.dataframe(pd.DataFrame(rows)[["company","city","decision_maker","business_email","follow_up_date","status"]],use_container_width=True,hide_index=True)
            st.warning("These follow-ups are due. Review the original conversation before sending any follow-up.")
        else: st.success("No follow-ups currently due.")
    else: st.info("Add leads to start tracking follow-ups.")
    st.caption("This tracker calculates due dates when the app is opened; it does not run in the background or send reminders.")

with tab4:
    st.subheader("Export and handoff")
    if len(df):
        st.download_button("Download all leads as CSV",df.to_csv(index=False).encode("utf-8"),"gopratle_bdr_leads.csv","text/csv")
        st.download_button("Download lead records as JSON",df.to_json(orient="records",indent=2).encode("utf-8"),"gopratle_bdr_leads.json","application/json")
    else: st.info("No records to export yet.")
    st.markdown("**Google Sheets handoff:** download the CSV, then import it into Google Sheets using File → Import → Upload. This is a manual import, not a live trigger/sync.")
    st.markdown("**Outreach handoff:** copy the reviewed email draft into a sandbox/test email account. No message is sent automatically.")

st.divider()
st.caption("Transparency: This no-API MVP supports manual research, local logging, pitch drafting, status management and a follow-up queue. Live web enrichment, Google Sheets event triggers, automated email sending and reply detection require external integrations.")
