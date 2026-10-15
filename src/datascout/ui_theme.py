"""Purple workspace styling and escaped semantic visual components."""

from html import escape

from datascout.ui_i18n import t


def icon(name):
    """Use HTML/CSS because Streamlit sanitizes inline SVG out of st.html."""
    if name not in {"search", "evidence", "file", "lock", "user"}:
        raise ValueError("Unknown semantic icon")
    return f'<span class="ds-icon ds-icon-{name}" aria-hidden="true"><i></i></span>'


def card(st, title, text, *, symbol="evidence", eyebrow=""):
    st.html(
        f'<article class="ds-card">{icon(symbol)}<small>{escape(eyebrow)}</small><h3>{escape(title)}</h3><p>{escape(text)}</p></article>'
    )


def brand(st):
    st.html(
        f'<div class="ds-brand">{icon("search")}'
        f'<span class="ds-brand-name">DataScout <em>AI</em></span>'
        f'<strong class="ds-brand-promise">{escape(t(st, "让数据选择有依据", "Make data decisions clear"))}</strong></div>'
    )


def apply_theme(st):
    st.html("""<style>
    :root {--ds-accent:#b59aff;--ds-panel:#19132c;--ds-line:#38264f;--ds-muted:#bfb3d1;}
    .stApp {font-size:16px;background:#0c0918;color:#f2eefb;background-image:linear-gradient(#b59aff05 1px,transparent 1px),linear-gradient(90deg,#b59aff05 1px,transparent 1px);background-size:44px 44px;}
    /* This app supplies its own navigation; the fixed native header obscures it. */
    [data-testid="stHeader"] {display:none;}
    .block-container {max-width:1420px;padding-top:1rem;padding-bottom:3rem;}
    [data-testid="stMarkdownContainer"] p,[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea {font-size:16px;line-height:1.7;}
    h1,h2,h3 {letter-spacing:-.035em;}
    .ds-brand {display:flex;align-items:center;gap:8px 10px;flex-wrap:wrap;min-height:48px;}
    .ds-brand-name {font-size:23px;font-weight:720;letter-spacing:-.055em;white-space:nowrap;line-height:1.1;}
    .ds-brand-name em {font-style:normal;color:var(--ds-accent)}
    .ds-brand-promise {font-size:15px;font-weight:550;letter-spacing:.015em;color:#d5c6ee;line-height:1.3;border-left:1px solid #8c6eb69c;padding-left:10px;}
    .ds-account {display:flex;align-items:center;justify-content:flex-end;gap:9px;min-height:48px;white-space:nowrap;}
    .ds-avatar {display:grid;place-items:center;width:35px;height:35px;flex:0 0 35px;border-radius:50%;background:linear-gradient(135deg,#8851dc,#bd9aff);color:#160b27;font-weight:750;}
    .ds-account-name {font-size:15px;font-weight:600;overflow:hidden;text-overflow:ellipsis;max-width:135px;}
    .ds-preview-badge {display:flex;align-items:center;justify-content:center;min-height:48px;border:1px solid #9271b957;border-radius:12px;background:#211630;color:#d9c9f1;font-size:14px;font-weight:600;}
    .st-key-site_nav {padding-bottom:16px;border-bottom:1px solid #8d6ab244;}
    .st-key-site_nav [data-testid="stHorizontalBlock"] {align-items:center;}
    .st-key-workspace_nav {margin:8px 0 10px;padding:4px 0;border-bottom:1px solid #38264f;background:transparent;}
    .st-key-workspace_nav [data-testid="stHorizontalBlock"] {align-items:center;}
    .st-key-workspace_nav h2 {font-size:22px;line-height:1.3;margin:0!important;}
    .st-key-workspace_nav [data-testid="stCaptionContainer"] {color:#cdbfe0;font-size:13px;letter-spacing:.09em;}
    .st-key-workspace_nav button {min-height:38px!important;border-radius:8px!important;}
    .st-key-workspace_nav button p {font-size:16px!important;font-weight:650!important;}
    .ds-icon {display:inline-block;position:relative;width:24px;height:24px;min-width:24px;flex-shrink:0;color:var(--ds-accent);vertical-align:middle;}
    .ds-icon::before,.ds-icon::after,.ds-icon i,.ds-icon i::before,.ds-icon i::after {position:absolute;box-sizing:border-box;content:"";display:block;}
    .ds-icon-search::before {width:15px;height:15px;left:2px;top:1px;border:1.5px solid currentColor;border-radius:50%;}
    .ds-icon-search::after {width:10px;height:1.5px;left:14px;top:16px;background:currentColor;transform:rotate(45deg);transform-origin:left;}
    .ds-icon-evidence::before,.ds-icon-file::before {width:16px;height:21px;left:4px;top:1px;border:1.5px solid currentColor;border-radius:2px;}
    .ds-icon-evidence::after {width:8px;height:10px;left:8px;top:7px;background:repeating-linear-gradient(to bottom,currentColor 0,currentColor 1px,transparent 1px,transparent 4px);}
    .ds-icon-file::after {height:10px;width:1.5px;left:11px;top:8px;background:currentColor;}
    .ds-icon-file i {width:7px;height:7px;left:8px;top:8px;border-top:1.5px solid currentColor;border-left:1.5px solid currentColor;transform:rotate(45deg);}
    .ds-icon-lock::before {width:18px;height:13px;left:3px;top:10px;border:1.5px solid currentColor;border-radius:3px;}
    .ds-icon-lock::after {width:10px;height:11px;left:7px;top:1px;border:1.5px solid currentColor;border-radius:8px 8px 0 0;}
    .ds-icon-lock i {width:2px;height:5px;background:currentColor;left:11px;top:14px;}
    .ds-icon-user::before {width:9px;height:9px;left:7.5px;top:1px;border:1.5px solid currentColor;border-radius:50%;}
    .ds-icon-user::after {width:20px;height:11px;left:2px;top:13px;border:1.5px solid currentColor;border-radius:12px 12px 2px 2px;}

    .ds-dataset {border-top:2px solid #725798;padding:18px 0;min-height:310px;}
    .ds-dataset h3 {font-size:21px;margin:0 0 8px;}.ds-dataset p{color:var(--ds-muted);line-height:1.6;min-height:54px;}
    .ds-dataset dl{font-size:14px;margin:12px 0 0;}.ds-dataset dl div{display:grid;grid-template-columns:80px 1fr;gap:10px;padding:5px 0;border-top:1px solid #38264f;}
    .ds-dataset dt{color:var(--ds-muted);}.ds-dataset dd{margin:0;overflow-wrap:anywhere;}
    .ds-card {background:linear-gradient(135deg,#201831,#151023);border:1px solid var(--ds-line);border-radius:18px;padding:28px;height:100%;transition:transform .25s,border-color .25s,box-shadow .25s;}
    .ds-card:hover {transform:translateY(-3px);border-color:#79609e;box-shadow:0 12px 36px #b59aff0d;}
    .ds-card h3 {margin:14px 0 8px;font-size:21px;} .ds-card p {color:var(--ds-muted);line-height:1.8;margin:0;} .ds-card small {color:var(--ds-accent);font:12px Consolas,monospace;letter-spacing:2px;margin-left:12px;}
    [data-testid="stForm"], [data-testid="stMetric"] {background:#19132c;border:1px solid var(--ds-line);border-radius:14px;padding:20px;}
    [data-testid="stBaseButton-secondary"] [data-testid="stIconMaterial"] {color:var(--ds-accent);}
    button {min-height:48px!important;} button p {font-size:16px!important;line-height:1.4!important;}
    button {transition:transform .2s,box-shadow .2s!important;} button:hover {box-shadow:0 0 22px #b59aff14;} button:focus-visible,a:focus-visible {outline:2px solid #b59aff!important;outline-offset:3px;}
    [data-testid="stExpander"] {border-color:var(--ds-line);background:#151023;}
    @media(max-width:700px){.block-container {padding:1rem;} .ds-brand-promise {font-size:13px;} .ds-account {justify-content:flex-start;} .ds-card {padding:18px;}.st-key-workspace_nav{padding:6px 0;margin-top:8px;}}
    .st-key-procurement {padding:16px 20px!important;border:1px solid var(--ds-line)!important;border-radius:14px!important;background:#151023;}
    .st-key-procurement [data-testid="stTextArea"] textarea {background:#0e0b19;border-radius:8px;}
    .st-key-procurement [data-testid="stCaptionContainer"] p {font-size:13px;line-height:1.5;}
    [data-testid="stNumberInput"] input,[data-testid="stSelectbox"] [data-baseweb="select"] {border-radius:8px;}
    [data-testid="InputInstructions"] {display:none;}
    @media(max-width:1100px){.st-key-site_nav [data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:8px!important}.st-key-site_nav [data-testid="stColumn"]{flex:1 1 30%!important;min-width:130px!important;width:auto!important}.st-key-site_nav [data-testid="stColumn"]:first-child{flex:1 1 100%!important}}
    @media(max-width:700px){.st-key-site_nav [data-testid="stHorizontalBlock"],.st-key-workspace_nav [data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:8px!important}.st-key-site_nav [data-testid="stColumn"],.st-key-workspace_nav [data-testid="stColumn"]{flex:1 1 40%!important;min-width:0!important;width:auto!important}.st-key-site_nav [data-testid="stColumn"]:first-child,.st-key-workspace_nav [data-testid="stColumn"]:first-child{flex:1 1 100%!important}.st-key-site_nav button{padding:8px!important}.st-key-site_nav button p{font-size:13px!important;white-space:normal!important;overflow:visible!important;text-overflow:clip!important}.st-key-site_nav [data-testid="stIconMaterial"]{font-size:18px!important}}
    @media(max-width:700px){.st-key-site_nav [data-testid="stColumn"]:nth-child(4){flex:1 1 100%!important}}
    @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important;}.ds-card:hover{transform:none;}}
    </style>""")

    if t(st, "zh", "en") == "zh":
        st.html("""<style>
        [data-testid="stFileUploaderDropzone"] button [data-testid="stMarkdownContainer"] p{font-size:0!important}
        [data-testid="stFileUploaderDropzone"] button [data-testid="stMarkdownContainer"] p::after{content:"选择文件";font-size:16px}
        [data-testid="stFileUploaderDropzoneInstructions"] span{font-size:0!important}
        [data-testid="stFileUploaderDropzoneInstructions"] span::after{content:"每个文件 ≤50 MiB · CSV、JSON、JSONL、TXT、PDF、ZIP";font-size:12px}
        </style>""")
