import streamlit as st
import base64
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configuration de la page
st.set_page_config(
    page_title="Votre assistant IA 🌟",
    layout="wide",
    page_icon="🤖",
)

# CSS pour le design, les animations et la navbar
st.markdown(
    """
    <style>
    /* Modern theme with improved aesthetics */
    :root {
        --primary-color: #6366F1;
        --secondary-color: #4F46E5;
        --background-color: #F9FAFB;
        --surface-color: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #4B5563;
    }

    /* Global styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--background-color);
        color: var(--text-primary);
    }

    /* Navbar */
    .navbar {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .navbar img {
        width: 3rem;
        height: 3rem;
        filter: brightness(0) invert(1);
    }

    .navbar h1 {
        color: white;
        margin: 0;
        font-size: 1.75rem;
        font-weight: 700;
    }

    /* Buttons */
    .stButton button {
        background: var(--primary-color);
        color: white;
        border-radius: 0.75rem;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        background: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }

    /* Message boxes */
    .message-box {
        border-radius: 1rem;
        padding: 1rem;
        margin-bottom: 1rem;
        font-size: 1rem;
        line-height: 1.5;
        animation: fadeIn 0.3s ease-in-out;
    }

    .user-message {
        background-color: #EEF2FF;
        border-left: 4px solid var(--primary-color);
    }

    .system-message {
        background-color: #F3F4F6;
        border-left: 4px solid var(--secondary-color);
    }

    /* Image display */
    .uploaded-image {
        border-radius: 1rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease-in-out;
    }

    .uploaded-image:hover {
        transform: scale(1.05);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navbar avec logo et titre
st.markdown(
    """
    <div class="navbar">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712106.png" alt="Robot Logo">
        <h1>Votre assistant IA 🌟</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Configuration de l'API Gemini
# Il se pourrait que cette api_key ne soit pas utilisable. Vous pouvez la remplacée en créant votre propre clé sur https://ai.google.dev/gemini-api/docs/api-key?hl=fr
genai.configure(api_key="*")

# Fonction pour afficher les messages avec style
def display_message_with_copy(role, message, key):
    role_class = "user-message" if role == "user" else "system-message"
    role_label = "👤 Utilisateur" if role == "user" else "🤖 Système"
    st.markdown(
        f"""
        <div class="message-box {role_class}">
            <strong>{role_label} :</strong> {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
# Initialisation de l'état de session
if "history" not in st.session_state:
    st.session_state.history = []

# Fonction principale
def main():
    st.sidebar.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712106.png",
        width=120,
        caption="Votre assistant IA 🤖",
    )
    st.sidebar.markdown("### 🌟 Menu")
    file_type = st.sidebar.radio(
        "Que souhaitez-vous faire ?",
        ["💬 Chat question-réponse", "📄 Analyser un PDF", "🖼️ Décrire ou analyser des images","Générer des images"],
    )

    # Chat interactif
    if file_type == "💬 Chat question-réponse":
        st.subheader("💬 Posez une question")
        with st.form(key="chat_form"):
            user_question = st.text_input("Posez votre question ici 👇 :")
            submit_chat = st.form_submit_button("Envoyer 🚀")

        if submit_chat and user_question.strip():
            model = genai.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content(f"{user_question}")
            st.session_state.history.append(("user", user_question))
            st.session_state.history.append(("system", response.text))
            st.success("Réponse générée avec succès ! ✅")

    # Analyse de PDF
    elif file_type == "📄 Analyser un PDF":
        st.subheader("📄 Analysez vos fichiers PDF")
        pdf_docs = st.file_uploader(
            "Téléchargez vos fichiers PDF (formats acceptés : .pdf)",
            accept_multiple_files=True,
            type=["pdf"],
        )
        if pdf_docs:
            pdf_content = ""
            for pdf in pdf_docs:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    pdf_content += page.extract_text()

            if pdf_content:
                with st.form(key="pdf_form"):
                    user_question = st.text_input("Posez une question sur le contenu du PDF 📘 :")
                    submit_pdf = st.form_submit_button("Analyser le contenu 📜")

                if submit_pdf and user_question.strip():
                    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
                    prompt_pdf = f"Basé sur ce contenu PDF : {pdf_content[:]}.\nQuestion : {user_question}"
                    response_pdf = model.generate_content([prompt_pdf])
                    st.session_state.history.append(("user", user_question))
                    st.session_state.history.append(("system", response_pdf.text))
                    st.success("Analyse complétée avec succès ! 🎉")

    # Analyse d'images
    elif file_type == "🖼️ Décrire ou analyser des images":
        st.subheader("🖼️ Analysez vos images")
        image_files = st.file_uploader(
            "Téléchargez vos images (formats acceptés : JPEG, PNG)",
            accept_multiple_files=True,
            type=["jpeg", "jpg", "png"],
        )
        if image_files:
            st.markdown("### 📷 Images chargées :")
            for img in image_files:
                st.image(img, caption=f"Image : {img.name}", use_container_width ="auto", output_format="auto")
            with st.form(key="image_form"):
                user_prompt = st.text_input(
                    "Décrivez votre demande pour analyser les images 🖼️ :", 
                    "Décrivez les objets présents dans ces images."
                )
                submit_image = st.form_submit_button("Analyser les images 🖼️")

            if submit_image and user_prompt.strip():
                images_base64 = []
                for img in image_files:
                    img_data = img.read()
                    img_base64 = base64.b64encode(img_data).decode("utf-8")
                    images_base64.append(
                        {
                            "mime_type": f"image/{img.name.split('.')[-1]}",
                            "data": img_base64,
                        }
                    )

                model = genai.GenerativeModel(model_name="gemini-1.5-pro")
                response_image = model.generate_content([*images_base64, user_prompt])
                st.session_state.history.append(("user", user_prompt))
                st.session_state.history.append(("system", response_image.text))
                st.success("Analyse d'images réussie ! ✅")
    elif file_type=="Générer des images":
        st.subheader("Générer des images")
        with st.form(key="image_form"):
            user_prompt = st.text_input(
                "Donnez la description de ou des image(s) que vous voulez générer"
            )
            submit_image = st.form_submit_button("Générer les images ")

        if submit_image and user_prompt.strip():
            imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
            result = imagen.generate_images(
                prompt="Fuzzy bunnies in my kitchen",
                number_of_images=4,
                safety_filter_level="block_only_high",
                person_generation="allow_adult",
                aspect_ratio="3:4",
                negative_prompt="Outside",
            )
            for img in result.images:
                st.image(img, caption=f"Image : {img.name}", use_container_width ="auto", output_format="auto")
            # for image in result.images:
            #   print(image)
            # Open and display the image using your local operating system.
            # for image in result.images:
            #   image._pil_image.show()
    
#     # Historique des interactions
    st.subheader("📜 Historique des interactions")
    for idx, (role, message) in enumerate(st.session_state.history):
        display_message_with_copy(role, message, key=f"copy-{idx}")
if __name__ == "__main__":
    main()







# import streamlit as st
# import base64
# from PyPDF2 import PdfReader
# import google.generativeai as genai

# # Configuration de la page
# st.set_page_config(
#     page_title="Chatbot Pédagogique 🌟",
#     layout="wide",
#     page_icon="🤖",
# )

# # CSS pour le design, les animations et la navbar
# st.markdown(
#     """
#     <style>
#     /* Global styles */
#     body {
#         font-family: 'Arial', sans-serif;
#         background-color: #F8FAFC; /* Gris clair */
#         color: #333333;
#     }
#     /* Navbar */
#     .navbar {
#         background-color: #4CAF50; /* Vert */
#         padding: 10px 20px;
#         display: flex;
#         align-items: center;
#         justify-content: space-between;
#         border-radius: 8px;
#         margin-bottom: 20px;
#     }
#     .navbar img {
#         width: 40px;
#         height: 40px;
#     }
#     .navbar h1 {
#         color: white;
#         margin: 0;
#         font-size: 1.5rem;
#         font-weight: bold;
#     }
#     /* Boutons */
#     .stButton button {
#         background-color: #007BFF; /* Bleu */
#         color: white;
#         border-radius: 12px;
#         border: none;
#         padding: 10px 18px;
#         font-weight: bold;
#         transition: transform 0.2s, box-shadow 0.2s;
#     }
#     .stButton button:hover {
#         background-color: #0056b3; /* Bleu foncé */
#         transform: scale(1.05);
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#     }
#     /* Message boxes */
#     .message-box {
#         border-radius: 10px;
#         padding: 15px;
#         margin-bottom: 15px;
#         font-size: 16px;
#         word-wrap: break-word;
#         overflow-wrap: break-word;
#         transition: background-color 0.3s ease-in-out, transform 0.2s ease-in-out;
#     }
#     .message-box:hover {
#         transform: scale(1.02);
#     }
#     .user-message {
#         background-color: #E3F2FD; /* Bleu clair */
#         color: #0D47A1;
#     }
#     .system-message {
#         background-color: #C8E6C9; /* Vert clair */
#         color: #1B5E20;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Navbar avec logo et titre
# st.markdown(
#     """
#     <div class="navbar">
#         <img src="https://cdn-icons-png.flaticon.com/512/4712/4712106.png" alt="Robot Logo">
#         <h1>Chatbot Pédagogique 🌟</h1>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# # Configuration de l'API Gemini
# genai.configure(api_key="AIzaSyCyjpR-nXL0JR0A2mW5537e1ybODU5ZEuM")

# # Fonction pour afficher les messages avec style
# def display_message_with_copy(role, message, key):
#     role_class = "user-message" if role == "user" else "system-message"
#     role_label = "👤 Utilisateur" if role == "user" else "🤖 Système"
#     st.markdown(
#         f"""
#         <div class="message-box {role_class}">
#             <strong>{role_label} :</strong> {message}
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # Initialisation de l'état de session
# if "history" not in st.session_state:
#     st.session_state.history = []

# # Fonction principale
# def main():
#     st.sidebar.image(
#         "https://cdn-icons-png.flaticon.com/512/4712/4712106.png",
#         width=120,
#         caption="Votre assistant IA 🤖",
#     )
#     st.sidebar.markdown("### 🌟 Menu")
#     file_type = st.sidebar.radio(
#         "Que souhaitez-vous faire ?",
#         ["💬 Chat question-réponse", "📄 Analyser un PDF", "🖼️ Décrire ou analyser des images"],
#     )

#     # Chat interactif
#     if file_type == "💬 Chat question-réponse":
#         st.subheader("💬 Posez une question")
#         with st.form(key="chat_form"):
#             user_question = st.text_input("Posez votre question ici 👇 :")
#             submit_chat = st.form_submit_button("Envoyer 🚀")

#         if submit_chat and user_question.strip():
#             model = genai.GenerativeModel(model_name="gemini-1.5-pro")
#             response = model.generate_content(f"{user_question}")
#             st.session_state.history.append(("user", user_question))
#             st.session_state.history.append(("system", response.text))
#             st.success("Réponse générée avec succès ! ✅")

#     # Analyse de PDF
#     elif file_type == "📄 Analyser un PDF":
#         st.subheader("📄 Analysez vos fichiers PDF")
#         pdf_docs = st.file_uploader(
#             "Téléchargez vos fichiers PDF (formats acceptés : .pdf)",
#             accept_multiple_files=True,
#             type=["pdf"],
#         )
#         if pdf_docs:
#             pdf_content = ""
#             for pdf in pdf_docs:
#                 pdf_reader = PdfReader(pdf)
#                 for page in pdf_reader.pages:
#                     pdf_content += page.extract_text()

#             if pdf_content:
#                 with st.form(key="pdf_form"):
#                     user_question = st.text_input("Posez une question sur le contenu du PDF 📘 :")
#                     submit_pdf = st.form_submit_button("Analyser le contenu 📜")

#                 if submit_pdf and user_question.strip():
#                     model = genai.GenerativeModel(model_name="gemini-1.5-pro")
#                     prompt_pdf = f"Basé sur ce contenu PDF : {pdf_content[:500]}.\nQuestion : {user_question}"
#                     response_pdf = model.generate_content([prompt_pdf])
#                     st.session_state.history.append(("user", user_question))
#                     st.session_state.history.append(("system", response_pdf.text))
#                     st.success("Analyse complétée avec succès ! 🎉")

#     # Analyse d'images
#     elif file_type == "🖼️ Décrire ou analyser des images":
#         st.subheader("🖼️ Analysez vos images")
#         image_files = st.file_uploader(
#             "Téléchargez vos images (formats acceptés : JPEG, PNG)",
#             accept_multiple_files=True,
#             type=["jpeg", "jpg", "png"],
#         )
#         if image_files:
#             with st.form(key="image_form"):
#                 user_prompt = st.text_input(
#                     "Décrivez votre demande pour analyser les images 🖼️ :", 
#                     "Décrivez les objets présents dans ces images."
#                 )
#                 submit_image = st.form_submit_button("Analyser les images 🖼️")

#             if submit_image and user_prompt.strip():
#                 images_base64 = []
#                 for img in image_files:
#                     img_data = img.read()
#                     img_base64 = base64.b64encode(img_data).decode("utf-8")
#                     images_base64.append(
#                         {
#                             "mime_type": f"image/{img.name.split('.')[-1]}",
#                             "data": img_base64,
#                         }
#                     )

#                 model = genai.GenerativeModel(model_name="gemini-1.5-pro")
#                 response_image = model.generate_content([*images_base64, user_prompt])
#                 st.session_state.history.append(("user", user_prompt))
#                 st.session_state.history.append(("system", response_image.text))
#                 st.success("Analyse d'images réussie ! ✅")

#     # Historique des interactions
#     st.subheader("📜 Historique des interactions")
#     for idx, (role, message) in enumerate(st.session_state.history):
#         display_message_with_copy(role, message, key=f"copy-{idx}")


# if __name__ == "__main__":
#     main()



