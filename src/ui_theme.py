import streamlit as st
from utils.helpers import get_base64_image

THEMES = ["Light", "Dark", "Hospital"]
ICONS = {"Light": "☀️", "Dark": "🌙", "Hospital": "➕"}

# --- Session state initialization ---
if "theme_idx" not in st.session_state:
    st.session_state.theme_idx = 0
if "theme" not in st.session_state:
    st.session_state.theme = THEMES[st.session_state.theme_idx]
if "theme_name" not in st.session_state:
    st.session_state.theme_name = THEMES[st.session_state.theme_idx]
    
def switch_theme():
    """
    Cycle through available UI themes and update the current session state.

    This function increments the theme index stored in ``st.session_state`` 
    and applies the corresponding theme from the global ``THEMES`` list. 
    It ensures the theme index wraps around safely using modulo arithmetic.

    """
    st.session_state.theme_idx = (st.session_state.theme_idx + 1) % len(THEMES)
    st.session_state.theme = THEMES[st.session_state.theme_idx]
    st.session_state.theme_name = THEMES[st.session_state.theme_idx]
    set_theme(st.session_state.theme)

def get_palette(theme: str):
    """
    Retrieve the color palette for a specified theme.

    Given a theme name, this function returns a dictionary mapping style 
    keys (e.g., background, borders, text colors, font) to their 
    corresponding color codes or CSS-compatible values. 
    
    Supported themes are:
    - ``"Light"``: Light-colored palette with dark text.
    - ``"Dark"``: Dark-colored palette with light text.
    - ``"Hospital"``: Custom palette using a hospital-themed background image 
      and accent colors.
    - Any unsupported theme defaults to ``"Light"``.

    Parameters
    ----------
    theme : str

    Returns
    -------
    dict[str, str]
        A dictionary containing style keys and their associated 
        color values or CSS properties.

    """
    if theme == "Light":
        return {
            "bg": "#8fb1b5",
            "border": "#000000",
            "input_bg": "#8fb1b5",
            "input_color": "#000000",
            "button_bg": "#8fb1b5",
            "button_color": "#000000",
            "tooltip_bg": "#f0f0f0",
            "tooltip_color": "#000000",
            "font": "Roboto, sans-serif"
        }
    elif theme == "Dark":
        return {
            "bg": "#1e1e1e",
            "border": "#ffffff",
            "input_bg": "#1e1e1e",
            "input_color": "#ffffff",
            "button_bg": "#1e1e1e",
            "button_color": "#fff",
            "tooltip_bg": "#333333",
            "tooltip_color": "#ffffff",
            "font": "Roboto Mono, monospace"
        }
    elif theme == "Hospital":
        bg_img = get_base64_image("img/Hospital_BG_Blur.jpg")
        return {
            "bg": f'url("{bg_img}")',
            "border": "#000000",
            "input_bg": f'url("{bg_img}")',
            "input_color": "#910c15",
            "button_bg": f'url("{bg_img}")',
            "button_color": "#910c15",
            "tooltip_bg": "#ffffff",
            "tooltip_color": "#910c15",
            "font": "Poppins, sans-serif"
        }
    else:  # default to Light
        return get_palette("Light")

def render_theme_toggle():
    """
    Render a theme toggle button with animated hover effects.

    This function manages theme state in ``st.session_state`` and 
    provides a button for users to cycle through available themes 
    defined in the global ``THEMES`` list. The button displays the 
    current theme's icon, with a subtle preview of the next theme’s 
    icon shown as a hover indicator.

    Behavior
    --------
    - Initializes ``st.session_state.theme_idx`` and ``st.session_state.theme`` 
      if they do not already exist.
    - Determines the current theme and the next theme in the cycle.
    - Renders a button with the current theme's icon that, when clicked, 
      calls ``switch_theme`` to update the session state.
    - Applies CSS for hover animations (rotation, scaling, and a 
      next-theme preview icon).
    - Applies the selected theme via ``set_theme``.

    """
    if "theme_idx" not in st.session_state:
        st.session_state.theme_idx = 0
    if "theme" not in st.session_state:
        st.session_state.theme = THEMES[st.session_state.theme_idx]
    
    idx = st.session_state.get("theme_idx", 0)
    theme = st.session_state.get("theme", THEMES[idx])
    next_idx = (idx + 1) % len(THEMES)
    next_theme = THEMES[next_idx]
    icon = ICONS.get(theme, "☀️")
    next_icon = ICONS.get(next_theme, "☀️")

    st.button(label=icon, key="theme_toggle_button", on_click=switch_theme)
    set_theme(theme)

    # --- Hovering effect ---
    st.markdown(f"""
        <style>
        div[role="button"] > button[key="theme_toggle_button"]:hover {{
            transform: rotate(25deg) scale(1.2);
            transition: transform 0.25s ease-in-out;
        }}
        div[role="button"] > button[key="theme_toggle_button"] {{
            font-size: 32px;
            border-radius: 50%;
            border: none;
            background: none;
            cursor: pointer;
            position: relative;
        }}
        div[role="button"] > button[key="theme_toggle_button"]::after {{
            content: '{next_icon}';
            position: absolute;
            top: -8px;
            right: -12px;
            font-size: 18px;
            opacity: 0.6;
        }}
        </style>
    """, unsafe_allow_html=True)

    set_theme(st.session_state.theme)

def set_theme(theme: str):
    """
    Apply a visual theme to the Streamlit app by injecting custom CSS.

    This function retrieves the style palette for the given theme via 
    ``get_palette`` and dynamically generates CSS to style various 
    Streamlit components, such as inputs, buttons, tabs, and tooltips. 
    It also configures fonts using Google Fonts and sets background 
    styling, including a blurred image effect for the ``"Hospital"`` theme.

    Parameters
    ----------
    theme : str
        The name of the theme to apply. Supported values include 
        ``"Light"``, ``"Dark"``, and ``"Hospital"``. Unrecognized 
        values fall back to the ``"Light"`` theme via ``get_palette``.

    Behavior
    --------
    - Injects CSS styles using ``st.markdown`` with ``unsafe_allow_html=True``.
    - Styles include:
        * Backgrounds (solid colors or image with blur effects).
        * Input fields (text, number, textarea).
        * Select boxes.
        * Buttons.
        * Tabs and tooltips.
        * Themed containers (e.g., ``.themed-box``).
    - Imports the selected font from Google Fonts.

    """
    palette = get_palette(theme)

    demo_field_style = """
        input[type="text"], input[type="number"], textarea {
            background-color: #a3b3aa !important;
        }
        .stSelectbox div[data-baseweb="select"] {
            background-color: #a3b3aa !important;
        }
    """ if st.session_state.get('use_demo') else ""

    bg_style = f'background-image: {palette["bg"]}; background-size: cover; background-position: center; background-attachment: fixed;' \
        if theme == "Hospital" else f'background-color: {palette["bg"]};'

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family={palette["font"].split(',')[0].replace(' ', '+')}&display=swap');
        html, body, [class*="st-"] {{
            font-family: {palette["font"]};
            color: {palette["input_color"]};
            {bg_style}
        }}
        .stApp {{
            {bg_style}
            {'backdrop-filter: blur(5px); padding: 20px; border-radius: 12px;' if theme=="Hospital" else ""}
        }}
        input[type="text"], input[type="number"], textarea {{
            background-color: {palette["input_bg"]} !important;
            color: {palette["input_color"]} !important;
            border: 1px solid {palette["border"]};
            border-radius: 6px;
        }}
        .stSelectbox div[data-baseweb="select"] {{
            background-color: {palette["input_bg"]} !important;
            color: {palette["input_color"]} !important;
        }}
        .stButton>button {{
            background-color: {palette["button_bg"]};
            color: {palette["button_color"]};
            font-weight: bold;
            border-radius: 6px;
        }}
        [data-testid="stTooltip"] {{
            background-color: {palette["tooltip_bg"]} !important;
            color: {palette["tooltip_color"]} !important;
            border: 1px solid {palette["border"]} !important;
            font-size: 0.85rem; border-radius: 6px; padding: 6px 10px;
        }}
        .themed-box {{
            background-color: {palette["input_bg"]};
            border: 1px solid {palette["border"]};
            border-radius: 12px;
            padding: 1px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stTabs {{
            background-color: {palette["input_bg"]};
            border: 1px solid {palette["border"]};
            border-radius: 12px;
            padding: 8px 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-top: 20px;
        }}
        .stTabs button {{
            border-radius: 8px;
            border: 1px solid {palette["border"]};
            background-color: {palette["input_bg"]};
            color: {palette["input_color"]};
            font-weight: bold;
            padding: 6px 12px;
            margin-right: 4px;
        }}
        .stTabs button[aria-selected="true"] {{
            background-color: {palette["button_bg"]};
            color: {palette["button_color"]};
            box-shadow: 0 1px 4px rgba(0,0,0,0.2);
        }}
        .tab-container {{
            padding: 10px;
            margin-top: 10px;
        }}
        {demo_field_style}
        </style>
    """, unsafe_allow_html=True)