import streamlit as st
import requests

st.set_page_config(page_title="Prompt-to-3D Generator", layout="centered")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🎨 Prompt to 3D Chat Interface")

st.markdown("## 🌟 Remix Your Prompt Magic! 🌈")
remix_option = st.radio(
    "✨ Would you like to remix your prompt with earlier memory?",
    options=["No", "Yes"],
    index=0,
    horizontal=True
)

if remix_option == "Yes":
    placeholder_text = "Tell me what previous visual you want to remix and how?"
else:
    placeholder_text = "Let's start fresh! What are you thinking? Lemme build it for you."

# Prompt form
with st.form("prompt_form", clear_on_submit=False):
    user_input = st.text_input("🗣 Your creative prompt:", placeholder=placeholder_text)
    submitted = st.form_submit_button("Send")

CONFIG_URL = "http://localhost:8888/config?uid=super-user"
EXEC_URL = "http://localhost:8888/execution"
REMIX_URL = "http://localhost:5000/remix"
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

def call_execution(prompt):
    try:
        response = requests.post(
            EXEC_URL,
            json={"attachments": ["string"], "prompt": prompt},
            headers={"accept": "application/json", "Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            return result.get("message", "")
        else:
            return f"Backend Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Request failed: {e}"

def call_remix(original_prompt):
    try:
        response = requests.post(
            REMIX_URL,
            json={"prompt": original_prompt},
            headers={"accept": "application/json", "Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            return result.get("remixed_prompt", original_prompt)
        else:
            return f"Remix API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Remix API Request failed: {e}"

if submitted:
    if user_input:
        st.write(f"📥 User input received: {user_input}")  

        st.session_state.chat_history.append(("user", user_input))
        final_prompt = user_input

        if remix_option == "Yes":
            st.write("🔁 Remix selected")
            remix_result = call_remix(user_input)
            if remix_result.startswith("Remix API Error") or remix_result.startswith("Remix API Request failed"):
                st.session_state.chat_history.append(("bot", {"error": remix_result}))
            else:
                final_prompt = remix_result
        else:
            st.write("🚀 Remix not selected, using original prompt")

        st.write(f"📤 Final prompt going to execution: {final_prompt}")
        full_message = call_execution(final_prompt)
        st.write("📬 Execution API response received")

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

        st.session_state.chat_history.append(("bot", model_output))
    else:
        st.warning("⚠️ No input received")


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
                    st.code(msg['image_url'], language="text")

                if msg["model_url"]:
                    st.markdown("🧱 **Image-to-3D Model Result Link:**")
                    st.markdown(f"[Open Image-to-3D Model]({msg['model_url']})", unsafe_allow_html=True)
                    st.code(msg['model_url'], language="text")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")
