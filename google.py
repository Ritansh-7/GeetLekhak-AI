
import streamlit as st
import google.generativeai as genai

# Configure the API key
API_KEY = "AIzaSyA_4ZNak6We4FShdNJRkK_kg5zaqdpsvDo"
genai.configure(api_key=API_KEY)

# Set page configuration
st.set_page_config(
    page_title="AI Lyrics Generator",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FC466B 0%, #3F5EFB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding-top: 1.5rem;
    }

    .subtitle {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #FC466B 0%, #3F5EFB 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 30px;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    .parameter-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }

    .section-title {
        color: #333;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3F5EFB;
        padding-left: 10px;
    }

    .stSelectbox, .stMultiSelect, .stTextInput {
        margin-bottom: 1.2rem;
    }

    /* Custom radio buttons for language */
    .language-selection {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 0.5rem;
    }

    .language-option {
        padding: 8px 15px;
        background-color: #f1f3f9;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .language-option.selected {
        background: linear-gradient(90deg, #FC466B 0%, #3F5EFB 100%);
        color: white;
    }
    </style>
    <div class="main-title">✨ Lyrical Genius AI ✨</div>
    <div class="subtitle">Transform your ideas into beautiful lyrics in any language</div>
""", unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2 = st.tabs(["Create Lyrics", "About"])

with tab1:
    # Create columns for layout with a bit more space for the lyrics
    col1, col2 = st.columns([2, 3])

    with col1:
        # Parameters card
        with st.container():
            st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎸 Basic Settings</div>', unsafe_allow_html=True)

            # Genre with custom icon
            st.markdown("**🎵 Music Genre**")
            genre = st.selectbox(
                "",
                ["Pop", "Rock", "Hip Hop", "R&B", "Country", "Electronic", "Jazz",
                 "Metal", "Folk", "Blues", "Reggae", "Classical", "K-Pop", "Indie",
                 "Bollywood", "Bhojpuri Folk", "Sufi"]
            )

            # Mood with emojis
            mood_emoji = {
                "Happy": "😊", "Sad": "😢", "Energetic": "⚡", "Romantic": "❤️",
                "Motivational": "💪", "Melancholic": "🌧️", "Angry": "😠",
                "Peaceful": "🕊️", "Nostalgic": "🕰️", "Spiritual": "✨", "Playful": "🎮"
            }
            mood_options = list(mood_emoji.keys())

            st.markdown("**🎭 Mood**")
            mood = st.selectbox("", mood_options, format_func=lambda x: f"{mood_emoji[x]} {x}")

            # Theme
            st.markdown("**📝 Theme or Topic**")
            theme = st.text_input("", "Love and friendship")

            st.markdown("</div>", unsafe_allow_html=True)

            # Advanced settings card
            st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎼 Advanced Settings</div>', unsafe_allow_html=True)

            # Structure
            st.markdown("**🏗️ Song Structure**")
            structure = st.multiselect(
                "",
                ["Intro", "Verse", "Pre-Chorus", "Chorus", "Bridge", "Outro", "Hook", "Refrain", "Interlude"],
                default=["Verse", "Chorus", "Verse", "Chorus", "Bridge", "Chorus"]
            )

            # Reference Artist
            st.markdown("**🌟 Artist Inspiration**")
            style_artist = st.text_input("", placeholder="e.g., Taylor Swift, Arijit Singh, A.R. Rahman")

            # Length option
            st.markdown("**📏 Length**")
            length = st.select_slider(
                "",
                options=["Short", "Medium", "Long"],
                value="Medium"
            )

            # Language selection
            st.markdown("**🌐 Language**")
            language = st.radio(
                "",
                ["English", "Hindi", "Bhojpuri", "Bilingual (English & Hindi)"],
                horizontal=True
            )

            # Additional instructions
            st.markdown("**✨ Special Requests**")
            additional_instructions = st.text_area(
                "",
                placeholder="Any specific words, phrases, or styles you'd like to include...",
                height=100
            )

# Button to generate lyrics
generate_button = st.button("Generate Lyrics")


# Function to create the prompt
def create_lyrics_prompt(genre, mood, theme, structure, style_artist, additional_instructions):
    prompt = f"""Create original and creative song lyrics with the following specifications:

    Genre: {genre}
    Mood: {mood}
    Theme/Topic: {theme}
    Structure: {', '.join(structure)}

    """

    if style_artist:
        prompt += f"Write in a style inspired by {style_artist}, but make it original.\n"

    if additional_instructions:
        prompt += f"\nAdditional notes: {additional_instructions}\n"

    prompt += """
    Make the lyrics emotionally resonant, meaningful, and suitable for the specified genre.
    Include appropriate metaphors, imagery, and rhyme patterns.
    Format properly with clear sections (verse, chorus, etc.).
    BE ORIGINAL - don't copy existing songs.
    """

    return prompt


# Generate and display lyrics
if generate_button:
    with st.spinner("Creating your lyrics... This might take a moment ✨"):
        try:
            # Create the prompt
            prompt = create_lyrics_prompt(genre, mood, theme, structure, style_artist, additional_instructions)

            # Select model
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate response
            response = model.generate_content(prompt)

            # Display response on the right column
            with col2:
                st.subheader("Your Generated Lyrics:")
                st.markdown(f"**Genre:** {genre} | **Mood:** {mood} | **Theme:** {theme}")

                # Create a container with styled output
                lyrics_container = st.container()
                with lyrics_container:
                    st.markdown("""
                    <div style="background-color: #f0f0f0;
                                padding: 20px;
                                border-radius: 10px;
                                border-left: 5px solid #1DB954;">
                    """, unsafe_allow_html=True)

                    # Format the lyrics with proper line breaks
                    formatted_lyrics = response.text.replace("\n", "<br>")
                    st.markdown(f"<div style='white-space: pre-wrap;'>{formatted_lyrics}</div>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                # Add buttons to download or copy
                st.download_button(
                    label="Download Lyrics",
                    data=response.text,
                    file_name=f"{genre}_{mood}_lyrics.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please try again with different parameters or check your API key.")

# Add footer with information
st.markdown("""
<div style="text-align: center; margin-top: 3rem; color: #777; font-size: 0.8rem;">
    This application uses Google's Gemini API to generate creative content.<br>
    The lyrics generated are AI creations and may require human refinement.<br>
    Created with ❤️ using Streamlit and Google Generative AI
</div>
""", unsafe_allow_html=True)