import streamlit as st
import google.generativeai as genai
import streamlit_authenticator as stauth
from datetime import datetime

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SCL Agent – Siemens PLC",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════
# CUSTOM CSS  –  Industrial dark-terminal aesthetic
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --bg:       #0b0e14;
    --surface:  #111620;
    --surface2: #1a2030;
    --border:   #1e2d45;
    --accent:   #00c2ff;
    --success:  #00e676;
    --danger:   #ff3b3b;
    --warn:     #ffd600;
    --text:     #c9d6e8;
    --muted:    #5a6a80;
}

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

.main .block-container { background: var(--bg) !important; padding-top: 2rem !important; }

h1 {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important; letter-spacing: 3px !important;
    color: var(--accent) !important; font-size: 2rem !important;
}
h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important; color: var(--text) !important;
    letter-spacing: 1px !important;
}

.metric-box {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 14px 18px; text-align: center; margin-bottom: 8px;
}
.metric-val { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; color: var(--accent); }
.metric-lbl { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-top: 2px; }

.audit-pass {
    background: rgba(0,230,118,0.08); border: 1px solid rgba(0,230,118,0.25);
    border-radius: 6px; padding: 8px 14px; margin: 4px 0;
    font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--success);
}
.audit-fail {
    background: rgba(255,59,59,0.08); border: 1px solid rgba(255,59,59,0.25);
    border-radius: 6px; padding: 8px 14px; margin: 4px 0;
    font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--danger);
}

.status-ok {
    background: linear-gradient(90deg, rgba(0,194,255,0.1), transparent);
    border: 1px solid rgba(0,194,255,0.3); border-radius: 8px; padding: 14px 20px;
    color: var(--accent); font-weight: 600; font-size: 15px; letter-spacing: 1px;
}
.status-warn {
    background: linear-gradient(90deg, rgba(255,214,0,0.1), transparent);
    border: 1px solid rgba(255,214,0,0.3); border-radius: 8px; padding: 14px 20px;
    color: var(--warn); font-weight: 600; font-size: 15px;
}
.status-fail {
    background: linear-gradient(90deg, rgba(255,59,59,0.1), transparent);
    border: 1px solid rgba(255,59,59,0.3); border-radius: 8px; padding: 14px 20px;
    color: var(--danger); font-weight: 600; font-size: 15px;
}

.tag {
    display: inline-block; background: rgba(0,194,255,0.12);
    border: 1px solid rgba(0,194,255,0.3); border-radius: 4px;
    padding: 2px 10px; font-size: 12px; font-family: 'JetBrains Mono', monospace;
    color: var(--accent); margin: 2px 3px;
}
.tag-warn { background: rgba(255,214,0,0.1); border-color: rgba(255,214,0,0.3); color: var(--warn); }
.tag-ok   { background: rgba(0,230,118,0.1); border-color: rgba(0,230,118,0.3); color: var(--success); }
.tag-danger { background: rgba(255,59,59,0.1); border-color: rgba(255,59,59,0.3); color: var(--danger); }

.section-lbl {
    font-size: 10px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase;
    color: var(--muted); margin: 24px 0 10px;
    border-bottom: 1px solid var(--border); padding-bottom: 6px;
}

textarea, input[type="text"], input[type="password"] {
    background: var(--surface2) !important; border: 1px solid var(--border) !important;
    border-radius: 6px !important; color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif !important; font-size: 15px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0078a8, #005580) !important;
    color: white !important; border: none !important; border-radius: 6px !important;
    font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important;
    font-size: 15px !important; letter-spacing: 1px !important;
    padding: 10px 24px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00a0d8, #006a9e) !important;
    box-shadow: 0 0 16px rgba(0,194,255,0.3) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stExpander"] {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] > div {
    background: var(--surface2) !important; border-color: var(--border) !important;
    color: var(--text) !important;
}
.stCodeBlock { border: 1px solid var(--border) !important; border-radius: 8px !important; }

#MainMenu, footer, .stDeployButton { visibility: hidden; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
for k, v in {
    "authentication_status": None,
    "scl_code": None,
    "review_text": None,
    "history": [],
    "active_template": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════
try:
    credentials = st.secrets["credentials"].to_dict()
    cookie = st.secrets["cookie"].to_dict()
    authenticator = stauth.Authenticate(
        credentials, cookie["name"], cookie["key"], int(cookie["expiry_days"])
    )
except Exception as e:
    st.error(f"Configuration Error: {e}. Check your Streamlit Secrets.")
    st.stop()

try:
    result = authenticator.login(label='Login', location='main')
except TypeError:
    result = authenticator.login('main')

if isinstance(result, tuple):
    name, authentication_status, username = result
else:
    name = st.session_state.get("name")
    authentication_status = st.session_state.get("authentication_status")


# ══════════════════════════════════════════════════════════
# CONSTANTS & HELPERS
# ══════════════════════════════════════════════════════════
AUDIT_CHECKS = {
    "FUNCTION_BLOCK Structure":     lambda c: "FUNCTION_BLOCK" in c.upper() and "END_FUNCTION_BLOCK" in c.upper(),
    "VAR / END_VAR Declaration":    lambda c: "VAR" in c.upper() and "END_VAR" in c.upper(),
    "Safety Interlock (Global DB)": lambda c: "Global_Safety_DB" in c,
    "3-Way Handshake":              lambda c: "i_HMI_Confirm" in c and "i_System_Ready" in c and "i_AI_Req" in c,
    "Input Clamping (LIMIT)":       lambda c: "LIMIT" in c.upper(),
    "RETURN on Safety Fail":        lambda c: "RETURN" in c.upper(),
    "Output Guard (q_Execute)":     lambda c: "q_Execute" in c,
    "IF / END_IF Syntax":           lambda c: c.upper().count("IF") >= 1 and "END_IF" in c.upper(),
}

FB_TEMPLATES = {
    "Lead/Lag Pump":    "Lead/Lag Pump Control with pressure monitoring, flow sensors, automatic switchover, runtime hour tracking per pump, and alternating start logic.",
    "PID Temperature":  "PID Temperature Control loop for a heat exchanger. Include setpoint ramp, manual/auto mode switch, output clamping 0–100%, and high/low deviation alarms.",
    "Conveyor Safety":  "Conveyor belt safety gate interlock. Monitor E-Stop, light curtain, physical gate switch. Require operator reset after fault. Include belt speed feedback and jam detection.",
    "Valve Sequencer":  "Motorised valve sequencer with open/close feedback, travel timeout fault, and partial-stroke test capability. Support manual override from HMI.",
    "Motor Soft-Start": "Motor soft-start with ramp-up time, current monitoring, overload protection, and auto-restart on fault clearance with configurable retry limit.",
    "Batch Dosing":     "Batch liquid dosing with load cell feedback, pre-act correction, tolerance checking, batch counter, flush sequence, and CIP mode.",
}

def run_audit(code):
    return {label: fn(code) for label, fn in AUDIT_CHECKS.items()}

def audit_score(results):
    return sum(1 for v in results.values() if v)

def count_lines(code):
    return len([l for l in code.splitlines() if l.strip()])

def count_vars(code):
    return sum(1 for line in code.splitlines() if ":" in line and any(
        t in line.upper() for t in ["BOOL","INT","REAL","DINT","WORD","DWORD","TIME","STRING","TON","CTU"]
    ))

def build_prompt(requirement, fb_name, opts):
    plc = opts.get("plc_model", "S7-1500")
    comments = opts.get("comments", True)
    alarms = opts.get("alarms", True)
    strictness = opts.get("strictness", "production")

    return f"""Act as a Senior Siemens TIA Portal Developer with 15+ years of {plc} experience.

Generate a complete, production-ready Siemens SCL FUNCTION_BLOCK for:
"{requirement}"

FUNCTION BLOCK NAME: {fb_name}

MANDATORY STRUCTURE:
1. FUNCTION_BLOCK "{fb_name}"
2. VAR_INPUT: i_AI_Req (Bool), i_HMI_Confirm (Bool), i_System_Ready (Bool), plus all process inputs
3. VAR_OUTPUT: q_Execute (Bool), q_Fault (Bool), q_Status (WORD), plus process outputs
4. VAR (static): state variables, TON timers, counters, handshake state
5. VAR_TEMP: temporary calculation variables only
6. BEGIN ... END_FUNCTION_BLOCK

SAFETY RULES (non-negotiable):
- FIRST line after BEGIN: IF NOT "Global_Safety_DB".All_Systems_OK THEN q_Fault := TRUE; RETURN; END_IF;
- q_Execute only TRUE when: i_AI_Req AND i_HMI_Confirm AND i_System_Ready AND all local conditions
- ALL analog values scaled with LIMIT(MN:=, IN:=, MX:=)
- Reset all outputs on any fault

{"COMMENTING: Use (* comment *) on every logic block. Include a header comment block with FB name, version, date, purpose." if comments else "Minimal inline comments only."}
{"ALARMS: Include bit-mapped q_Status WORD with minimum 4 defined alarm bits." if alarms else ""}
{"Strictness: Full IEC 61131-3 compliance. Every variable declared and typed." if strictness == "production" else "Functional prototype, relax commenting."}

Target: TIA Portal V17+ on {plc}.
Output ONLY raw SCL text — no markdown, no backticks, no prose. Begin immediately with FUNCTION_BLOCK."""


# ══════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════
if authentication_status:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("## ⚙️ SCL AGENT")
        st.markdown("---")
        authenticator.logout("Logout", "sidebar")
        st.markdown(f"**👤 {name}**")
        st.markdown(f"<span style='color:#5a6a80;font-size:12px;font-family:JetBrains Mono,monospace'>{datetime.now().strftime('%Y-%m-%d  %H:%M')}</span>", unsafe_allow_html=True)
        st.markdown("---")

        page = st.radio("Module", ["🔧 Generator", "📜 History", "📖 SCL Reference"], label_visibility="collapsed")

        st.markdown("---")
        st.markdown('<div class="section-lbl">Session Stats</div>', unsafe_allow_html=True)
        total_gen = len(st.session_state.history)
        passed_all = sum(1 for h in st.session_state.history if h.get("score") == len(AUDIT_CHECKS))
        st.markdown(f"""
        <div class="metric-box"><div class="metric-val">{total_gen}</div><div class="metric-lbl">Blocks Generated</div></div>
        <div class="metric-box"><div class="metric-val" style="color:var(--success)">{passed_all}</div><div class="metric-lbl">Full Audits Passed</div></div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # GENERATOR
    # ══════════════════════════════════════════════════════
    if "Generator" in page:
        st.markdown("# ⚙️ SIEMENS SCL FUNCTION BLOCK AGENT")
        st.markdown(
            '<span class="tag">TIA Portal V17+</span>'
            '<span class="tag">S7-1500 / S7-1200</span>'
            '<span class="tag">IEC 61131-3</span>'
            '<span class="tag">SCL</span>',
            unsafe_allow_html=True
        )

        col_form, col_opts = st.columns([3, 2])

        with col_form:
            st.markdown('<div class="section-lbl">Quick Templates</div>', unsafe_allow_html=True)
            tpl_cols = st.columns(3)
            for idx, tname in enumerate(FB_TEMPLATES):
                with tpl_cols[idx % 3]:
                    if st.button(tname, key=f"tpl_{idx}", use_container_width=True):
                        st.session_state.active_template = FB_TEMPLATES[tname]
                        st.rerun()

            st.markdown('<div class="section-lbl">Function Block Requirement</div>', unsafe_allow_html=True)
            requirement = st.text_area(
                "Requirement",
                value=st.session_state.active_template or "",
                height=130,
                placeholder="e.g. Lead/Lag pump control with pressure safety interlock, flow monitoring, and HMI status feedback…",
                label_visibility="collapsed"
            )
            fb_name = st.text_input(
                "Function Block Name",
                value="FB_Generated_Logic",
                help='Appears as FUNCTION_BLOCK "FB_Generated_Logic"'
            )

        with col_opts:
            st.markdown('<div class="section-lbl">Generation Options</div>', unsafe_allow_html=True)
            plc_model = st.selectbox("Target PLC", ["S7-1500", "S7-1200", "S7-300 (Legacy)"])
            st.selectbox("TIA Portal Version", ["V19", "V18", "V17", "V16"])
            strictness = st.radio("Code Standard", ["production", "prototype"], horizontal=True)
            include_comments = st.toggle("Inline Comments", value=True)
            include_alarms = st.toggle("Alarm Status Word", value=True)
            add_review = st.toggle("AI Code Review", value=True)

            st.markdown('<div class="section-lbl">Audit Checks</div>', unsafe_allow_html=True)
            for check in AUDIT_CHECKS:
                st.markdown(f'<span class="tag" style="font-size:11px;margin:2px;">{check}</span>', unsafe_allow_html=True)

        st.markdown("")
        gen_col, _ = st.columns([2, 3])
        with gen_col:
            generate = st.button("⚡ GENERATE FUNCTION BLOCK", use_container_width=True)

        if generate:
            if not requirement.strip():
                st.warning("⚠️ Enter a requirement or select a template.")
            else:
                with st.spinner("Generating SCL Function Block…"):
                    opts = {"strictness": strictness, "comments": include_comments,
                            "alarms": include_alarms, "plc_model": plc_model}
                    response = model.generate_content(build_prompt(requirement, fb_name, opts))
                    scl_code = response.text.strip()
                    for fence in ["```scl", "```pascal", "```", "~~~"]:
                        scl_code = scl_code.replace(fence, "")
                    st.session_state.scl_code = scl_code.strip()
                    st.session_state.review_text = None

                if add_review:
                    with st.spinner("Running AI code review…"):
                        review_prompt = f"""You are a senior Siemens TIA Portal engineer doing a code review.
Analyse this SCL Function Block and provide a structured review with these sections:

**1. Correctness** – syntax issues, undeclared variables, logic errors
**2. Safety Gaps** – missing interlocks, unguarded outputs, missing RETURN paths
**3. TIA Portal Compatibility** – any V17+ incompatibilities
**4. Optimisation Tips** – redundant code, better patterns, performance
**5. Overall Rating** – score /10 with one-line verdict

Be concise, specific, and technical. Use bullet points.

SCL Code:
{st.session_state.scl_code}"""
                        st.session_state.review_text = model.generate_content(review_prompt).text

                # Save to history
                audit_results = run_audit(st.session_state.scl_code)
                st.session_state.history.insert(0, {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "requirement": requirement[:60] + ("…" if len(requirement) > 60 else ""),
                    "fb_name": fb_name,
                    "plc": plc_model,
                    "code": st.session_state.scl_code,
                    "score": audit_score(audit_results),
                    "lines": count_lines(st.session_state.scl_code),
                })

        # ── Results ──
        if st.session_state.scl_code:
            scl_code = st.session_state.scl_code
            audit_results = run_audit(scl_code)
            score = audit_score(audit_results)
            total_checks = len(AUDIT_CHECKS)

            st.markdown("---")
            st.markdown('<div class="section-lbl">Generated Output</div>', unsafe_allow_html=True)

            mc1, mc2, mc3, mc4 = st.columns(4)
            score_color = "var(--success)" if score == total_checks else "var(--warn)" if score >= int(total_checks * 0.7) else "var(--danger)"
            mc1.markdown(f'<div class="metric-box"><div class="metric-val">{count_lines(scl_code)}</div><div class="metric-lbl">Lines of Code</div></div>', unsafe_allow_html=True)
            mc2.markdown(f'<div class="metric-box"><div class="metric-val">{count_vars(scl_code)}</div><div class="metric-lbl">Variables Declared</div></div>', unsafe_allow_html=True)
            mc3.markdown(f'<div class="metric-box"><div class="metric-val" style="color:{score_color}">{score}/{total_checks}</div><div class="metric-lbl">Audit Score</div></div>', unsafe_allow_html=True)
            mc4.markdown(f'<div class="metric-box"><div class="metric-val" style="color:var(--accent)">{int(score/total_checks*100)}%</div><div class="metric-lbl">Compliance</div></div>', unsafe_allow_html=True)

            code_col, audit_col = st.columns([3, 2])

            with code_col:
                st.markdown('<div class="section-lbl">SCL Source Code</div>', unsafe_allow_html=True)
                st.code(scl_code, language="pascal")
                dl1, dl2 = st.columns(2)
                with dl1:
                    st.download_button("💾 Download .SCL", data=scl_code, file_name=f"{fb_name}.scl",
                                       mime="text/plain", use_container_width=True)
                with dl2:
                    st.download_button("📄 Download .TXT", data=scl_code, file_name=f"{fb_name}.txt",
                                       mime="text/plain", use_container_width=True)

            with audit_col:
                st.markdown('<div class="section-lbl">Security & Compliance Audit</div>', unsafe_allow_html=True)
                for check, passed in audit_results.items():
                    css = "audit-pass" if passed else "audit-fail"
                    icon = "✅" if passed else "❌"
                    st.markdown(f'<div class="{css}">{icon} {check}</div>', unsafe_allow_html=True)

                st.markdown("")
                if score == total_checks:
                    st.markdown('<div class="status-ok">✅ VALIDATED — READY FOR TIA PORTAL</div>', unsafe_allow_html=True)
                elif score >= int(total_checks * 0.7):
                    st.markdown('<div class="status-warn">⚠️ PARTIAL PASS — MANUAL REVIEW REQUIRED</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="status-fail">❌ AUDIT FAILED — DO NOT DEPLOY</div>', unsafe_allow_html=True)

                failed = [k for k, v in audit_results.items() if not v]
                if failed:
                    st.markdown('<div class="section-lbl">Remediation Needed</div>', unsafe_allow_html=True)
                    for f in failed:
                        st.markdown(f'<span class="tag-danger">{f}</span>', unsafe_allow_html=True)

            if st.session_state.review_text:
                st.markdown("---")
                with st.expander("🤖 AI Code Review Report", expanded=True):
                    st.markdown(st.session_state.review_text)

    # ══════════════════════════════════════════════════════
    # HISTORY
    # ══════════════════════════════════════════════════════
    elif "History" in page:
        st.markdown("# 📜 GENERATION HISTORY")
        st.caption("All Function Blocks generated this session")

        history = st.session_state.history
        if not history:
            st.info("No blocks generated yet.")
        else:
            for i, item in enumerate(history):
                score = item.get("score", 0)
                total = len(AUDIT_CHECKS)
                sc = "var(--success)" if score == total else "var(--warn)" if score >= int(total * 0.7) else "var(--danger)"
                with st.expander(
                    f"⚙️ {item['fb_name']}  |  {item['timestamp']}  |  {item['plc']}  |  Score {score}/{total}",
                    expanded=False
                ):
                    st.markdown(f"**Requirement:** {item['requirement']}")
                    st.markdown(
                        f'<span class="tag">{item["plc"]}</span>'
                        f'<span class="tag">{item["lines"]} lines</span>'
                        f'<span class="tag" style="color:{sc}">Audit {score}/{total}</span>',
                        unsafe_allow_html=True
                    )
                    st.code(item["code"], language="pascal")
                    st.download_button(
                        f"💾 Download {item['fb_name']}.scl",
                        data=item["code"], file_name=f"{item['fb_name']}.scl",
                        mime="text/plain", key=f"dl_hist_{i}"
                    )

            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.rerun()

    # ══════════════════════════════════════════════════════
    # SCL REFERENCE
    # ══════════════════════════════════════════════════════
    elif "Reference" in page:
        st.markdown("# 📖 SCL QUICK REFERENCE")
        st.caption("Common patterns for Siemens TIA Portal SCL development")

        r1, r2 = st.columns(2)
        with r1:
            st.markdown("### Block Structure")
            st.code("""FUNCTION_BLOCK "FB_Name"
VAR_INPUT
    i_Enable   : Bool;
    i_Setpoint : Real;
END_VAR
VAR_OUTPUT
    q_Active   : Bool;
    q_Fault    : Bool;
END_VAR
VAR
    s_State    : Int;
    s_Timer    : TON;
END_VAR
VAR_TEMP
    t_Calc     : Real;
END_VAR

BEGIN
    IF NOT "Global_Safety_DB".All_Systems_OK THEN
        q_Fault := TRUE;
        RETURN;
    END_IF;

END_FUNCTION_BLOCK""", language="pascal")

            st.markdown("### LIMIT Function")
            st.code("""scaled := LIMIT(MN := 0.0,
                IN := raw_analog,
                MX := 100.0);""", language="pascal")

            st.markdown("### TON Timer")
            st.code("""s_Timer(IN := i_StartCondition,
        PT := T#5S,
        Q  => s_Done,
        ET => s_Elapsed);""", language="pascal")

        with r2:
            st.markdown("### 3-Way Handshake")
            st.code("""IF i_AI_Req AND i_HMI_Confirm AND i_System_Ready THEN
    q_Execute := TRUE;
ELSE
    q_Execute := FALSE;
END_IF;""", language="pascal")

            st.markdown("### State Machine")
            st.code("""CASE s_State OF
    0: (* IDLE *)
        IF i_Start THEN s_State := 1; END_IF;
    1: (* RUNNING *)
        q_Running := TRUE;
        IF i_Stop OR q_Fault THEN
            s_State := 0;
        END_IF;
    ELSE
        s_State := 0;
END_CASE;""", language="pascal")

            st.markdown("### Alarm Status Word")
            st.code("""q_Status.%X0 := b_OverTemp;
q_Status.%X1 := b_UnderPressure;
q_Status.%X2 := b_MotorFault;
q_Status.%X3 := b_CommTimeout;""", language="pascal")

            st.markdown("### Safety DB Check")
            st.code("""IF NOT "Global_Safety_DB".All_Systems_OK THEN
    q_Execute := FALSE;
    q_Fault   := TRUE;
    s_State   := 0;
    RETURN;
END_IF;""", language="pascal")

        st.markdown("---")
        st.markdown("### IEC 61131-3 Data Types")
        types = [
            ("Bool","1-bit boolean","TRUE / FALSE"),
            ("Int","16-bit signed","−32768..32767"),
            ("DInt","32-bit signed","−2147483648..2147483647"),
            ("Real","32-bit float","±3.4×10³⁸"),
            ("Word","16-bit unsigned","0..65535"),
            ("Time","Duration","T#1D2H3M4S5MS"),
            ("String","Characters","String[254]"),
            ("TON","On-delay timer","IN, PT → Q, ET"),
        ]
        tc1, tc2 = st.columns(2)
        for i, (dtype, desc, rng) in enumerate(types):
            col = tc1 if i % 2 == 0 else tc2
            col.markdown(
                f'<span class="tag">{dtype}</span> '
                f'<span style="color:var(--muted);font-size:13px;">{desc} — {rng}</span>',
                unsafe_allow_html=True
            )

# ══════════════════════════════════════════════════════════
# AUTH STATES
# ══════════════════════════════════════════════════════════
elif authentication_status == False:
    st.error("❌ Incorrect username or password.")
elif authentication_status is None:
    st.markdown("## ⚙️ SIEMENS SCL FUNCTION BLOCK AGENT")
    st.markdown("Production-grade SCL generation for TIA Portal. Please log in to continue.")
