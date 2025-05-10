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
        elif eye_shape == 'Happy':
            draw.arc(bb, start=0, end=180, fill=eye_color, width=thickness*SCALE)
        elif eye_shape == 'Sad':
            draw.arc(bb, start=180, end=360, fill=eye_color, width=thickness*SCALE)
        elif eye_shape == 'Surprised':
            draw.ellipse(bb, outline=eye_color, width=thickness*SCALE)
        elif eye_shape == 'Sleepy':
            draw.arc(bb, start=45, end=135, fill=eye_color, width=thickness*SCALE)
        elif eye_shape == 'Angry':
            draw.line([(ex-eye_r, ey-eye_r*0.5),(ex+eye_r, ey+eye_r*0.5)], fill=eye_color, width=thickness*SCALE)
        elif eye_shape == 'Excited':
            draw.line([(ex, ey-eye_r),(ex, ey+eye_r)], fill=eye_color, width=thickness*SCALE)
            draw.line([(ex-eye_r, ey),(ex+eye_r, ey)], fill=eye_color, width=thickness*SCALE)
        else:  # Dazed
            draw.line([(ex-eye_r, ey-eye_r),(ex+eye_r, ey+eye_r)], fill=eye_color, width=thickness*SCALE)
            draw.line([(ex-eye_r, ey+eye_r),(ex+eye_r, ey-eye_r)], fill=eye_color, width=thickness*SCALE)

    # Mouth
    mx, my = cx, cy + radius*0.4
    mw, mh = BASE_SIZE*SCALE*0.25, BASE_SIZE*SCALE*0.1
    if mouth_style == 'Smile':
        draw.arc([(mx-mw, my-mh),(mx+mw,my+mh)],0,180, fill=mouth_color, width=thickness*SCALE)
    elif mouth_style == 'Frown':
        draw.arc([(mx-mw, my-mh),(mx+mw,my+mh)],180,360, fill=mouth_color, width=thickness*SCALE)
    elif mouth_style == 'Neutral':
        draw.line([(mx-mw,my),(mx+mw,my)], fill=mouth_color, width=thickness*SCALE)
    elif mouth_style == 'Surprised':
        draw.ellipse([(mx-mh,my-mh),(mx+mh,my+mh)], outline=mouth_color, width=thickness*SCALE)
    elif mouth_style == 'Tongue':
        draw.arc([(mx-mw,my-mh),(mx+mw,my+mh)],0,180, fill=mouth_color, width=thickness*SCALE)
        draw.rectangle([(mx-mw*0.3,my),(mx+mw*0.3,my+mh*0.6)], fill='pink')
    elif mouth_style == 'Laugh':
        draw.arc([(mx-mw,my-mh),(mx+mw,my+mh)],0,180, fill=mouth_color, width=thickness*SCALE)
        draw.arc([(mx-mw*0.8,my-mh*0.2),(mx-mw*0.2,my+mh*0.2)],180,360, fill=mouth_color, width=thickness*SCALE)
        draw.arc([(mx+mw*0.2,my-mh*0.2),(mx+mw*0.8,my+mh*0.2)],180,360, fill=mouth_color, width=thickness*SCALE)
    elif mouth_style == 'Sad':
        draw.arc([(mx-mw,my-mh),(mx+mw,my+mh)],180,360, fill=mouth_color, width=thickness*SCALE)
    elif mouth_style == 'OpenSmile':
        draw.ellipse([(mx-mw,my-mh),(mx+mw,my+mh)], fill=mouth_color)
    elif mouth_style == 'Grimace':
        draw.rectangle([(mx-mw,my-mh*0.2),(mx+mw,my+mh*0.2)], fill=mouth_color)
    else:  # Oops
        draw.arc([(mx-mw,my-mh),(mx+mw,my+mh)],90,270, fill=mouth_color, width=thickness*SCALE)

    # Eyebrows
    offset = radius*0.35
    length = eye_r*1.5
    for ex, ey in eyes:
        yb = ey - offset
        if brow_style == 'Straight':
            draw.line([(ex-length,yb),(ex+length,yb)], fill=brow_color, width=thickness*SCALE)
        elif brow_style == 'Angled':
            draw.line([(ex-length,yb+length*0.3),(ex+length,yb-length*0.3)], fill=brow_color, width=thickness*SCALE)
        elif brow_style == 'Raised':
            draw.arc([(ex-length,yb-length),(ex+length,yb+length)],0,180, fill=brow_color, width=thickness*SCALE)
        elif brow_style == 'Sad':
            draw.arc([(ex-length,yb-length),(ex+length,yb+length)],180,360, fill=brow_color, width=thickness*SCALE)
        elif brow_style == 'Frown':
            draw.arc([(ex-length,yb-length*1.2),(ex+length,yb+length*0.2)],200,340, fill=brow_color, width=thickness*SCALE)
        elif brow_style == 'Rounded':
            draw.ellipse([(ex-length,yb-length),(ex+length,yb+length)], outline=brow_color, width=thickness*SCALE)
        elif brow_style == 'Zigzag':
            pts = [(ex-length,yb),(ex-length/2,yb-length/2),(ex,yb),(ex+length/2,yb-length/2),(ex+length,yb)]
            draw.line(pts, fill=brow_color, width=thickness*SCALE)
        elif brow_style == 'RaisedAngled':
            draw.line([(ex-length,yb+length*0.2),(ex,yb-length*0.2),(ex+length,yb+length*0.2)], fill=brow_color, width=thickness*SCALE)
        elif brow_style == 'Slanted':
            draw.line([(ex-length,yb+length),(ex+length,yb-length)], fill=brow_color, width=thickness*SCALE)
        # 'None' draws nothing

    return img.resize((BASE_SIZE, BASE_SIZE), resample=Image.LANCZOS)

# SVG generator
def generate_svg(params):
    w, h = BASE_SIZE, BASE_SIZE
    cx, cy, r = w/2, h/2, (w/2-10)
    svg = [f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">']
    # Body
    if params['body_style']=='Filled':
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{params["body_color"]}"/>')
    else:
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{params["body_color"]}" stroke-width="{params["thickness"]}"/>')
    # Eyes
    eye_r = r*0.15
    ox = r*0.5
    oy = -r*0.2
    for i in [ -ox, ox ]:
        ex = cx + i; ey = cy + oy
        shape = params['eye_shape']
        stroke = params['thickness']
        col = params['eye_color']
        if shape in ['Open','Wink']: 
            if shape=='Open' or (shape=='Wink' and i>0):
                svg.append(f'<circle cx="{ex}" cy="{ey}" r="{eye_r}" fill="{col}"/>')
        elif shape=='Closed':
            svg.append(f'<line x1="{ex-eye_r}" y1="{ey}" x2="{ex+eye_r}" y2="{ey}" stroke="{col}" stroke-width="{stroke}"/>')
        # Other eye shapes can be added similarly...
    # Mouth (simplified)
    svg.append(f'<text x="{cx}" y="{cy + r*0.5}" text-anchor="middle" fill="{params["mouth_color"]}" font-size="{r*0.4}">{params["mouth_style"][0]}</text>')
    # Eyebrows (simplified)
    svg.append('</svg>')
    return '\n'.join(svg)

# Sidebar UI
st.sidebar.title("Emote Creator")

thickness = st.sidebar.slider("Line thickness", 1, 20, 4)
body_color = st.sidebar.color_picker("Body color", "#000000")
body_style = st.sidebar.selectbox("Body style", ['Filled', 'Outline'])

st.sidebar.subheader("Eyes")
ey_color = st.sidebar.color_picker("Eye color", "#000000")
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
