import streamlit as st

PINK = "#E65A8A"
CREAM = "#FFD45C"
MINT = "#62CFA9"
LIGHT_BLUE = "#5BA9E5"
LAVENDER = "#9B7BE1"

DARK = "#172348"
TEXT = "#30466F"
BACKGROUND = "#F7F8FD"


def load_styles():
    st.markdown(
        f"""
        <style>

        /* =========================================
           GLOBAL - MINIMIZED DESKTOP LAYOUT
        ========================================= */

        .stApp {{
            background: {BACKGROUND};
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            max-width: 1180px;
            padding-top: 14px;
            padding-bottom: 35px;
            padding-left: 24px;
            padding-right: 24px;
        }}

        [data-testid="stHorizontalBlock"] {{
            gap: 20px !important;
        }}

        [data-testid="column"] {{
            padding: 0 !important;
        }}

        /* =========================================
           HERO
        ========================================= */

        .hero {{
            position: relative;
            width: 100%;
            height: 145px;
            overflow: hidden;
            border-radius: 22px;
            background: #DCCCF7;
            box-sizing: border-box;
            margin: 0 0 20px 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .hero::before {{
            content: "";
            position: absolute;
            left: -55px;
            bottom: -65px;
            width: 170px;
            height: 105px;
            border-radius: 50%;
            background: rgba(180, 151, 239, 0.35);
        }}

        .hero::after {{
            content: "";
            position: absolute;
            right: -45px;
            bottom: -65px;
            width: 165px;
            height: 105px;
            border-radius: 50%;
            background: rgba(180, 151, 239, 0.30);
        }}

        .hero-content {{
            position: relative;
            z-index: 5;
            text-align: center;
            margin-left: 115px;
        }}

        .hero-title {{
            color: {DARK};
            font-size: 34px;
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: -0.7px;
        }}

        .hero-text {{
            color: #273B64;
            font-size: 14px;
            margin-top: 8px;
        }}

        .lion-mascot {{
            position: absolute;
            z-index: 4;
            left: 55px;
            bottom: -2px;
            width: 245px;
            height: 150px;
            object-fit: contain;
            object-position: center bottom;
            background: transparent;
        }}

        /* =========================================
           SECTION HEADING
        ========================================= */

        .section-heading {{
            color: {DARK};
            font-size: 23px;
            font-weight: 800;
            margin: 0 0 4px 0;
            line-height: 1.2;
        }}

        .section-description {{
            color: #647392;
            font-size: 13px;
            margin: 0 0 15px 0;
        }}

        /* =========================================
           CARDS
        ========================================= */

        .card {{
            position: relative;
            width: 100%;
            height: 155px;
            box-sizing: border-box;
            border-radius: 18px;
            padding: 19px 20px 58px 100px;
            margin: 0;
            overflow: hidden;
            box-shadow: 0 5px 13px rgba(44, 57, 91, 0.07);
        }}

        .card-icon {{
            position: absolute;
            left: 17px;
            top: 20px;
            width: 65px;
            height: 60px;
            object-fit: contain;
        }}

        .card-title {{
            color: {DARK};
            font-size: 18px;
            font-weight: 800;
            line-height: 1.2;
            margin-top: 1px;
        }}

        .card-text {{
            color: #30466F;
            font-size: 13px;
            line-height: 1.45;
            margin-top: 10px;
            max-width: 340px;
        }}

        /* =========================================
           BUTTONS
        ========================================= */

        .home-button {{
            margin-top: -48px;
            position: relative;
            z-index: 10;
        }}

        .home-button .stButton {{
            width: 100%;
        }}

        .home-button .stButton > button {{
            width: 100%;
            height: 40px;
            min-height: 40px;
            border-radius: 12px;
            border: none;
            font-size: 13px;
            font-weight: 800;
            padding: 0 10px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}

        .home-button .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(35, 45, 75, 0.13);
        }}

        .yellow-btn button {{
            background: #FFD24E !important;
            color: #172348 !important;
        }}

        .purple-btn button {{
            background: #9B75DF !important;
            color: white !important;
        }}

        .pink-btn button {{
            background: #E65A8A !important;
            color: white !important;
        }}

        .blue-btn button {{
            background: #3697DC !important;
            color: white !important;
        }}

        .green-btn button {{
            background: #27AE8A !important;
            color: white !important;
        }}

        /* =========================================
           RESPONSIVE
        ========================================= */

        @media (max-width: 900px) {{
            .block-container {{
                padding-left: 15px;
                padding-right: 15px;
            }}

            .lion-mascot {{
                left: 10px;
                width: 190px;
            }}

            .hero-content {{
                margin-left: 100px;
            }}
        }}

        @media (max-width: 700px) {{
            .hero {{
                height: 155px;
            }}

            .lion-mascot {{
                left: -10px;
                width: 150px;
                height: 140px;
            }}

            .hero-content {{
                margin-left: 75px;
            }}

            .hero-title {{
                font-size: 26px;
            }}

            .hero-text {{
                font-size: 12px;
            }}

            .card {{
                height: 155px;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
