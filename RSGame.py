
import streamlit as st
from pathlib import Path
import random
import streamlit.components.v1 as components
import base64
import uuid

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(
    page_title="Ο κόσμος από το διάστημα!",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------
# IMAGE FOLDERS
# -------------------
BASE_DIR = Path(__file__).parent 
FOLDERS = {
    "guess": BASE_DIR / "images/guess_the_place",
    "puzzle": BASE_DIR / "images/puzzle",
    "before_after": BASE_DIR / "images/before_after",
    "color_detective": BASE_DIR / "images/color_detective",
}
logo_path = BASE_DIR / "images" / "icons" / "group_logo.png"
for f in FOLDERS.values():
    f.mkdir(parents=True, exist_ok=True)


# -------------------
# GUESS THE PLACE
# -------------------
def show_guess_the_place():
    st.header("Μάντεψε το μέρος")
    images = list(FOLDERS["guess"].glob("*.*"))
    if not images:
        st.warning("Put some images in `images/guess_the_place/`")
        return

    if "current_guess" not in st.session_state:
        st.session_state.current_guess = str(random.choice(images))

    if st.button("Επόμενη Εικόνα"):
        # try to pick a different image
        choices = [str(p) for p in images if str(p) != st.session_state.current_guess]
        st.session_state.current_guess = random.choice(choices) if choices else str(random.choice(images))

    st.image(st.session_state.current_guess, width=700)

from streamlit_image_comparison import image_comparison

#for offline

def show_before_after_offline():
    st.header("Πριν και Μετά")

    # Collect before/after pairs
    pairs = {}
    for f in FOLDERS["before_after"].glob("*.*"):
        name = f.stem.lower()
        if "_before" in name:
            key = name.replace("_before", "")
            pairs.setdefault(key, {})["before"] = str(f)
        elif "_after" in name:
            key = name.replace("_after", "")
            pairs.setdefault(key, {})["after"] = str(f)

    if not pairs:
        st.warning("Put pairs of images in `images/before_after/` (e.g. city_before.jpg, city_after.jpg)")
        return

    choice = st.selectbox("Διάλεξε μέρος", list(pairs.keys()))

    if "before" in pairs[choice] and "after" in pairs[choice]:
        mode = st.radio("Εμφάνιση:", ["Πριν", "Μετά"], horizontal=True)

        if mode == "Πριν":
            st.image(pairs[choice]["before"], caption="Πριν", use_container_width=True)
        else:
            st.image(pairs[choice]["after"], caption="Μετά", use_container_width=True)
    else:
        st.error(f"Missing before/after pair for {choice}")

def show_color_offline():
    st.header("Ντετέκτιβ χρωμάτων")

    # Collect before/after pairs
    pairs = {}
    for f in FOLDERS["color_detective"].glob("*.*"):
        name = f.stem.lower()
        if "_before" in name:
            key = name.replace("_before", "")
            pairs.setdefault(key, {})["before"] = str(f)
        elif "_after" in name:
            key = name.replace("_after", "")
            pairs.setdefault(key, {})["after"] = str(f)

    if not pairs:
        st.warning("Put pairs of images in `images/before_after/` (e.g. city_before.jpg, city_after.jpg)")
        return

    choice = st.selectbox("Διάλεξε μέρος", list(pairs.keys()))

    if "before" in pairs[choice] and "after" in pairs[choice]:
        mode = st.radio("Εμφάνιση:", ["True color", "False color"], horizontal=True)

        if mode == "True color":
            st.image(pairs[choice]["before"], caption="True color", use_container_width=True)
        else:
            st.image(pairs[choice]["after"], caption="False color", use_container_width=True)
    else:
        st.error(f"Missing before/after pair for {choice}")
#till here offline

def show_color_online():
    st.header("Ντετέκτιβ χρωμάτων")

    pairs = {}
    for f in FOLDERS["color_detective"].glob("*.*"):
        name = f.stem.lower()
        if "_before" in name:
            key = name.replace("_before", "")
            pairs.setdefault(key, {})["before"] = str(f)
        elif "_after" in name:
            key = name.replace("_after", "")
            pairs.setdefault(key, {})["after"] = str(f)

    if not pairs:
        st.warning("Put pairs of images in `images/before_after/` (e.g. city_before.jpg, city_after.jpg)")
        return

    choice = st.selectbox("Διάλεξε μέρος", list(pairs.keys()))

    if "before" in pairs[choice] and "after" in pairs[choice]:
        image_comparison(
            img1=pairs[choice]["before"],
            img2=pairs[choice]["after"],
            label1="True color",
            label2="False color",
            width=950,
        )
    else:
        st.error(f"Missing before/after pair for {choice}")

def show_before_after_online():
    st.header("Πριν και Μετά")

    pairs = {}
    for f in FOLDERS["before_after"].glob("*.*"):
        name = f.stem.lower()
        if "_before" in name:
            key = name.replace("_before", "")
            pairs.setdefault(key, {})["before"] = str(f)
        elif "_after" in name:
            key = name.replace("_after", "")
            pairs.setdefault(key, {})["after"] = str(f)

    if not pairs:
        st.warning("Put pairs of images in `images/before_after/` (e.g. city_before.jpg, city_after.jpg)")
        return

    choice = st.selectbox("Διάλεξε μέρος", list(pairs.keys()))

    if "before" in pairs[choice] and "after" in pairs[choice]:
        image_comparison(
            img1=pairs[choice]["before"],
            img2=pairs[choice]["after"],
            label1="Πριν",
            label2="Μετά",
            width=950,
        )
    else:
        st.error(f"Missing before/after pair for {choice}")
# -------------------
# PUZZLE GAME
# -------------------



def show_puzzle():
    st.header("Puzzle")

    images = list(FOLDERS["puzzle"].glob("*.*"))
    if not images:
        st.warning("Put one image in `images/puzzle/` (e.g. earth.jpg)")
        return

    img_path = images[0]

    # Read and convert image to base64
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{img_b64}"

    # Slider for difficulty (grid size)
    grid_size = st.slider("Διάλεξε δυσκολία", 3, 6, 3)
    tile_size = 150  # bigger tiles now

    # Unique ID for container (prevents conflicts when rerunning)
    container_id = f"puzzle_{uuid.uuid4().hex}"

    # Shuffle button (we’ll trigger JS shuffle via streamlit’s components)
    if st.button("🔀 Ανακάτεψε"):
        st.session_state["shuffle_key"] = uuid.uuid4().hex  # force rerun to refresh
        


    html_code = f"""
    <style>
      #{container_id} {{
        display: flex;
        justify-content: center;
        margin-top: 10px;
      }}
      #{container_id} #puzzle {{
        display: grid;
        grid-template-columns: repeat({grid_size}, {tile_size}px);
        grid-template-rows: repeat({grid_size}, {tile_size}px);
        gap: 2px;
        user-select: none;
      }}
      #{container_id} .piece {{
        width: {tile_size}px;
        height: {tile_size}px;
        background-image: url('{image_url}');
        background-size: {grid_size * tile_size}px {grid_size * tile_size}px;
        border: 1px solid #999;
        cursor: grab;
        box-sizing: border-box;
      }}
    </style>

    <div id="{container_id}">
      <div id="puzzle"></div>
    </div>

    <script>
    const container = document.getElementById("{container_id}");
    const puzzle = container.querySelector("#puzzle");
    const size = {grid_size};
    const positions = [];

    // Create pieces
    for (let row=0; row<size; row++) {{
      for (let col=0; col<size; col++) {{
        const piece = document.createElement("div");
        piece.classList.add("piece");
        piece.style.backgroundPosition = '-' + (col * {tile_size}) + 'px -' + (row * {tile_size}) + 'px';
        positions.push(piece);
      }}
    }}

    function shufflePuzzle() {{
      puzzle.innerHTML = ""; // clear
      positions.sort(() => Math.random() - 0.5);
      positions.forEach(p => puzzle.appendChild(p));

      // re-attach drag events
      let dragged = null;
      document.querySelectorAll("#{container_id} .piece").forEach(piece => {{
        piece.draggable = true;
        piece.addEventListener("dragstart", e => dragged = piece);
        piece.addEventListener("dragover", e => e.preventDefault());
        piece.addEventListener("drop", e => {{
          e.preventDefault();
          if (dragged && dragged !== piece) {{
            const temp = document.createElement("div");
            puzzle.insertBefore(temp, piece);
            puzzle.insertBefore(piece, dragged);
            puzzle.insertBefore(dragged, temp);
            puzzle.removeChild(temp);
          }}
        }});
      }});
    }}

    // Initial shuffle
    shufflePuzzle();
    </script>
    """

    iframe_size = grid_size * (tile_size + 2) + 20
    components.html(html_code, height=iframe_size, width=iframe_size)

import socket

# --- Helper: check internet ---
def has_internet(host="8.8.8.8", port=53, timeout=2):
    """Return True if internet is available, False otherwise."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def show_before_after():
    if has_internet():
        show_before_after_online()
    else:
        #st.info("Χωρίς σύνδεση στο διαδίκτυο – χρήση offline έκδοσης.")
        show_before_after_offline()

def show_color():
    if has_internet():
        show_color_online()
    else:
        #st.info("Χωρίς σύνδεση στο διαδίκτυο – χρήση offline έκδοσης.")
        show_color_offline()
# -------------------
# MAIN MENU
# -------------------
with st.sidebar:
    st.title("Ο κόσμος από το διάστημα!")
    st.image(str(logo_path), width=230)  # your logo file
    menu = st.sidebar.radio(
        "Διάλεξε δραστηριότητα",
        ["Μάντεψε το μέρος", "Puzzle", "Πριν και μετά", "Ντετέκτιβ χρωμάτων"]
    )
    st.markdown("---")  # separator line
    st.markdown("Πανεπιστήμιο Αιγαίου  \nΤμήμα Γεωγραφίας  \n  \nΑνάπτυξη:  \nΧρήστος Βασιλάκος  \nΕπίκ. Καθηγητής  \nhttps://rsgis.aegean.gr")
if menu == "Μάντεψε το μέρος":
    show_guess_the_place()
elif menu == "Puzzle":
    show_puzzle()
elif menu == "Πριν και μετά":
    show_before_after()
elif menu == "Ντετέκτιβ χρωμάτων":
    show_color()


