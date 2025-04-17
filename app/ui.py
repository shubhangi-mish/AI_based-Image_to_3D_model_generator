import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Prompt-to-3D Generator", layout="centered")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🎨 Prompt to 3D Chat Interface")

CONFIG_URL = "http://localhost:8888/config?uid=super-user"
EXEC_URL = "http://localhost:8888/execution"
APP_IDS = [
    "c25dcd829d134ea98f5ae4dd311d13bc.node3.openfabric.network",
    "f0b5f319156c4819b9827000b17e511a.node3.openfabric.network"
]

def configure_backend():
    try:
        response = requests.post(
            CONFIG_URL,
            json={"app_ids": APP_IDS},
            headers={"accept": "application/json", "Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            st.success("✅ Backend configured successfully.")
        else:
            st.warning(f"⚠️ Config setup failed: {response.text}")
    except Exception as e:
        st.error(f"🔥 Error while connecting to backend: {e}")

if "configured" not in st.session_state:
    configure_backend()
    st.session_state.configured = True

with st.form("prompt_form", clear_on_submit=True):
    user_input = st.text_input("🗣 Enter your prompt:", placeholder="e.g., Describe a car")
    submitted = st.form_submit_button("Send")

def fetch_resource_data(resource_id, resource_type="image"):
    try:
        if resource_type == "image":
            url = f"https://c25dcd829d134ea98f5ae4dd311d13bc.node3.openfabric.network/resource?reid={resource_id}"
        elif resource_type == "model":
            url = f"https://f0b5f319156c4819b9827000b17e511a.node3.openfabric.network/resource?reid={resource_id}"
        else:
            return None

        return url 
    except Exception as e:
        st.error(f"🔥 Error while fetching resource: {e}")
        return None

if submitted and user_input:
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = requests.post(
            EXEC_URL,
            json={"attachments": ["string"], "prompt": user_input},
            headers={"accept": "application/json", "Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            full_message = result.get("message", "")

            try:
                prompt_section = full_message.split("🧠 Prompt:")[1].split("💬 LLM Response:")[0].strip()
                response_section = full_message.split("💬 LLM Response:")[1].split("🖼️ Text-to-Image Result:")[0].strip()
                image_url = full_message.split("🖼️ Text-to-Image Result:")[1].split("🔲 Image-to-3D Result:")[0].strip()
                model_url = full_message.split("🔲 Image-to-3D Result:")[1].strip()

                image_resource_url = fetch_resource_data(image_url, resource_type="image")
                model_resource_url = fetch_resource_data(model_url, resource_type="model")

                model_output = {
                    "prompt": prompt_section,
                    "response": response_section,
                    "image_url": image_resource_url,
                    "model_url": model_resource_url,
                }

            except Exception as parse_err:
                model_output = {"error": f"Failed to parse response: {parse_err}\n\nRaw message: {full_message}"}

        else:
            model_output = {"error": f"Backend Error: {response.status_code} - {response.text}"}

    except Exception as e:
        model_output = {"error": f"Request failed: {e}"}

    st.session_state.chat_history.append(("bot", model_output))

st.markdown("### 💬 Conversation")
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**🧑‍💻 You:** {msg}")
    else:
        if isinstance(msg, dict):
            if "error" in msg:
                st.error(msg["error"])
            else:
                st.markdown(f"**🧠 Prompt:** {msg['prompt']}")
                st.markdown(f"**🤖 LLM Response:** {msg['response']}")
                
                if msg["image_url"]:
                    st.markdown("📸 **Text-to-Image Result Link:**")
                    st.markdown(f"[Open Text-to-Image]({msg['image_url']})", unsafe_allow_html=True)
                    st.markdown("**Resource Path:**")
                    st.code(msg['image_url'], language="text")

                if msg["model_url"]:
                    st.markdown("🧱 **Image-to-3D Model Result Link:**")
                    st.markdown(f"[Open Image-to-3D Model]({msg['model_url']})", unsafe_allow_html=True)
                    st.markdown("**Resource Path:**")
                    st.code(msg['model_url'], language="text")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")
