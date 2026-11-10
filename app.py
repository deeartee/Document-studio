import streamlit as st
import easyocr
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Vogue Reader",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;600&display=swap');

        /* Чистый фон */
        .stApp {
            background-color: #fafafa;
        }

        /* Базовые стили */
        h1, h2, h3, h4 {
            font-family: 'Playfair Display', serif !important;
            color: #111111 !important;
            font-weight: 400;
        }

        p, span, div, label {
            font-family: 'Montserrat', sans-serif;
            color: #333333 !important;
            font-weight: 300;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        /* Заголовок журнала */
        .vogue-header {
            text-align: center;
            border-bottom: 1px solid #111;
            padding-bottom: 1rem;
            margin-bottom: 3rem;
        }

        .vogue-title {
            font-family: 'Playfair Display', serif;
            font-size: 5rem;
            font-weight: 700;
            letter-spacing: -2px;
            line-height: 1;
            margin: 0;
            text-transform: uppercase;
        }

        .vogue-subtitle {
            font-family: 'Montserrat', sans-serif;
            font-size: 0.8rem;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: #666 !important;
            margin-top: 10px;
        }

        /* Колонки */
        .editorial-img {
            width: 100%;
            border: 1px solid #ddd;
            padding: 5px;
            background: #fff;
            box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        }

        /* Текст */
        .editorial-text {
            font-family: 'Playfair Display', serif;
            font-size: 1.15rem;
            line-height: 1.8;
            text-align: justify;
            color: #222 !important;
            margin-bottom: 1.5rem;
            position: relative;
        }

        /* Буквица (Drop Cap) */
        .editorial-text::first-letter {
            font-size: 4rem;
            float: left;
            line-height: 0.8;
            margin-right: 12px;
            margin-top: 5px;
            font-weight: 700;
        }

        /* Разделитель */
        .divider {
            height: 1px;
            background: #ddd;
            margin: 2rem 0;
        }

        /* Загрузчик */
        div[data-testid="stFileUploader"] {
            background: transparent;
            border: 1px dashed #999;
            padding: 1rem;
            border-radius: 0;
        }

        div[data-testid="stFileUploader"] button {
            background-color: #111 !important;
            color: #fff !important;
            border-radius: 0 !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 400 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 0.5rem 1.5rem !important;
            border: none !important;
        }

        /* Скрываем лишнее */
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="vogue-header">
        <div class="vogue-title">VOGUE</div>
        <div class="vogue-subtitle">Hotel Document Scanning · Vol. 17</div>
    </div>
    """,
    unsafe_allow_html=True
)

@st.cache_resource(show_spinner=False)
def load_vogue_engine():
    return easyocr.Reader(['ru', 'en'], gpu=False)

engine = load_vogue_engine()

st.markdown("<p style='text-align: center; letter-spacing: 1px; font-size: 0.9rem;'>ЗАГРУЗИТЕ СКАН ДОКУМЕНТА ДЛЯ ПУБЛИКАЦИИ</p>", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Выберите фото",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded:
    img = Image.open(uploaded)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Несимметричные колонки (2:1)
    col_img, col_text = st.columns([1.5, 1], gap="large")
    
    with col_img:
        st.markdown('<p style="font-size: 0.7rem; letter-spacing: 2px; color: #888;">PORTRAIT OF THE GUEST</p>', unsafe_allow_html=True)
        st.markdown('<div class="editorial-img">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 0.7rem; color: #888; margin-top: 10px; text-align: right;">Photo: {}</p>'.format(uploaded.name), unsafe_allow_html=True)
        
    with col_text:
        st.markdown('<p style="font-size: 0.7rem; letter-spacing: 2px; color: #888;">THE EXCLUSIVE INTERVIEW</p>', unsafe_allow_html=True)
        
        with st.spinner("Редактор набирает текст..."):
            img_array = np.array(img)
            extracted = engine.readtext(img_array, detail=0)
            
        if extracted:
            # Выводим первую строку как заголовок
            if len(extracted) > 0:
                st.markdown(f"<h2 style='font-size: 2rem; margin-bottom: 1rem;'>{extracted[0]}</h2>", unsafe_allow_html=True)
            
            # Остальное как текст статьи
            full_text = " ".join(extracted[1:]) if len(extracted) > 1 else " "
            st.markdown(f'<div class="editorial-text">{full_text}</div>', unsafe_allow_html=True)
            
            filename = f"vogue_dossier_{uploaded.name}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(extracted))
                
            st.markdown(f"<p style='font-size: 0.8rem; color: #888; margin-top: 2rem; border-top: 1px solid #ddd; padding-top: 10px;'>Archived in: <i>{filename}</i></p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #999;'><i>Текст не обнаружен. Попробуйте другой кадр.</i></p>", unsafe_allow_html=True)