"""Public bilingual narrative; trusted animation only observes fixed markup."""

from html import escape
from math import cos, radians, sin

from datascout.ui_i18n import t
from datascout.ui_theme import icon

_HOME_SCRIPT = """
(()=>{
  const root=document.getElementById('ds-home-story');
  if(!root)return;
  const fill=root.querySelector('.ds-read-fill');
  let scrollElement=document.scrollingElement;
  for(let el=root.parentElement;el;el=el.parentElement){
    const overflow=getComputedStyle(el).overflowY;
    if((overflow==='auto'||overflow==='scroll')&&el.scrollHeight>el.clientHeight+1){
      scrollElement=el;break;
    }
  }
  const target=scrollElement===document.scrollingElement?window:scrollElement;
  let resizeObserver;
  const update=()=>{
    if(!root.isConnected){
      target.removeEventListener('scroll',update);
      window.removeEventListener('resize',update);
      resizeObserver?.disconnect();return;
    }
    const total=scrollElement.scrollHeight-scrollElement.clientHeight;
    const ratio=total>0?Math.max(0,Math.min(1,scrollElement.scrollTop/total)):1;
    fill.style.width=(ratio*100)+'%';
  };
  target.addEventListener('scroll',update,{passive:true});
  window.addEventListener('resize',update);
  if('ResizeObserver' in window){resizeObserver=new ResizeObserver(update);resizeObserver.observe(root);}
  update();
  if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;
  const sections=root.querySelectorAll('.ds-reveal');
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(entry.isIntersecting){
      entry.target.classList.remove('ds-wait');entry.target.classList.add('ds-visible');
    }else if(entry.target.getBoundingClientRect().top>innerHeight*.75){
      entry.target.classList.remove('ds-visible');entry.target.classList.add('ds-wait');
    }
  }),{threshold:.12});
  sections.forEach(el=>{
    if(el.getBoundingClientRect().top>innerHeight)el.classList.add('ds-wait');
    observer.observe(el);
  });
})();
"""

# Stylized geographic outlines, projected into a dot globe locally without image requests.
_LAND = (
    ((-168, 70), (-130, 72), (-105, 82), (-60, 55), (-80, 25), (-96, 17), (-117, 32), (-145, 58)),
    ((-82, 12), (-53, 5), (-35, -7), (-48, -30), (-69, -55), (-78, -28)),
    ((-17, 36), (8, 38), (36, 30), (50, 10), (40, -13), (20, -35), (9, -18), (-9, 5)),
    ((-11, 36), (-10, 58), (12, 71), (40, 68), (65, 55), (43, 37), (20, 35)),
    ((-55, 60), (-45, 60), (-20, 80), (-45, 84), (-65, 75)),
    ((40, 35), (35, 65), (80, 75), (140, 66), (170, 55), (130, 20), (100, 4), (70, 10)),
)


def _globe_dots():
    dots = []
    for latitude in range(-60, 85, 4):
        for longitude in range(-160, 85, 4):
            inside = False
            for polygon in _LAND:
                crossed = False
                previous = polygon[-1]
                for current in polygon:
                    x1, y1 = previous
                    x2, y2 = current
                    if (y1 > latitude) != (y2 > latitude):
                        boundary = (x2 - x1) * (latitude - y1) / (y2 - y1) + x1
                        if longitude < boundary:
                            crossed = not crossed
                    previous = current
                inside = inside or crossed
            lat, lon = radians(latitude), radians(longitude + 25)
            depth = cos(lat) * cos(lon)
            if not inside or depth < 0.03:
                continue
            x = 50 + 47 * cos(lat) * sin(lon)
            y = 50 - 47 * sin(lat)
            dots.append(
                f'<i style="left:{x:.2f}%;top:{y:.2f}%;opacity:{0.25 + 0.7 * depth:.2f}"></i>'
            )
    return "".join(dots)


_GLOBE_DOTS = _globe_dots()

_HOME_STYLE = """<style>
.ds-home{padding-top:24px}.ds-home h1,.ds-home h2,.ds-home h3{color:#f5f0ff}
.ds-home p{font-size:18px;line-height:1.85;color:#beb3d0;margin:20px 0;max-width:720px}
.ds-home h1{font-size:clamp(52px,6.5vw,92px);line-height:1.08;font-weight:650;letter-spacing:-.065em;margin:22px 0 26px}
.ds-home h1 em,.ds-home h2 em{font-style:normal;color:#c8afff}
.ds-kicker{font-size:12px;font-weight:650;letter-spacing:.15em;text-transform:uppercase;color:#c8afff}
.ds-hero{display:grid;grid-template-columns:1.03fr 1fr;gap:24px;align-items:center;min-height:610px}
.ds-hero-copy{position:relative;z-index:1}.ds-hero-copy p{max-width:590px}
.ds-globe-stage{position:relative;aspect-ratio:1;min-width:0;isolation:isolate;display:grid;place-items:center;perspective:900px}
.ds-globe-stage:before{content:"";position:absolute;inset:-12%;background:radial-gradient(ellipse,#8c57e62b,transparent 66%);z-index:-1}
.ds-globe{position:absolute;width:78%;height:78%;border-radius:50%;border:1px solid #bd9bf54a;overflow:hidden;background:radial-gradient(circle at 34% 28%,#593c7a65,#241832 53%,#0b0917 83%);box-shadow:inset -26px -15px 58px #03020a,0 0 85px #965aff18;animation:ds-globe-turn 14s ease-in-out infinite}
.ds-globe i{position:absolute;width:3px;height:3px;background:#d2b6ff;border-radius:50%;box-shadow:0 0 4px #b68aff70}
.ds-globe:before{content:"";position:absolute;inset:0;border-radius:50%;background:linear-gradient(135deg,#d6bfff13,transparent 45%);z-index:1}
.ds-meridian{position:absolute;top:0;height:100%;left:30%;width:40%;border:1px solid #bca0e428;border-radius:50%}.ds-meridian.wide{left:12%;width:76%}
.ds-parallel{position:absolute;top:30%;left:0;height:40%;width:100%;border:1px solid #bca0e42e;border-radius:50%}.ds-parallel.wide{top:12%;height:76%}
.ds-network-orbit{position:absolute;width:99%;height:42%;border:1px solid #c8a5ff4a;border-radius:50%;transform:rotate(-26deg);box-shadow:0 0 22px #b59aff0a;animation:ds-orbit-turn 18s linear infinite}
.ds-network-orbit.second{width:97%;height:57%;transform:rotate(41deg);border-color:#a17bc32f;animation:ds-orbit-turn 22s linear infinite reverse}
.ds-network-orbit:after{content:"";position:absolute;top:21%;left:6%;width:7px;height:7px;border-radius:50%;background:#dec6ff;box-shadow:0 0 16px 4px #bb8bff70;animation:ds-beacon 4s ease-in-out infinite}
.ds-signal{position:absolute;width:10px;height:10px;border-radius:50%;background:#dbbdff;box-shadow:0 0 20px 5px #af78ff80;z-index:2}
.ds-signal.one{top:34%;left:46%}.ds-signal.two{top:58%;left:37%}.ds-signal.three{top:43%;left:67%}
.ds-data-packet{position:absolute;z-index:3;pointer-events:none;opacity:0;animation:ds-packet-rise 5s cubic-bezier(.18,.66,.25,1) infinite;}
.ds-data-packet.one{top:34%;left:46%;--dx:-80px;--dy:-95px;animation-delay:0s}
.ds-data-packet.two{top:58%;left:37%;--dx:-110px;--dy:-65px;animation-delay:1.7s}
.ds-data-packet.three{top:43%;left:67%;--dx:75px;--dy:-85px;animation-delay:3.3s}
.ds-data-packet i{display:block;width:2px;height:36px;margin:0 auto;background:linear-gradient(transparent,#c9a7ffcc);box-shadow:0 0 13px #a56eff80;transform:rotate(-20deg);transform-origin:bottom}
.ds-data-packet b{display:block;margin-top:-38px;margin-left:13px;padding:5px 7px;border:1px solid #a882d484;border-radius:6px;background:#201433e8;color:#eadcff;font:11px Consolas,monospace;letter-spacing:.1em;box-shadow:0 0 18px #a56eff45;white-space:nowrap}
.ds-globe-tag{position:absolute;z-index:3;border:1px solid #9271b957;border-radius:13px;background:#181124dc;box-shadow:0 14px 40px #0004;padding:12px 18px;backdrop-filter:blur(16px);color:#eee5ff;font-size:14px;display:flex;gap:10px;align-items:center}
.ds-globe-tag.source{top:17%;right:0}.ds-globe-tag.proof{bottom:18%;left:0}.ds-globe-tag.decision{bottom:7%;right:7%}
.ds-globe-label{position:absolute;top:4%;left:9%;color:#a58abd;font:11px Consolas,monospace;letter-spacing:.15em}
@keyframes ds-beacon{50%{opacity:.5;box-shadow:0 0 22px 7px #bb8bff45}}
@keyframes ds-globe-turn{0%,100%{transform:rotateY(-18deg)}50%{transform:rotateY(18deg)}}
@keyframes ds-orbit-turn{to{transform:rotate(334deg)}}
@keyframes ds-packet-rise{0%,8%{opacity:0;transform:translate(0,0) scale(.72)}22%,68%{opacity:1}100%{opacity:0;transform:translate(var(--dx),var(--dy)) scale(1)}}
.ds-read-progress{position:fixed;top:0;left:0;width:100%;height:3px;background:#b59aff0d;z-index:100;pointer-events:none}
.ds-read-fill{display:block;height:100%;width:0;background:#c5a6ff;box-shadow:0 0 9px #b59aff88;transition:width .12s linear}
.ds-section{padding:110px 0;border-bottom:1px solid #b59aff18}.ds-section:last-child{border:0;padding-bottom:36px}
.ds-home h2{font-size:clamp(38px,4.7vw,64px);line-height:1.16;letter-spacing:-.055em;font-weight:620;margin:20px 0 30px;max-width:1000px}
.ds-section-head{max-width:850px;margin-bottom:44px}.ds-section-head p{max-width:750px}
.ds-home-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}.ds-home-grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.ds-home .ds-card{padding:32px;min-height:240px}.ds-home .ds-card h3{font-size:25px;line-height:1.3}.ds-home .ds-card p{font-size:17px;margin-bottom:0}
.ds-number{font:14px Consolas,monospace;color:#c8afff;display:block;margin-bottom:28px;letter-spacing:.12em}
.ds-demo-shell{border:1px solid #695080;border-radius:24px;background:linear-gradient(135deg,#2b1e3e,#140e21);overflow:hidden;box-shadow:0 24px 100px #0003}
.ds-demo-bar{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;padding:20px 28px;border-bottom:1px solid #6650775c;color:#cdb8ec;font-size:13px}
.ds-demo-layout{display:grid;grid-template-columns:.85fr 1.4fr;gap:0}.ds-demo-request{padding:36px;border-right:1px solid #6650775c}.ds-demo-request h3{font-size:26px;margin-top:16px}
.ds-demo-request p{font-size:17px}.ds-chip{display:inline-block;border:1px solid #8d70ae5e;border-radius:24px;padding:7px 12px;margin:4px 3px 4px 0;color:#d1bee8;font-size:13px}
.ds-demo-results{padding:28px}.ds-result-row{display:grid;grid-template-columns:36px 1fr;gap:16px;padding:22px 0;border-bottom:1px solid #69508050}.ds-result-row:last-child{border:0}
.ds-result-row strong{font-size:18px;display:block;color:#eee4ff}.ds-result-row p{font-size:15px;margin:7px 0 0;line-height:1.75}
.ds-home .ds-note{font-size:14px;color:#ae9cc4;line-height:1.7;margin-top:24px;max-width:900px}
.ds-category{position:relative;padding:30px;border-radius:20px;border:1px solid #58406f;background:linear-gradient(150deg,#2b203e,#171021);overflow:hidden;min-height:240px}
.ds-category:after{content:"";position:absolute;width:160px;height:160px;border:1px solid #b798ee1f;border-radius:50%;right:-38px;top:-55px;box-shadow:0 0 0 22px #b798ee07,0 0 0 44px #b798ee04;pointer-events:none}
.ds-category h3{font-size:26px;margin:36px 0 12px}.ds-category p{font-size:16px;margin:0}.ds-category small{font-size:12px;color:#c5a7ee;letter-spacing:.08em}
.ds-evidence{display:grid;grid-template-columns:1.05fr 1fr;gap:44px;align-items:center}.ds-evidence-sheet{border:1px solid #695080;border-radius:22px;background:#1a1329;padding:34px;box-shadow:20px 20px 0 #b59aff06}
.ds-evidence-sheet h3{font-size:24px;margin:16px 0 24px}.ds-evidence-item{padding:20px 0;border-top:1px solid #5d447344}.ds-evidence-item strong{font-size:15px;color:#c9acf5}.ds-evidence-item p{font-size:16px;margin:8px 0 0}
.ds-license-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.ds-license{padding:38px;border:1px solid #654d7d;border-radius:22px;background:#1a1229}.ds-license h3{font-size:30px;margin:18px 0}.ds-license p{font-size:17px}.ds-license ul{padding-left:20px;color:#c0b3d0;font-size:16px;line-height:2.15}
.ds-license.highlight{background:linear-gradient(145deg,#352343,#1b1229);border-color:#a481cf}
.ds-role{padding:38px;border-radius:22px;background:linear-gradient(140deg,#2c203e,#171020);border:1px solid #604779}.ds-role h3{font-size:32px;margin:22px 0}.ds-role p{font-size:18px}.ds-role .ds-role-detail{font-size:15px;color:#cbb5e8;margin-top:30px}
.ds-finale{text-align:center;padding-top:150px!important;position:relative}.ds-finale:before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(ellipse at 50% 90%,#a274dd21,transparent 65%)}
.ds-finale h2{font-size:clamp(44px,5.8vw,80px);max-width:1000px;margin:25px auto}.ds-finale p{margin:24px auto;max-width:700px}
.st-key-home_login button,.st-key-home_bottom button{width:100%;min-height:76px!important;border-radius:18px!important;background:linear-gradient(110deg,#ba98ff,#dec9ff)!important;color:#1b102c!important;border:1px solid #e4d3ff!important;box-shadow:0 10px 42px #b59aff22!important}
.st-key-home_login button p,.st-key-home_bottom button p{font-size:22px!important;font-weight:650!important}.st-key-home_catalog button{width:100%;min-height:54px!important;border-radius:14px!important;font-size:16px!important}
.ds-reveal{transform-origin:center 35%;transition:opacity 1050ms ease,transform 1050ms cubic-bezier(.14,.75,.18,1),filter 1050ms ease}.ds-reveal.ds-wait{opacity:.08;transform:translateY(110px) scale(.88);filter:blur(10px)}.ds-reveal.ds-visible{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}
@media(max-width:900px){.ds-hero{min-height:500px}.ds-home h1{font-size:58px}.ds-globe-tag{padding:10px;font-size:12px}.ds-globe-tag .ds-icon{width:18px;height:18px;transform:scale(.75)}.ds-home-grid{grid-template-columns:1fr}.ds-demo-layout{grid-template-columns:1fr}.ds-demo-request{border-right:0;border-bottom:1px solid #6650775c}.ds-section{padding:80px 0}}
@media(max-width:650px){.ds-hero{grid-template-columns:1fr;gap:0}.ds-hero-copy{padding-top:20px}.ds-home h1{font-size:clamp(45px,10vw,64px)}.ds-home h2{font-size:38px}.ds-home p{font-size:17px}.ds-globe-stage{width:100%;max-width:460px;margin:10px auto;min-height:320px}.ds-home-grid.two,.ds-evidence,.ds-license-grid{grid-template-columns:1fr}.ds-section{padding:65px 0}.ds-home .ds-card,.ds-role,.ds-license,.ds-evidence-sheet{padding:26px}.ds-finale{padding-top:90px!important}.ds-demo-request{padding:26px}.ds-demo-results{padding:18px 26px}.ds-demo-bar{padding:18px 26px}.st-key-home_login button p,.st-key-home_bottom button p{font-size:18px!important}}
@media(prefers-reduced-motion:reduce){.ds-reveal.ds-wait{opacity:1;transform:none;filter:none}.ds-network-orbit,.ds-globe{animation:none}.ds-data-packet{animation:none;opacity:.75;transform:translate(var(--dx),var(--dy))}.ds-network-orbit:after{animation:none}.ds-reveal{transition:none}}
</style>"""


def render_home(st, *, signed_in=False, preview_only=False):
    def text(zh, en):
        return escape(t(st, zh, en))

    st.html(_HOME_STYLE)
    st.html(f"""<div class="ds-home"><section class="ds-hero" data-story="positioning">
    <div class="ds-hero-copy"><div class="ds-kicker">{text("从数据，到有据可循的决策", "From data to decisions you can explain")}</div>
    <h1>{text("世界有数据。", "A world of data.")}<br><em>{text("你需要答案。", "Your next answer.")}</em></h1>
    <p>{text("把需求、数据来源与许可放在同一个判断过程里。找到值得深入了解的数据，让每一次选择，都有清晰的依据。", "Bring your needs, data sources and usage rights into one decision. Discover data worth a closer look, with clear reasons behind every choice.")}</p>
    </div><div class="ds-globe-stage" aria-hidden="true"><span class="ds-globe-label">DATA SCOUT / 01</span>
    <div class="ds-network-orbit"></div><div class="ds-network-orbit second"></div>
    <div class="ds-globe">{_GLOBE_DOTS}<span class="ds-meridian"></span><span class="ds-meridian wide"></span><span class="ds-parallel"></span><span class="ds-parallel wide"></span></div>
    <span class="ds-signal one"></span><span class="ds-signal two"></span><span class="ds-signal three"></span>
    <span class="ds-data-packet one"><i></i><b>001 101</b></span>
    <span class="ds-data-packet two"><i></i><b>110 010</b></span>
    <span class="ds-data-packet three"><i></i><b>011 100</b></span>
    <div class="ds-globe-tag source">{icon("file")}{text("发现来源", "Discover sources")}</div>
    <div class="ds-globe-tag proof">{icon("evidence")}{text("追溯证据", "Trace evidence")}</div>
    <div class="ds-globe-tag decision">{icon("search")}{text("判断适配", "Find your fit")}</div>
    </div></section></div>""")
    if st.button(
        t(st, "浏览数据集广场 →", "Explore the dataset marketplace →")
        if preview_only
        else (
            t(st, "进入我的工作空间 →", "Open my workspace →")
            if signed_in
            else t(st, "开始探索 · 登录 / 注册 →", "Start exploring · Sign in / Register →")
        ),
        key="home_login",
        icon=":material/arrow_forward:",
        type="primary",
    ):
        st.session_state["page"] = (
            "catalog" if preview_only else ("buyer" if signed_in else "login")
        )
        st.rerun()
    if st.button(
        t(st, "先浏览数据目录 →", "Browse the catalog →"),
        key="home_catalog",
        icon=":material/search:",
    ):
        st.session_state["page"] = "catalog"
        st.rerun()
    st.caption(
        t(
            st,
            "公开预览 · 仅展示公开目录，不提供账户、上传或在线评估"
            if preview_only
            else "本地工作空间 · 上传不自动发送给模型 · 可选 GPT 在线评估或离线示例",
            "Public preview · Browse public metadata; accounts, uploads and online analysis are unavailable"
            if preview_only
            else "Local workspace · Uploads are not automatically sent to a model · Choose online GPT analysis or the offline example",
        )
    )

    pain_cards = "".join(
        f'<article class="ds-card"><span class="ds-number">0{i}</span><h3>{text(zh, en)}</h3><p>{text(body_zh, body_en)}</p></article>'
        for i, (zh, en, body_zh, body_en) in enumerate(
            [
                (
                    "找到了，却不一定适合。",
                    "Available. But is it suitable?",
                    "同一个任务，可能需要不同地域、时间与标注。名称相似的数据集，未必能回答相同的问题。",
                    "A task can depend on geography, collection dates and annotation detail. Similar dataset names can hide very different coverage.",
                ),
                (
                    "有描述，却缺少依据。",
                    "Described. But is it supported?",
                    "一个评分无法替代原始说明。把来源、限制与待核验项一起看，才知道下一步该检查什么。",
                    "A score cannot replace the source material. See the evidence, limitations and open questions together to know what to check next.",
                ),
                (
                    "能下载，不等于能使用。",
                    "Downloadable. But can you use it?",
                    "公开获取、研究用途与商业授权是不同的边界。预算之外，还需要确认许可与实际样本质量。",
                    "Public access, research use and commercial permission have different boundaries. Check the license and actual samples alongside your budget.",
                ),
            ],
            1,
        )
    )
    result_rows = "".join(
        f'<div class="ds-result-row">{icon(symbol)}<div><strong>{text(zh, en)}</strong><p>{text(body_zh, body_en)}</p></div></div>'
        for symbol, zh, en, body_zh, body_en in [
            (
                "search",
                "先明确硬约束",
                "Start with hard constraints",
                "任务：行人检测 · 场景：夜间、雨天 · 必需标注：二维边界框",
                "Task: pedestrian detection · Conditions: night and rain · Required annotation: 2D boxes",
            ),
            (
                "evidence",
                "再比较来源与适配",
                "Compare sources and fit",
                "把候选数据集的采集说明、覆盖范围与原始链接放回判断过程。",
                "Compare collection notes, coverage and source links for each candidate.",
            ),
            (
                "lock",
                "保留待核验的边界",
                "Keep open questions visible",
                "商业授权：待核验 · 样本质量：未审查 · 模拟报价：不代表公开售价",
                "Commercial rights: verify · Sample quality: not audited · Simulated offers are not public prices",
            ),
        ]
    )
    categories = "".join(
        f'<article class="ds-category"><small>{text(kzh, ken)}</small><h3>{text(zh, en)}</h3><p>{text(bzh, ben)}</p></article>'
        for kzh, ken, zh, en, bzh, ben in [
            (
                "图像与场景",
                "IMAGES & SCENES",
                "计算机视觉",
                "Computer vision",
                "从道路场景到通用图像，关注任务、标注与采集条件。",
                "From road scenes to general images: examine tasks, annotations and collection conditions.",
            ),
            (
                "结构与关系",
                "STRUCTURE & RELATIONSHIPS",
                "表格数据",
                "Tabular data",
                "从字段与目标变量出发，理解样本规模、缺失值与适用边界。",
                "Start with fields and target variables, then inspect sample size, missing values and limitations.",
            ),
            (
                "时间与变化",
                "TIME & CHANGE",
                "时间序列",
                "Time series",
                "关注采样频率、时间覆盖与预测目标，找到可比较的序列。",
                "Compare sampling frequency, time coverage and forecasting targets.",
            ),
        ]
    )
    evidence = "".join(
        f'<div class="ds-evidence-item"><strong>{text(zh, en)}</strong><p>{text(bzh, ben)}</p></div>'
        for zh, en, bzh, ben in [
            (
                "来源说明",
                "Source context",
                "候选资料提到道路场景与标注信息；需要返回原始页面核对范围。",
                "Candidate material describes road scenes and annotations; check the original page for exact coverage.",
            ),
            (
                "适配判断",
                "Fit assessment",
                "任务描述相关；夜间与雨天覆盖仍需代表性样本验证。",
                "The described task is relevant; night and rain coverage still needs representative samples.",
            ),
            (
                "下一步行动",
                "Next action",
                "查看原始许可，审查样本，再决定是否继续洽谈。",
                "Read the original license, audit samples, then decide whether to discuss terms.",
            ),
        ]
    )
    content = f"""<div id="ds-home-story" class="ds-home"><div class="ds-read-progress" aria-hidden="true"><span class="ds-read-fill"></span></div>
    <section class="ds-section ds-reveal" data-story="pain"><div class="ds-section-head"><div class="ds-kicker">{text("选择数据，难在判断", "The challenge is making the choice")}</div><h2>{text("数据很多。", "So much data.")}<br><em>{text("真正合适的，需要看清。", "See what actually fits.")}</em></h2><p>{text("搜索只是起点。选择一份数据，需要同时理解它能做什么、依据是什么，以及允许如何使用。", "Search is the beginning. Choosing data means understanding what it can do, what supports that claim and how you are allowed to use it.")}</p></div><div class="ds-home-grid">{pain_cards}</div></section>
    <section class="ds-section ds-reveal" data-story="workflow"><div class="ds-section-head"><div class="ds-kicker">{text("模拟工作流", "Simulated workflow")}</div><h2>{text("一句需求。", "One clear brief.")}<br><em>{text("展开一条判断路径。", "A path to your decision.")}</em></h2><p>{text("用一个行人检测场景，了解需求如何变成约束、候选与待核验项。以下为流程演示，不代表实时检索结果。", "Follow a pedestrian detection brief from constraints to candidates and open questions. This is a workflow demonstration, not live search results.")}</p></div>
    <div class="ds-demo-shell"><div class="ds-demo-bar"><span>DataScout AI</span><span>{text("流程演示 · 模拟内容", "Workflow demo · Simulated content")}</span></div><div class="ds-demo-layout"><div class="ds-demo-request"><span class="ds-kicker">{text("你的需求", "Your brief")}</span><h3>{text("我要做夜间与雨天的行人检测。", "I need pedestrian detection data for nights and rain.")}</h3><p>{text("需要二维边界框，并希望评估商业使用条件。", "I need 2D boxes and want to assess commercial usage rights.")}</p><span class="ds-chip">{text("夜间", "Night")}</span><span class="ds-chip">{text("雨天", "Rain")}</span><span class="ds-chip">{text("商业用途待核验", "Verify commercial rights")}</span></div><div class="ds-demo-results">{result_rows}</div></div></div>
    <p class="ds-note">{text("演示不包含真实报价或成交承诺。具体结果取决于你的需求与目录中可用的材料。", "The demo contains no real quotes or transaction commitments. Actual results depend on your brief and available catalog material.")}</p></section>
    <section class="ds-section ds-reveal" data-story="categories"><div class="ds-section-head"><div class="ds-kicker">{text("数据目录预览", "A preview of the catalog")}</div><h2>{text("不同类型的数据，", "Different kinds of data.")}<br><em>{text("相同清晰的起点。", "The same clear starting point.")}</em></h2><p>{text("按任务与数据类型开始探索，再深入查看来源和说明。目录中的示例与公开数据资料，帮助你形成下一步问题。", "Explore by task and data type, then examine the sources and descriptions. Catalog examples and public dataset information help you frame the next question.")}</p></div><div class="ds-home-grid">{categories}</div></section>
    <section class="ds-section ds-reveal" data-story="evidence"><div class="ds-evidence"><div><div class="ds-kicker">{text("示例证据", "Illustrative evidence")}</div><h2>{text("看见结论。", "See the conclusion.")}<br><em>{text("也看见它的依据。", "And what supports it.")}</em></h2><p>{text("让来源与不确定性留在决策里。分项判断帮助你理解适配程度，原文与链接帮助你继续核验。", "Keep sources and uncertainty in the decision. Individual assessments explain fit; source text and links support your next verification step.")}</p><p class="ds-note">{text("右侧是说明结构的模拟示例，并非真实引用或已经完成的样本审计。", "This simulated example illustrates the evidence structure. It is not a real quotation or a completed sample audit.")}</p></div><article class="ds-evidence-sheet"><span class="ds-kicker">{text("示例评估档案", "Example assessment")}</span><h3>{text("结论有据，边界可见。", "Reasons visible. Boundaries clear.")}</h3>{evidence}</article></div></section>
    <section class="ds-section ds-reveal" data-story="licenses"><div class="ds-section-head"><div class="ds-kicker">{text("理解使用边界", "Understand the usage boundaries")}</div><h2>{text("免费获取。", "Free to access.")}<br><em>{text("许可，仍然需要读清楚。", "Still read the license.")}</em></h2><p>{text("获取成本与使用权利是两件需要分别确认的事。公开数据可以成为起点，原始许可决定具体使用边界。", "Access cost and usage rights need separate checks. Public data can be a starting point; the original license determines how it may be used.")}</p></div>
    <div class="ds-license-grid"><article class="ds-license"><span class="ds-kicker">{text("获取方式", "Access")}</span><h3>{text("找到可探索的数据", "Find data to explore")}</h3><p>{text("查看公开来源、下载说明与数据类型。先了解材料，再决定是否适合你的任务。", "Review public sources, download guidance and data types. Understand the material before deciding whether it suits your task.")}</p><ul><li>{text("公开资料与原始来源链接", "Public information and original source links")}</li><li>{text("字段、标注与覆盖说明", "Fields, annotations and coverage notes")}</li><li>{text("获取要求与已知限制", "Access requirements and known limitations")}</li></ul></article>
    <article class="ds-license highlight"><span class="ds-kicker">{text("使用权利", "Usage rights")}</span><h3>{text("确认允许的使用方式", "Confirm permitted uses")}</h3><p>{text("下载权限不能替代商业授权。没有确认的许可与质量，不会被当成已经通过。", "Download access does not establish commercial permission. Unconfirmed rights and quality remain open questions.")}</p><ul><li>{text("商业使用与研究使用", "Commercial and research use")}</li><li>{text("再分发、署名与其他条件", "Redistribution, attribution and other conditions")}</li><li>{text("代表性样本质量审查", "Representative sample quality audit")}</li></ul></article></div></section>
    <section class="ds-section ds-reveal" data-story="roles"><div class="ds-section-head"><div class="ds-kicker">{text("需求与供给，在这里相遇", "Where needs meet supply")}</div><h2>{text("为寻找数据的人。", "For people finding data.")}<br><em>{text("也为提供数据的人。", "And people offering it.")}</em></h2><p>{text("同一个本地账户，切换买方与卖方工作空间。让需求更具体，让数据档案更清晰。", "Switch between buyer and seller workspaces with one local account. Make your brief more specific and your dataset profile clearer.")}</p></div>
    <div class="ds-home-grid two"><article class="ds-role">{icon("search")}<h3>{text("找到适合任务的数据", "Find data for your task")}</h3><p>{text("描述场景、预算与必需条件。比较候选，查看分项评估与证据，再导出报告继续讨论。", "Describe the scenario, budget and requirements. Compare candidates, review assessments and evidence, then export a report for further discussion.")}</p><div class="ds-role-detail">{text("买方工作空间 · 需求 → 候选 → 评估报告", "Buyer workspace · Brief → Candidates → Report")}</div></article>
    <article class="ds-role">{icon("file")}<h3>{text("为数据建立可信档案", "Build a clear dataset profile")}</h3><p>{text("保存样本、覆盖说明与许可材料，继续完善草稿。提交后进入待审核状态，私有文件保留在本地账户中。", "Save samples, coverage notes and license material, then refine your draft. Submitted profiles are marked pending review; private files remain in your local account.")}</p><div class="ds-role-detail">{text("卖方工作空间 · 材料 → 草稿 → 待审核", "Seller workspace · Material → Draft → Pending review")}</div></article></div></section>
    <section class="ds-section ds-finale ds-reveal" data-story="finale"><div class="ds-kicker">{text("你的下一次数据选择", "Your next data decision")}</div><h2>{text("从一个问题开始。", "Begin with a question.")}<br><em>{text("让答案，更有依据。", "Choose with clearer reasons.")}</em></h2><p>{text("带来你的需求，或者一份值得被了解的数据。你的工作空间，已经准备好下一步。", "Bring a brief, or a dataset worth understanding. Your workspace is ready for the next step.")}</p></section></div>"""
    st.html(content + "<script>" + _HOME_SCRIPT + "</script>", unsafe_allow_javascript=True)
    if st.button(
        t(st, "探索公开数据目录 →", "Explore the public catalog →")
        if preview_only
        else (
            t(st, "打开我的工作空间 →", "Open my workspace →")
            if signed_in
            else t(st, "创建账户，开始使用 →", "Create an account and begin →")
        ),
        key="home_bottom",
        icon=":material/arrow_forward:",
        type="primary",
    ):
        st.session_state["page"] = (
            "catalog" if preview_only else ("buyer" if signed_in else "login")
        )
        st.rerun()
    st.caption(
        t(st, "DataScout AI · 公开预览", "DataScout AI · Public preview")
        if preview_only
        else t(st, "DataScout AI · 本地数据工作空间", "DataScout AI · Local data workspace")
    )
