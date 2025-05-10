import streamlit as st
from PIL import Image, ImageDraw
import io

# Constants
BASE_SIZE = 400
SCALE = 4  # for antialiasing
TRUE_SIZE = BASE_SIZE * SCALE

# Drawing function
def draw_emote(body_color, body_style,
               eye_color, eye_style, eye_shape,
               mouth_color, mouth_style,
               eyebrows, brow_color, brow_style,
               thickness):
    # Create high-res canvas
    img = Image.new("RGBA", (TRUE_SIZE, TRUE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = (TRUE_SIZE // 2, TRUE_SIZE // 2)
    radius = (BASE_SIZE // 2 - 10) * SCALE

    # Body
    bbox = [
        (center[0] - radius, center[1] - radius),
        (center[0] + radius, center[1] + radius),
    ]
    if body_style == 'Filled':
        draw.ellipse(bbox, fill=body_color)
    else:
        draw.ellipse(bbox, outline=body_color, width=thickness * SCALE)

    # Eye params
    eye_r = radius * 0.15
    ox = radius * 0.5
    oy = -radius * 0.2
    eyes = [
        (center[0] - ox, center[1] + oy),
        (center[0] + ox, center[1] + oy)
    ]
    for (x, y) in eyes:
        bbox_eye = [(x - eye_r, y - eye_r), (x + eye_r, y + eye_r)]
        if eye_style == 'Filled':
            draw.ellipse(bbox_eye, fill=eye_color)
        else:
            draw.ellipse(bbox_eye, outline=eye_color, width=thickness * SCALE)
        if eye_shape == 'Closed':
            start = (x - eye_r, y)
            end = (x + eye_r, y)
            draw.line([start, end], fill=eye_color, width=thickness * SCALE)

    # Mouth
    mx, my = center[0], center[1] + radius * 0.4
    mw = BASE_SIZE * SCALE * 0.25
    mh = BASE_SIZE * SCALE * 0.1
    if mouth_style == 'Smile':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 0, 180, fill=mouth_color, width=thickness * SCALE)
    elif mouth_style == 'Frown':
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 180, 360, fill=mouth_color, width=thickness * SCALE)
    elif mouth_style == 'Neutral':
        draw.line([(mx-mw, my), (mx+mw, my)], fill=mouth_color, width=thickness * SCALE)
    elif mouth_style == 'Surprised':
        r = mw * 0.5
        draw.ellipse([(mx-r, my-r), (mx+r, my+r)], outline=mouth_color, width=thickness * SCALE)
    else:  # 'Tongue'
        # simple arc with tongue
        draw.arc([(mx-mw, my-mh), (mx+mw, my+mh)], 0, 180, fill=mouth_color, width=thickness * SCALE)
        draw.rectangle([(mx- mw*0.3, my), (mx+ mw*0.3, my+mh*0.6)], fill='pink')

    # Eyebrows
    brow_offset = radius * 0.35
    brow_length = eye_r * 1.5
    for (x, y) in eyes:
        yb = y - brow_offset
        if brow_style == 'Straight':
            draw.line([(x-brow_length, yb), (x+brow_length, yb)], fill=brow_color, width=thickness * SCALE)
        elif brow_style == 'Angled':
            draw.line([(x-brow_length, yb+brow_length*0.3), (x+brow_length, yb-brow_length*0.3)], fill=brow_color, width=thickness * SCALE)
        elif brow_style == 'Raised':
            draw.arc([(x-brow_length, yb-brow_length), (x+brow_length, yb+brow_length)], 0, 180, fill=brow_color, width=thickness * SCALE)
        elif brow_style == 'Sad':
            draw.arc([(x-brow_length, yb-brow_length), (x+brow_length, yb+brow_length)], 180, 360, fill=brow_color, width=thickness * SCALE)
        # 'None' draws nothing

    # Downscale for smoothing
    return img.resize((BASE_SIZE, BASE_SIZE), resample=Image.LANCZOS)

# Sidebar UI
st.sidebar.title("Emote Creator")

# Thickness slider
thickness = st.sidebar.slider("Line thickness", 1, 20, 4)

# Body options
body_color = st.sidebar.color_picker("Body color", "#000000")
body_style = st.sidebar.selectbox("Body style", ['Filled', 'Outline'])

# Eye options
st.sidebar.subheader("Eyes")
ey_color = st.sidebar.color_picker("Eye color", "#000000")
eye_style = st.sidebar.selectbox("Eye style", ['Filled', 'Outline'])
eye_shape = st.sidebar.selectbox("Eye shape", ['Open', 'Closed'])

# Mouth options
st.sidebar.subheader("Mouth")
mouth_color = st.sidebar.color_picker("Mouth color", "#000000")
mouth_style = st.sidebar.selectbox("Mouth type", ['Smile', 'Frown', 'Neutral', 'Surprised', 'Tongue'])

# Eyebrow options
st.sidebar.subheader("Eyebrows")
eyebrows = st.sidebar.selectbox("Eyebrow style", ['None', 'Straight', 'Angled', 'Raised', 'Sad'])
brow_color = st.sidebar.color_picker("Brow color", "#000000")
brow_style = eyebrows

def generate_svg(params):
    # Simple SVG output matching current emote
    w, h = BASE_SIZE, BASE_SIZE
    cx, cy, r = w/2, h/2, (w/2 - 10)
    svg = [f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">']
    # Body
    if params['body_style']=='Filled':
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{params["body_color"]}"/>')
    else:
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{params["body_color"]}" stroke-width="{params["thickness"]}"/>')
    # ... (eyes, mouth, brows omitted for brevity) ...
    svg.append('</svg>')
    return '\n'.join(svg)

# Draw and show
img = draw_emote(body_color, body_style,
                 eye_color, eye_style, eye_shape,
                 mouth_color, mouth_style,
                 eyebrows!='None', brow_color, brow_style,
                 thickness)
st.image(img, use_column_width=True)

# Download options
st.sidebar.subheader("Download")
res = st.sidebar.selectbox("Resolution", ['400x400','800x800','1200x1200'])
formats = st.sidebar.multiselect("Formats", ['PNG','SVG'])
cols = st.sidebar.columns(len(formats))
for fmt, col in zip(formats, cols):
    if fmt=='PNG':
        w, h = map(int, res.split('x'))
        buf = io.BytesIO()
        img.resize((w, h)).save(buf, format='PNG')
        col.download_button("Download PNG", buf.getvalue(), file_name=f"emote_{w}x{h}.png", mime="image/png")
    else:
        svg_str = generate_svg(locals())
        col.download_button("Download SVG", svg_str, file_name="emote.svg", mime="image/svg+xml")
