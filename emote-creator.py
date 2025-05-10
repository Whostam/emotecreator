import streamlit as st
from PIL import Image, ImageDraw
import io
import math
import random

# Constants
BASE_SIZE = 400
SCALE = 4  # antialias multiplier
TRUE_SIZE = BASE_SIZE * SCALE

# Ensure session_state defaults exist
def initialize_state():
    defaults = {
        'thickness': 15,               # Fixed default thickness
        'body_color': '#2AFF00',
        'body_style': 'Outline',       # Fixed outline body style
        'eye_color': '#2AFF00',
        'eye_style': 'Filled',
        'eye_shape': 'Open',
        'mouth_color': '#2AFF00',
        'mouth_style': 'Smile',
        'brow_color': '#2AFF00',
        'brow_style': 'None',
        'res': '400x400',
        'formats': []
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# Randomize callback
def randomize():
    st.session_state['thickness'] = random.randint(1, 20)
    st.session_state['body_color'] = f"#{random.randint(0,0xFFFFFF):06x}"
    st.session_state['eye_color'] = f"#{random.randint(0,0xFFFFFF):06x}"
    st.session_state['mouth_color'] = f"#{random.randint(0,0xFFFFFF):06x}"
    st.session_state['brow_color'] = f"#{random.randint(0,0xFFFFFF):06x}"
    # body_style remains Outline
    st.session_state['eye_style'] = random.choice(['Filled','Outline'])
    st.session_state['eye_shape'] = random.choice(['Open','Closed','Wink','Happy','Sad','Surprised','Sleepy','Angry','Excited','Dazed'])
    st.session_state['mouth_style'] = random.choice(['Smile','Frown','Neutral','Surprised','Tongue','Laugh','Sad','OpenSmile','Grimace','Oops'])
    st.session_state['brow_style'] = random.choice(['None','Straight','Angled','Raised','Sad','Frown','Rounded','Zigzag'])

# Drawing function
def draw_emote(body_color, body_style,
               eye_color, eye_style, eye_shape,
               mouth_color, mouth_style,
               brow_color, brow_style,
               thickness):
    img = Image.new('RGBA', (TRUE_SIZE, TRUE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = TRUE_SIZE // 2, TRUE_SIZE // 2
    r = (BASE_SIZE // 2 - 10) * SCALE
    t = thickness * SCALE

    # Body
    bbox = [(cx-r, cy-r), (cx+r, cy+r)]
    draw.ellipse(bbox, outline=body_color, width=t)

    # Eye helper (star for excited)
    def star(center, radius, color):
        pts=[]
        for i in range(5):
            ang = math.radians(90 + i*72)
            pts.append((center[0]+radius*math.cos(ang), center[1]-radius*math.sin(ang)))
            ang = math.radians(126 + i*72)
            pts.append((center[0]+radius*0.4*math.cos(ang), center[1]-radius*0.4*math.sin(ang)))
        draw.polygon(pts, fill=color)

    # Eyes
    eye_r = int(r * 0.15)
    offs = (r * 0.5, -r * 0.2)
    for idx, pos in enumerate([(cx-offs[0], cy+offs[1]), (cx+offs[0], cy+offs[1])]):
        ex, ey = pos
        bb = [(ex-eye_r, ey-eye_r), (ex+eye_r, ey+eye_r)]
        if eye_shape == 'Open':
            if eye_style == 'Filled': draw.ellipse(bb, fill=eye_color)
            else: draw.ellipse(bb, outline=eye_color, width=t)
        elif eye_shape == 'Closed': draw.arc(bb, 0, 180, fill=eye_color, width=t)
        elif eye_shape == 'Wink':
            if idx == 0: draw.arc(bb, 0, 180, fill=eye_color, width=t)
            else: draw.ellipse(bb, fill=eye_color)
        elif eye_shape == 'Happy': draw.arc(bb, 0, 180, fill=eye_color, width=t)
        elif eye_shape == 'Sad': draw.arc(bb, 180, 360, fill=eye_color, width=t)
        elif eye_shape == 'Surprised': draw.ellipse(bb, outline=eye_color, width=t)
        elif eye_shape == 'Sleepy': draw.arc(bb, 30, 150, fill=eye_color, width=t)
        elif eye_shape == 'Angry': draw.line([(ex-eye_r, ey+eye_r), (ex, ey-eye_r/2), (ex+eye_r, ey+eye_r)], fill=eye_color, width=t)
        elif eye_shape == 'Excited': star((ex, ey), eye_r, eye_color)
        elif eye_shape == 'Dazed':
            for i in range(4): draw.arc([(ex-i*eye_r*0.1, ey-i*eye_r*0.1), (ex+i*eye_r*0.1, ey+i*eye_r*0.1)], 0, 270, fill=eye_color, width=1)

    # Mouth
    mx, my = cx, cy + r * 0.4
    mw, mh = r * 0.5, r * 0.2
    if mouth_style == 'Smile': draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 0, 180, fill=mouth_color, width=t)
    elif mouth_style == 'Frown': draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 180, 360, fill=mouth_color, width=t)
    elif mouth_style == 'Neutral': draw.line([(mx-mw, my), (mx+mw, my)], fill=mouth_color, width=t)
    # ... other mouth styles remain unchanged for brevity ...

    # Eyebrows
    off = r * 0.35
    bl = eye_r * 1.2
    if brow_style != 'None':
        yb = cy + off - r * 0.2
        if brow_style == 'Straight': draw.line([(cx-bl, yb), (cx+bl, yb)], fill=brow_color, width=t)
        # ... other eyebrow styles unchanged for brevity ...

    return img.resize((BASE_SIZE, BASE_SIZE), resample=Image.LANCZOS)

# SVG stub
 def generate_svg(params):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{BASE_SIZE}" height="{BASE_SIZE}"></svg>'

# Init state
initialize_state()

# Sidebar UI
st.sidebar.title('Emote Creator')
st.sidebar.button('Randomize', on_click=randomize)

# Fixed thickness, no slider
# Fixed body style 'Outline', no selector

st.sidebar.subheader('Eyes')
eye_color = st.sidebar.color_picker('Eye color', key='eye_color')
eye_style = st.sidebar.selectbox('Eye style', ['Filled','Outline'], key='eye_style')
eye_shape = st.sidebar.selectbox('Eye shape', ['Open','Closed','Wink','Happy','Sad','Surprised','Sleepy','Angry','Excited','Dazed'], key='eye_shape')

st.sidebar.subheader('Mouth')
mouth_color = st.sidebar.color_picker('Mouth color', key='mouth_color')
mouth_style = st.sidebar.selectbox('Mouth type', ['Smile','Frown','Neutral','Surprised','Tongue','Laugh','Sad','OpenSmile','Grimace','Oops'], key='mouth_style')

st.sidebar.subheader('Eyebrows')
brow_color = st.sidebar.color_picker('Brow color', key='brow_color')
brow_style = st.sidebar.selectbox('Eyebrow style', ['None','Straight','Angled','Raised','Sad','Frown','Rounded','Zigzag'], key='brow_style')

# Draw and display
img = draw_emote(
    st.session_state['body_color'], 'Outline',
    st.session_state['eye_color'], st.session_state['eye_style'], st.session_state['eye_shape'],
    st.session_state['mouth_color'], st.session_state['mouth_style'],
    st.session_state['brow_color'], st.session_state['brow_style'],
    st.session_state['thickness']
)
st.image(img, use_container_width=True)

# Download options
st.sidebar.subheader('Download')
res = st.sidebar.selectbox('Resolution', ['400x400','800x800','1200x1200'], key='res')
formats = st.sidebar.multiselect('Formats', ['PNG','SVG'], key='formats')
if formats:
    cols = st.sidebar.columns(len(formats))
    for fmt, col in zip(formats, cols):
        if fmt == 'PNG':
            w, h = map(int, st.session_state['res'].split('x'))
            buf = io.BytesIO(); img.resize((w,h)).save(buf, format='PNG')
            col.download_button('Download PNG', buf.getvalue(), file_name=f'emote_{w}x{h}.png', mime='image/png')
        else:
            svg = generate_svg(st.session_state)
            col.download_button('Download SVG', svg, file_name='emote.svg', mime='image/svg+xml')
