import streamlit as st
import time

AGENTS_IMPORT_ERROR = None
try:
    from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
except Exception as e:
    build_reader_agent = None
    build_search_agent = None
    writer_chain = None
    critic_chain = None
    AGENTS_IMPORT_ERROR = e

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    color: #c8d4c0;
    background: #050a05;
}

.stApp {
    background: #060d06;
    background-image:
        radial-gradient(ellipse at 0% 0%, rgba(20, 80, 20, 0.28) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%, rgba(10, 50, 10, 0.20) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.6) 0%, transparent 80%);
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 3rem; max-width: 1200px; }

/* ── Scanline texture overlay ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 0, 0, 0.03) 2px,
        rgba(0, 0, 0, 0.03) 4px
    );
    pointer-events: none;
    z-index: 0;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 1.2rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3.2rem, 7vw, 5.2rem);
    font-weight: 800;
    line-height: 0.95;
    color: #e8f5e8;
    margin: 0 0 1rem;
    letter-spacing: -0.02em;
}
.hero h1 span {
    color: #4ade80;
    position: relative;
}
.hero h1 span::after {
    content: '';
    position: absolute;
    bottom: 4px;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4ade80, #16a34a);
    border-radius: 2px;
}
.hero-sub {
    font-size: 0.95rem;
    font-weight: 400;
    color: #6b7c6b;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.9;
    letter-spacing: 0.01em;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.2), transparent);
    margin: 2rem 0;
}

/* ── Corner decoration ── */
.corner-tl, .corner-br {
    position: absolute;
    width: 18px;
    height: 18px;
}
.corner-tl {
    top: 0; left: 0;
    border-top: 1.5px solid #4ade80;
    border-left: 1.5px solid #4ade80;
    border-radius: 2px 0 0 0;
}
.corner-br {
    bottom: 0; right: 0;
    border-bottom: 1.5px solid #4ade80;
    border-right: 1.5px solid #4ade80;
    border-radius: 0 0 2px 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(5, 18, 5, 0.95);
    border: 1px solid rgba(74,222,128,0.12);
    border-radius: 4px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    position: relative;
}
.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #4ade80, transparent);
    opacity: 0.4;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(0, 0, 0, 0.6) !important;
    border: 1px solid rgba(74,222,128,0.2) !important;
    border-radius: 4px !important;
    color: #d4e8d4 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 2px rgba(74,222,128,0.08) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3a4e3a !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: #4ade80 !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: #0a1f0a !important;
    color: #4ade80 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(74,222,128,0.35) !important;
    border-radius: 4px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    width: 100%;
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(74,222,128,0.06) 0%, transparent 60%);
}
.stButton > button:hover {
    background: #122012 !important;
    border-color: #4ade80 !important;
    color: #86efac !important;
    box-shadow: 0 0 20px rgba(74,222,128,0.1), inset 0 0 20px rgba(74,222,128,0.04) !important;
}
.stButton > button:active {
    transform: scale(0.99) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(0, 5, 0, 0.7);
    border: 1px solid rgba(74,222,128,0.07);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 8px; height: 8px;
    border-top: 1px solid rgba(74,222,128,0.15);
    border-right: 1px solid rgba(74,222,128,0.15);
}
.step-card.active {
    border-color: rgba(74,222,128,0.3);
    background: rgba(10, 30, 10, 0.85);
}
.step-card.done {
    border-color: rgba(74,222,128,0.18);
    background: rgba(5, 20, 5, 0.8);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 2px;
    background: rgba(74,222,128,0.1);
    transition: background 0.3s;
}
.step-card.active::before { background: #4ade80; box-shadow: 0 0 8px #4ade80; }
.step-card.done::before   { background: #16a34a; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 0.25rem;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    color: #2d6a2d;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #c8d8c8;
    letter-spacing: 0.01em;
}
.step-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
}
.status-waiting  { color: #2a402a; }
.status-running  { color: #4ade80; }
.status-done     { color: #16a34a; }

/* ── Result panels ── */
.result-panel {
    background: rgba(0, 5, 0, 0.7);
    border: 1px solid rgba(74,222,128,0.08);
    border-radius: 4px;
    padding: 1.6rem 1.8rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(74,222,128,0.1);
}
.result-content {
    font-size: 0.9rem;
    line-height: 1.9;
    color: #7a9a7a;
    white-space: pre-wrap;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: rgba(2, 10, 2, 0.9);
    border: 1px solid rgba(74,222,128,0.14);
    border-radius: 4px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
    position: relative;
}
.report-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.4), transparent);
}
.feedback-panel {
    background: rgba(2, 10, 2, 0.9);
    border: 1px solid rgba(22,163,74,0.18);
    border-radius: 4px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    margin-bottom: 1.3rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(74,222,128,0.1);
}
.panel-label.orange { color: #4ade80; }
.panel-label.green  { color: #16a34a; }

/* ── Section heading ── */
.section-heading {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #4ade80;
    margin: 1.8rem 0 1rem;
    padding-left: 0.75rem;
    border-left: 2px solid #4ade80;
}

/* ── Expander ── */
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #3a5c3a !important;
    letter-spacing: 0.12em !important;
    cursor: pointer;
}

/* ── Spinner ── */
.stSpinner > div { color: #4ade80 !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: #4ade80 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.14em !important;
    border: 1px solid rgba(74,222,128,0.25) !important;
    border-radius: 4px !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    border-color: #4ade80 !important;
    background: rgba(74,222,128,0.06) !important;
}

/* ── Warning / error / info overrides ── */
.stAlert {
    background: rgba(10, 25, 10, 0.9) !important;
    border: 1px solid rgba(74,222,128,0.2) !important;
    border-radius: 4px !important;
    color: #a0c0a0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── Footer notice ── */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #1e3020;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Markdown inside report panel ── */
.report-panel h1, .report-panel h2, .report-panel h3 {
    color: #86efac;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    border-bottom: 1px solid rgba(74,222,128,0.1);
    padding-bottom: 0.3rem;
    margin-bottom: 0.8rem;
}
.report-panel p { color: #8aaa8a; line-height: 1.85; }
.report-panel strong { color: #c8d8c8; }
.report-panel code {
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 3px;
    padding: 0.1rem 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    color: #4ade80;
}
</style>
""", unsafe_allow_html=True)

if AGENTS_IMPORT_ERROR is not None:
    st.error("The app could not load required AI dependencies.")
    st.error(f"Import error: {AGENTS_IMPORT_ERROR}")
    st.info(
        "Install missing packages (e.g. bs4, tavily-python, langchain, openai) "
        "and make sure the correct Python environment is active."
    )
    st.stop()


def _handle_step_error(step_name: str, exc: Exception):
    msg = str(exc)
    is_rate = False
    try:
        import openai
        is_rate = isinstance(exc, getattr(openai, 'error', getattr(openai, 'OpenAIError', Exception)).RateLimitError) if hasattr(openai, 'error') else False
    except Exception:
        is_rate = False

    if not is_rate:
        if "insufficient_quota" in msg or "RateLimitError" in type(exc).__name__ or "429" in msg:
            is_rate = True

    if is_rate:
        st.error(f"{step_name} failed: OpenAI quota/rate limit error.")
        st.info("This usually means your OpenAI API key has no remaining quota. Wait and try again, or set a different key.")
    else:
        st.error(f"{step_name} failed: {msg}")

    if st.button("Retry"):
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.error = None
        st.experimental_rerun()

    st.session_state.running = False
    st.session_state.done = False
    st.session_state.error = msg
    st.stop()


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("— IDLE",    "status-waiting"),
        "running": ("◉ RUNNING", "status-running"),
        "done":    ("✓ DONE",    "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.75rem;color:#2a4a2a;margin-top:0.3rem;font-family:JetBrains Mono,monospace;letter-spacing:0.06em;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">// AI Research Studio v2.0</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Accelerated intelligence for professional research workflows.
        Search, analyze, summarise and validate findings automatically
        with a single streamlined pipeline.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Execute Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;align-items:center;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#2d502d;letter-spacing:0.18em;text-transform:uppercase;">Try →</span>
    """, unsafe_allow_html=True)
    examples = ["AI governance risks", "Climate innovation research", "Enterprise knowledge synthesis"]
    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(74,222,128,0.05);
            border:1px solid rgba(74,222,128,0.14);
            border-radius:3px;
            padding:0.3rem 0.75rem;
            font-size:0.75rem;
            color:#5a7a5a;
            font-family:'Syne',sans-serif;
            letter-spacing:0.02em;
            cursor:default;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline Status</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        if step in r:
            return "done"
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    try:
        results = {}
        topic_val = st.session_state.topic_input

        # ── Step 1: Search ──
        with st.spinner("[ 01 ]  Search Agent is working…"):
            try:
                search_agent = build_search_agent()
                sr = search_agent.invoke({
                    "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
                })
                results["search"] = sr["messages"][-1].content
                st.session_state.results = dict(results)
            except Exception as e:
                _handle_step_error("Search agent", e)

        # ── Step 2: Reader ──
        with st.spinner("[ 02 ]  Reader Agent is scraping top resources…"):
            try:
                reader_agent = build_reader_agent()
                rr = reader_agent.invoke({
                    "messages": [("user",
                        f"Based on the following search results about '{topic_val}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{results['search'][:800]}"
                    )]
                })
                results["reader"] = rr["messages"][-1].content
                st.session_state.results = dict(results)
            except Exception as e:
                _handle_step_error("Reader agent", e)

        # ── Step 3: Writer ──
        with st.spinner("[ 03 ]  Writer is drafting the report…"):
            try:
                research_combined = (
                    f"SEARCH RESULTS:\n{results['search']}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
                )
                results["writer"] = writer_chain.invoke({
                    "topic": topic_val,
                    "research": research_combined
                })
                st.session_state.results = dict(results)
            except Exception as e:
                _handle_step_error("Writer chain", e)

        # ── Step 4: Critic ──
        with st.spinner("[ 04 ]  Critic is reviewing the report…"):
            try:
                results["critic"] = critic_chain.invoke({
                    "report": results["writer"]
                })
                st.session_state.results = dict(results)
            except Exception as e:
                _handle_step_error("Critic chain", e)

        st.session_state.running = False
        st.session_state.done = True
        st.rerun()
    except Exception as e:
        _handle_step_error("Pipeline", e)


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Output</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("[ 01 ]  Search Results — raw output", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">// Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("[ 02 ]  Scraped Content — raw output", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">// Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">// Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="↓  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">// Critic Analysis</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)