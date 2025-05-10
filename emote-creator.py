import streamlit as st
from PIL import Image, ImageDraw
import io
import math

# Constants
BASE_SIZE = 400
SCALE = 4  # antialias multiplier
TRUE_SIZE = BASE_SIZE * SCALE

# Drawing function with refined aesthetics
def draw_emote(body_color, body_style,
               eye_color, eye_style, eye_shape,
               mouth_color, mouth_style,
               brow_color, brow_style,
               thickness):
    img = Image.new('RGBA', (TRUE_SIZE, TRUE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = TRUE_SIZE // 2, TRUE_SIZE // 2
    r = (BASE_SIZE//2 - 10) * SCALE
    t = thickness * SCALE

    # Body
    body_bbox = [(cx - r, cy - r), (cx + r, cy + r)]
    if body_style == 'Filled':
        draw.ellipse(body_bbox, fill=body_color)
    else:
        draw.ellipse(body_bbox, outline=body_color, width=t)

    # Eye positions
    eye_r = int(r * 0.15)
    ex_off = r * 0.5
    ey_off = -r * 0.2
    positions = [(cx - ex_off, cy + ey_off), (cx + ex_off, cy + ey_off)]

    def star(center, radius, color):
        cx_, cy_ = center
        pts = []
        for i in range(5):
            angle = math.radians(90 + i*72)
            x = cx_ + radius*math.cos(angle)
            y = cy_ - radius*math.sin(angle)
            pts.append((x,y))
            angle = math.radians(126 + i*72)
            x = cx_ + radius*0.4*math.cos(angle)
            y = cy_ - radius*0.4*math.sin(angle)
            pts.append((x,y))
        draw.polygon(pts, fill=color)

    # Draw eyes
    for idx, (ex, ey) in enumerate(positions):
        bb = [(ex-eye_r, ey-eye_r), (ex+eye_r, ey+eye_r)]
        if eye_shape == 'Open':
            if eye_style == 'Filled': draw.ellipse(bb, fill=eye_color)
            else: draw.ellipse(bb, outline=eye_color, width=t)
        elif eye_shape == 'Closed':
            draw.arc(bb, start=0, end=180, fill=eye_color, width=t)
        elif eye_shape == 'Wink':
            if idx == 0: draw.arc(bb, start=0, end=180, fill=eye_color, width=t)
            else: draw.ellipse(bb, fill=eye_color)
        elif eye_shape == 'Happy':
            draw.arc(bb, start=0, end=180, fill=eye_color, width=t)
        elif eye_shape == 'Sad':
            draw.arc(bb, start=180, end=360, fill=eye_color, width=t)
        elif eye_shape == 'Surprised':
            draw.ellipse(bb, outline=eye_color, width=t)
        elif eye_shape == 'Sleepy':
            draw.arc(bb, start=30, end=150, fill=eye_color, width=t)
        elif eye_shape == 'Angry':
            # caret shape
            draw.line([(ex-eye_r, ey+eye_r), (ex, ey-eye_r/2), (ex+eye_r, ey+eye_r)], fill=eye_color, width=t)
        elif eye_shape == 'Excited':
            star((ex, ey), eye_r, eye_color)
        elif eye_shape == 'Dazed':
            # swirl: simple spiral
            for i in range(4):
                draw.arc([(ex-i*eye_r*0.1, ey-i*eye_r*0.1), (ex+i*eye_r*0.1, ey+i*eye_r*0.1)], start=0, end=270, fill=eye_color, width=1)

    # Mouth
    mx, my = cx, cy + r*0.4
    mw, mh = r*0.5, r*0.2
    if mouth_style == 'Smile':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 0, 180, fill=mouth_color, width=t)
    elif mouth_style == 'Frown':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 180, 360, fill=mouth_color, width=t)
    elif mouth_style == 'Neutral':
        draw.line([(mx-mw, my), (mx+mw, my)], fill=mouth_color, width=t)
    elif mouth_style == 'Surprised':
        draw.ellipse([(mx-mh, my-mh), (mx+mh, my+mh)], outline=mouth_color, width=t)
    elif mouth_style == 'Tongue':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 0, 180, fill=mouth_color, width=t)
        draw.pieslice([(mx-mw*0.3, my), (mx+mw*0.3, my+mh)], 0, 180, fill='pink')
    elif mouth_style == 'Laugh':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 0, 180, fill=mouth_color, width=t)
        draw.line([(mx-mw*0.6, my+mh*0.1), (mx-mw*0.2, my+mh*0.5)], fill=mouth_color, width=t)
        draw.line([(mx+mw*0.6, my+mh*0.1), (mx+mw*0.2, my+mh*0.5)], fill=mouth_color, width=t)
    elif mouth_style == 'Sad':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 180, 360, fill=mouth_color, width=t)
    elif mouth_style == 'OpenSmile':
        draw.pieslice([(mx-mw, my-mh), (mx+mw, my+mh)], 0, 180, fill=mouth_color)
    elif mouth_style == 'Grimace':
        draw.rectangle([(mx-mw, my-mh*0.2), (mx+mw, my+mh*0.2)], outline=mouth_color, width=t)
        for i in range(1,5): draw.line([(mx-mw+i*mw*0.4, my-mh*0.2), (mx-mw+i*mw*0.4, my+mh*0.2)], fill=mouth_color, width=int(t/2))
    elif mouth_style == 'Oops':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 90, 270, fill=mouth_color, width=t)

    # Eyebrows
    brow_off = r*0.35
    brow_len = eye_r*1.2
    for ex, ey in positions:
        yb = ey - brow_off
        if brow_style == 'None': continue
        if brow_style == 'Straight':
            draw.line([(ex-brow_len, yb), (ex+brow_len, yb)], fill=brow_color, width=t)
        elif brow_style == 'Angled':
            draw.line([(ex-brow_len, yb+brow_len*0.3), (ex+brow_len, yb-brow_len*0.3)], fill=brow_color, width=t)
        elif brow_style == 'Raised':
            draw.arc([(ex-brow_len, yb-brow_len), (ex+brow_len, yb+brow_len)], 0, 180, fill=brow_color, width=t)
        elif brow_style == 'Sad':
            draw.arc([(ex-brow_len, yb-brow_len), (ex+brow_len, yb+brow_len)], 180, 360, fill=brow_color, width=t)
        elif brow_style == 'Frown':
            draw.line([(ex-brow_len, yb+brow_len*0.5), (ex+brow_len, yb+brow_len*0.5)], fill=brow_color, width=t)
        elif brow_style == 'Rounded':
            draw.arc([(ex-brow_len, yb-brow_len), (ex+brow_len, yb+brow_len)], 0, 360, fill=brow_color, width=t)
        elif brow_style == 'Zigzag':
            pts = [(ex-brow_len, yb), (ex-brow_len/2, yb-brow_len), (ex, yb), (ex+brow_len/2, yb-brow_len), (ex+brow_len, yb)]
            draw.line(pts, fill=brow_color, width=t)

    # Downsample
    return img.resize((BASE_SIZE, BASE_SIZE), resample=Image.LANCZOS)

# SVG stub
def generate_svg(params):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{0}"></svg>'.format(BASE_SIZE)

# Streamlit UI
st.sidebar.title('Emote Creator')
thickness = st.sidebar.slider('Line thickness', 1, 20, 10)
body_color = st.sidebar.color_picker('Body color', '#2AFF00')
body_style = st.sidebar.selectbox('Body style', ['Filled','Outline'], index=1)

st.sidebar.subheader('Eyes')
eye_color = st.sidebar.color_picker('Eye color', '#2AFF00')
eye_style = st.sidebar.selectbox('Eye style',['Filled','Outline'], index=0)
eye_shape = st.sidebar.selectbox('Eye shape', ['Open','Closed','Wink','Happy','Sad','Surprised','Sleepy','Angry','Excited','Dazed'], index=0)

st.sidebar.subheader('Mouth')
mouth_color = st.sidebar.color_picker('Mouth color', '#2AFF00')
mouth_style = st.sidebar.selectbox('Mouth type',['Smile','Frown','Neutral','Surprised','Tongue','Laugh','Sad','OpenSmile','Grimace','Oops'], index=0)

st.sidebar.subheader('Eyebrows')
brow_color = st.sidebar.color_picker('Brow color', '#2AFF00')
brow_style = st.sidebar.selectbox('Eyebrow style',['None','Straight','Angled','Raised','Sad','Frown','Rounded','Zigzag'], index=0)

# Render
img = draw_emote(body_color, body_style, eye_color, eye_style, eye_shape, mouth_color, mouth_style, brow_color, brow_style, thickness)
st.image(img, use_container_width=True)

# Download
st.sidebar.subheader('Download')
res = st.sidebar.selectbox('Resolution',[ '400x400','800x800','1200x1200'])
formats = st.sidebar.multiselect('Formats',['PNG','SVG'])
if formats:
    cols = st.sidebar.columns(len(formats))
    for fmt,col in zip(formats,cols):
        if fmt=='PNG':
            w,h = map(int,res.split('x'))
            buf=io.BytesIO(); img.resize((w,h)).save(buf,format='PNG')
            col.download_button('PNG',buf.getvalue(),file_name=f'emote_{w}x{h}.png',mime='image/png')
        else:
            svg=generate_svg({}); col.download_button('SVG',svg,file_name='emote.svg',mime='image/svg+xml')
