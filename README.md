# BGL Client Support Assistant

A RAG-based support assistant for BGL's clients and internal sales team. This is a real, deployable tool that could genuinely reduce the manual back-and-forth your account managers handle for routine client questions.

## What it does

- Answers client questions (installation, pricing, warranty, onboarding)
  grounded in BGL's actual knowledge base — no hallucinated policy details
- Full chat interface with conversation memory (follow-up questions work)
- Shows **sources** for every answer, so you can verify what it's citing
- Has a built-in **relevance threshold** — if a question falls outside the
  knowledge base, it says so honestly and points to the account manager,
  instead of guessing

## Setup (same as before)

```
pip install -r requirements.txt
export MISTRAL_API_KEY="your-key-here"
streamlit run app.py
```

## Making this genuinely useful for BGL (not just a demo)

1. **Replace `knowledge_base.txt` with real content.** I've stubbed in
   plausible BGL policies (ES-25 install process, warranty terms, pricing
   model) — swap these for your actual documented policies, FAQs pulled
   from real client emails, and your real pricing/contract terms.

2. **Think about who uses this.** Two real options:
   - **Internal tool** for your 3-person sales team, so they can answer
     client questions instantly instead of digging through old emails or
     asking you directly — lower risk, faster to roll out.
   - **Client-facing tool** embedded on your website or shared via a link
     — higher value, but needs tighter guardrails (the relevance threshold
     and "I don't know" fallback matter a lot more here).
   Start internal. It's the same code either way — the only change is who
   you give the link to.

3. **Test it hard before trusting it.** Ask it deliberately tricky
   questions — things adjacent to but not exactly in the knowledge base —
   and check it says "I don't know" rather than inventing a plausible-
   sounding but wrong answer. This is the single most important thing to
   validate before anyone relies on it for real client conversations.

## Deploy it live

Same as the earlier demo: push to a public GitHub repo, deploy free on
Streamlit Cloud (share.streamlit.io), add your API key as a secret. You'll
get a shareable URL your team (or you, in an interview) can actually use.


- "I thought through rollout sequencing — internal tool first to de-risk,
  then potentially client-facing — which mirrors how I'd actually guide a
  customer through an adoption journey."
- Be honest about scope: in-memory retrieval, no vector database, no
  authentication — fine for a small internal pilot, and you can speak
  clearly to what you'd add (Pinecone/Weaviate, SSO, monitoring) for a
  production rollout at enterprise scale.
