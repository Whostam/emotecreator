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
               brow_color, brow_style,
               thickness):
    img = Image.new("RGBA", (TRUE_SIZE, TRUE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = TRUE_SIZE//2, TRUE_SIZE//2
    radius = (BASE_SIZE//2 - 10) * SCALE

    # Body
    bbox = [(cx-radius, cy-radius), (cx+radius, cy+radius)]
    if body_style == 'Filled':
        draw.ellipse(bbox, fill=body_color)
    else:
        draw.ellipse(bbox, outline=body_color, width=thickness*SCALE)

    # Eye positions
    eye_r = radius * 0.15
    ox = radius * 0.5
    oy = -radius * 0.2
    eyes = [ (cx-ox, cy+oy), (cx+ox, cy+oy) ]

    for i, (ex, ey) in enumerate(eyes):
        bb = [(ex-eye_r, ey-eye_r), (ex+eye_r, ey+eye_r)]
        # Shape handlers
        if eye_shape == 'Open':
            if eye_style=='Filled': draw.ellipse(bb, fill=eye_color)
            else: draw.ellipse(bb, outline=eye_color, width=thickness*SCALE)
        elif eye_shape == 'Closed':
            draw.line([(ex-eye_r, ey),(ex+eye_r,ey)], fill=eye_color, width=thickness*SCALE)
        elif eye_shape == 'Wink':
            if i==0: draw.line([(ex-eye_r, ey),(ex+eye_r,ey)], fill=eye_color, width=thickness*SCALE)
            else: draw.ellipse(bb, fill=eye_color)
        # ... other shapes unchanged ...
        else:  # Dazed
            draw.line([(ex-eye_r, ey-eye_r),(ex+eye_r, ey+eye_r)], fill=eye_color, width=thickness*SCALE)
            draw.line([(ex-eye_r, ey+eye_r),(ex+eye_r, ey-eye_r)], fill=eye_color, width=thickness*SCALE)

    # Mouth (existing logic remains)
    # Eyebrows (existing logic remains)
    return img.resize((BASE_SIZE, BASE_SIZE), resample=Image.LANCZOS)

# SVG generator (existing stub)

def generate_svg(params):
    # existing SVG code
    return '<svg></svg>'

# Sidebar UI
st.sidebar.title("Emote Creator")

thickness = st.sidebar.slider("Line thickness", 1, 20, 4)
body_color = st.sidebar.color_picker("Body color", "#000000")
body_style = st.sidebar.selectbox("Body style", ['Filled', 'Outline'])

st.sidebar.subheader("Eyes")
eye_color = st.sidebar.color_picker("Eye color", "#000000")  # fixed variable name
eye_style = st.sidebar.selectbox("Eye style", ['Filled', 'Outline'])
eye_shape = st.sidebar.selectbox("Eye shape", ['Open', 'Closed', 'Wink', 'Happy', 'Sad', 'Surprised', 'Sleepy', 'Angry', 'Excited', 'Dazed'])

st.sidebar.subheader("Mouth")
mouth_color = st.sidebar.color_picker("Mouth color", "#000000")
mouth_style = st.sidebar.selectbox("Mouth type", ['Smile', 'Frown', 'Neutral', 'Surprised', 'Tongue', 'Laugh', 'Sad', 'OpenSmile', 'Grimace', 'Oops'])

st.sidebar.subheader("Eyebrows")
brow_color = st.sidebar.color_picker("Brow color", "#000000")
brow_style = st.sidebar.selectbox("Eyebrow style", ['None', 'Straight', 'Angled', 'Raised', 'Sad', 'Frown', 'Rounded', 'Zigzag', 'RaisedAngled', 'Slanted'])

# Render and display
img = draw_emote(body_color, body_style,
                 eye_color, eye_style, eye_shape,
                 mouth_color, mouth_style,
                 brow_color, brow_style,
                 thickness)
st.image(img, use_column_width=True)

# Download
st.sidebar.subheader("Download")
res = st.sidebar.selectbox("Resolution", ['400x400','800x800','1200x1200'])
formats = st.sidebar.multiselect("Formats", ['PNG','SVG'])
cols = st.sidebar.columns(len(formats))
for fmt, col in zip(formats, cols):
    if fmt=='PNG':
        w,h = map(int,res.split('x'))
        buf=io.BytesIO(); img.resize((w,h)).save(buf,format='PNG')
        col.download_button("Download PNG",buf.getvalue(),file_name=f"emote_{w}x{h}.png",mime="image/png")
    else:
        svg = generate_svg({
            'body_color': body_color,
            'body_style': body_style,
            'eye_color': eye_color,
            'eye_style': eye_style,
            'eye_shape': eye_shape,
            'mouth_color': mouth_color,
            'mouth_style': mouth_style,
            'brow_color': brow_color,
            'brow_style': brow_style,
            'thickness': thickness
        })
        col.download_button("Download SVG", svg, file_name="emote.svg", mime="image/svg+xml")
