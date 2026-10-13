import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="✨",
    layout="wide",
)

st.title("Hello World Motion Lab")
st.caption("A tiny app-building playground: enter a name, style it, and add looping motion effects.")

# Keep the dependency list intentionally minimal: Streamlit only.
st.sidebar.header("Customize your app")

name = st.sidebar.text_input("Your name or message", value="Hello World", max_chars=80)
font_family = st.sidebar.selectbox(
    "Font family",
    ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Comic Sans MS", "Impact"],
)
font_size = st.sidebar.slider("Font size", min_value=20, max_value=100, value=52, step=2)
font_weight = st.sidebar.selectbox("Font weight", ["Normal", "Bold"])
name_mode = st.sidebar.selectbox("Name display", ["Centered", "Ticker tape", "Repeated"])
background = st.sidebar.selectbox(
    "Background",
    ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Starry night"],
)
effect = st.sidebar.selectbox(
    "Looping effect",
    ["None", "Rain", "Snow", "Hail", "Wind gusts", "Confetti", "Tornado"],
)
speed = st.sidebar.slider("Animation speed", min_value=1, max_value=10, value=5,
                          help="1 is slow and 10 is fast.")

# Values are selected from fixed allow-lists. Escape user-entered text before placing it in HTML.
safe_name = html.escape(name or "Hello World")
safe_font = html.escape(font_family, quote=True)
font_weight_css = "700" if font_weight == "Bold" else "400"

backgrounds = {
    "Light": ("#f7f8fc", "#172033"),
    "Dark": ("#10131a", "#ffffff"),
    "Ocean": ("linear-gradient(135deg, #063970, #0ea5a4)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg, #ff9966, #ff5e62)", "#2b1020"),
    "Forest": ("linear-gradient(135deg, #12372a, #436850)", "#ffffff"),
    "Lavender": ("linear-gradient(135deg, #e9d5ff, #c4b5fd)", "#31204f"),
    "Starry night": ("radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%)", "#ffffff"),
}
bg_css, text_color = backgrounds[background]
speed_seconds = round(11 - speed, 1) / 2.5  # 0.4s–4.0s; higher setting is faster

effect_classes = {
    "None": "",
    "Rain": "rain",
    "Snow": "snow",
    "Hail": "hail",
    "Wind gusts": "wind",
    "Confetti": "confetti",
    "Tornado": "tornado",
}
effect_class = effect_classes[effect]

# Generate decorative particles in HTML. CSS animations run in the embedded browser frame,
# so the Streamlit script does not need an infinite rerun loop.
particles = ""
if effect == "Rain":
    particles = "".join(
        f'<span class="particle rain-drop" style="left:{(i * 17) % 100}%; animation-delay:-{(i % 13) * 0.23}s; animation-duration:{speed_seconds + (i % 4) * 0.16}s;"></span>'
        for i in range(42)
    )
elif effect == "Snow":
    particles = "".join(
        f'<span class="particle snowflake" style="left:{(i * 23) % 100}%; font-size:{10 + (i % 5) * 4}px; animation-delay:-{(i % 17) * 0.31}s; animation-duration:{speed_seconds * 2 + (i % 5) * 0.5}s;">❄</span>'
        for i in range(34)
    )
elif effect == "Hail":
    particles = "".join(
        f'<span class="particle hailstone" style="left:{(i * 19) % 100}%; animation-delay:-{(i % 11) * 0.22}s; animation-duration:{speed_seconds + (i % 3) * 0.2}s;"></span>'
        for i in range(32)
    )
elif effect == "Wind gusts":
    particles = "".join(
        f'<span class="particle wind-line" style="top:{8 + (i * 13) % 85}%; animation-delay:-{(i % 9) * 0.4}s; animation-duration:{speed_seconds * 2 + (i % 4) * 0.35}s; width:{45 + (i % 6) * 24}px;"></span>'
        for i in range(20)
    )
elif effect == "Confetti":
    colors = ["#ff4d6d", "#ffd166", "#06d6a0", "#4cc9f0", "#c77dff", "#ffffff"]
    particles = "".join(
        f'<span class="particle confetti-bit" style="left:{(i * 29) % 100}%; background:{colors[i % len(colors)]}; animation-delay:-{(i % 15) * 0.27}s; animation-duration:{speed_seconds * 2 + (i % 4) * 0.45}s; transform:rotate({i * 37}deg);"></span>'
        for i in range(48)
    )
elif effect == "Tornado":
    particles = '<div class="tornado-funnel">' + "".join(
        f'<span style="--i:{i}; animation-duration:{speed_seconds * 2.2}s;"></span>' for i in range(13)
    ) + "</div>"

if name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(
        f'<div class="name-line">{safe_name}</div>' for _ in range(5)
    ) + "</div>"
elif name_mode == "Ticker tape":
    name_markup = f'<div class="ticker"><div class="ticker-track"><span>{safe_name}</span><span aria-hidden="true">{safe_name}</span></div></div>'
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

html_page = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ font-family: {safe_font}, sans-serif; }}
  .stage {{
    position: relative; isolation: isolate; overflow: hidden;
    height: 590px; width: 100%; border-radius: 18px;
    background: {bg_css}; color: {text_color};
    display: flex; align-items: center; justify-content: center;
  }}
  .effect-layer {{ position: absolute; inset: 0; overflow: hidden; z-index: 1; pointer-events: none; }}
  .name-layer {{
    position: relative; z-index: 2; width: 100%; padding: 24px;
    font-size: {font_size}px; font-weight: {font_weight_css};
    text-align: center; overflow: hidden;
    text-shadow: 0 2px 12px rgba(0,0,0,.15);
  }}
  .center-name {{ overflow-wrap: anywhere; }}
  .repeated {{ display: flex; flex-direction: column; gap: .12em; }}
  .name-line {{ line-height: 1.05; overflow-wrap: anywhere; }}
  .ticker {{ overflow: hidden; width: 100%; }}
  .ticker-track {{ display: flex; width: max-content; gap: 1.5em; animation: ticker-scroll {max(5, speed_seconds * 5)}s linear infinite; }}
  .ticker-track span {{ white-space: nowrap; }}
  @keyframes ticker-scroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
  .particle {{ position: absolute; display: block; }}
  .rain-drop {{ top: -35px; height: 28px; width: 2px; background: rgba(100,190,255,.8); box-shadow: 0 0 5px rgba(100,190,255,.4); animation: rain-fall linear infinite; }}
  @keyframes rain-fall {{ to {{ transform: translate3d(-25px, 680px, 0); }} }}
  .snowflake {{ top: -35px; color: #fff; text-shadow: 0 0 5px #7aa9df; animation: snow-fall linear infinite; }}
  @keyframes snow-fall {{ 50% {{ transform: translate(35px, 300px) rotate(180deg); }} to {{ transform: translate(-15px, 650px) rotate(360deg); }} }}
  .hailstone {{ top: -20px; width: 7px; height: 7px; border-radius: 50%; background: #d9f4ff; box-shadow: 0 0 5px #fff; animation: hail-fall linear infinite; }}
  @keyframes hail-fall {{ to {{ transform: translate(22px, 680px); }} }}
  .wind-line {{ left: -180px; height: 2px; border-radius: 99px; background: rgba(255,255,255,.65); box-shadow: 0 0 8px rgba(255,255,255,.25); animation: wind-blow linear infinite; }}
  @keyframes wind-blow {{ from {{ transform: translateX(0) scaleX(.65); opacity: 0; }} 15%, 75% {{ opacity: .9; }} to {{ transform: translateX(120vw) scaleX(1.2); opacity: 0; }} }}
  .confetti-bit {{ top: -20px; width: 9px; height: 15px; border-radius: 2px; animation: confetti-fall linear infinite; }}
  @keyframes confetti-fall {{ to {{ transform: translate3d(40px, 680px, 0) rotate(900deg); }} }}
  .tornado-funnel {{ position: absolute; left: 50%; top: 50%; width: 270px; height: 410px; transform: translate(-50%, -50%); opacity: .68; }}
  .tornado-funnel span {{ position: absolute; left: 50%; top: calc(8% + var(--i) * 6.4%); width: calc(30px + var(--i) * 15px); height: 12px; border: 3px solid rgba(220,240,255,.9); border-left-color: transparent; border-radius: 50%; transform: translateX(-50%); animation: twister-spin linear infinite; }}
  @keyframes twister-spin {{ from {{ rotate: 0deg; }} to {{ rotate: 360deg; }} }}
  @media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{ animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; }}
  }}
</style>
</head>
<body>
  <main class="stage">
    <div class="effect-layer {effect_class}">{particles}</div>
    <div class="name-layer">{name_markup}</div>
  </main>
</body>
</html>
"""

components.html(html_page, height=610, scrolling=False)
st.caption("Tip: change the controls in the sidebar to experiment. Motion loops in the preview without repeatedly rerunning the Streamlit app.")
