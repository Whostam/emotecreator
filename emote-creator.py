import streamlit as st
from PIL import Image, ImageDraw

def draw_emote(body_color, eye_color, eye_thickness, eye_style, eye_shape,
               mouth_color, mouth_width, mouth_height, mouth_thickness, mouth_style,
               eyebrows, brow_color, brow_thickness, brow_offset):
    size = 400
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw body
    radius = size // 2 - 10
    center = (size // 2, size // 2)
    draw.ellipse([
        (center[0] - radius, center[1] - radius),
        (center[0] + radius, center[1] + radius)
    ], fill=body_color)

    # Eye positions
    eye_offset_x = radius * 0.5
    eye_offset_y = -radius * 0.2
    eye_radius = radius * 0.15
    left_eye = (center[0] - eye_offset_x, center[1] + eye_offset_y)
    right_eye = (center[0] + eye_offset_x, center[1] + eye_offset_y)

    def draw_eye(pos):
        x, y = pos
        bbox = [
            (x - eye_radius, y - eye_radius),
            (x + eye_radius, y + eye_radius)
        ]
        if eye_style == 'Filled':
            draw.ellipse(bbox, fill=eye_color)
        else:
            draw.ellipse(bbox, outline=eye_color, width=eye_thickness)
        if eye_shape == 'Closed':
            # draw simple arc line for closed eye
            start = (x - eye_radius, y)
            end = (x + eye_radius, y)
            draw.line([start, end], fill=eye_color, width=eye_thickness)

    draw_eye(left_eye)
    draw_eye(right_eye)

    # Mouth
    mouth_center = (center[0], center[1] + radius * 0.4)
    mouth_half_width = mouth_width
    mouth_half_height = mouth_height
    mouth_box = [
        (mouth_center[0] - mouth_half_width, mouth_center[1] - mouth_half_height),
        (mouth_center[0] + mouth_half_width, mouth_center[1] + mouth_half_height)
    ]
    if mouth_style == 'Arc':
        start_angle, end_angle = (0, 180) if mouth_thickness > 0 else (180, 0)
        draw.arc(mouth_box, start=start_angle, end=end_angle, fill=mouth_color, width=mouth_thickness)
    else:
        p1 = (mouth_box[0][0], mouth_center[1])
        p2 = (mouth_box[1][0], mouth_center[1])
        draw.line([p1, p2], fill=mouth_color, width=mouth_thickness)

    # Eyebrows
    if eyebrows:
        brow_y = center[1] + eye_offset_y - brow_offset
        l1 = (left_eye[0] - eye_radius, brow_y)
        l2 = (left_eye[0] + eye_radius, brow_y)
        draw.line([l1, l2], fill=brow_color, width=brow_thickness)
        r1 = (right_eye[0] - eye_radius, brow_y)
        r2 = (right_eye[0] + eye_radius, brow_y)
        draw.line([r1, r2], fill=brow_color, width=brow_thickness)

    return img

# Sidebar controls
st.sidebar.title("Emote Creator")

# Body
body_color = st.sidebar.color_picker("Body color", "#000000")

# Eyes
st.sidebar.subheader("Eyes")
eye_color = st.sidebar.color_picker("Eye color", "#000000")
eye_thickness = st.sidebar.slider("Eye thickness", 1, 20, 5)
eye_style = st.sidebar.selectbox("Style", ["Filled", "Outline"])
eye_shape = st.sidebar.selectbox("Shape", ["Open", "Closed"])

# Mouth
st.sidebar.subheader("Mouth")
mouth_color = st.sidebar.color_picker("Mouth color", "#000000")
mouth_width = st.sidebar.slider("Mouth width", 10, 200, 100)
mouth_height = st.sidebar.slider("Mouth height", 0, 100, 50)
mouth_thickness = st.sidebar.slider("Mouth thickness", 1, 20, 5)
mouth_style = st.sidebar.selectbox("Mouth type", ["Arc", "Line"])

# Eyebrows
st.sidebar.subheader("Eyebrows")
eyebrows = st.sidebar.checkbox("Add eyebrows", True)
brow_color = st.sidebar.color_picker("Brow color", "#000000")
brow_thickness = st.sidebar.slider("Brow thickness", 1, 20, 5)
brow_offset = st.sidebar.slider("Brow offset", 0, 100, 20)

# Render emote
emote_img = draw_emote(
    body_color, eye_color, eye_thickness, eye_style, eye_shape,
    mouth_color, mouth_width, mouth_height, mouth_thickness, mouth_style,
    eyebrows, brow_color, brow_thickness, brow_offset
)

st.image(emote_img, use_column_width=True)
