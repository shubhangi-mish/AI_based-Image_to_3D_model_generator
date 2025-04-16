
# 🚀 The AI Developer Challenge

### Make Something Insanely Great
Welcome. This isn’t just a coding task. This is a mission. A calling for the bold and curious—those who dare to think
differently. If you're ready to build something magical, something powerful, something *insanely great*—read on.

---

## 🌟 The Vision

Imagine this:  
A user types a simple idea —
> “Make me a glowing dragon standing on a cliff at sunset.”

And your app...

- Understands the request using a local LLM.
- Generates stunning visuals from text.
- Transforms that image into an interactive 3D model.
- Remembers it. Forever.

You're not building an app. You're building **a creative partner**.

---

## 🎯 The Mission

Create an intelligent, end-to-end pipeline powered by Openfabric and a locally hosted LLM:

### Step 1: Understand the User

Use a local LLM like **DeepSeek** or **Llama** to:

- Interpret prompts
- Expand them creatively
- Drive meaningful, artistic input into the generation process

### Step 2: Bring Ideas to Life

Chain two Openfabric apps together:

- **Text to Image**  
  App ID: `f0997a01-d6d3-a5fe-53d8-561300318557`  
  [View on Openfabric](https://openfabric.network/app/view/f0997a01-d6d3-a5fe-53d8-561300318557)

- **Image to 3D**  
  App ID: `69543f29-4d41-4afc-7f29-3d51591f11eb`  
  [View on Openfabric](https://openfabric.network/app/view/69543f29-4d41-4afc-7f29-3d51591f11eb)

Use their **manifest** and **schema** dynamically to structure requests.

### Step 3: Remember Everything

Build memory like it matters.

- 🧠 **Short-Term**: Session context during a single interaction
- 💾 **Long-Term**: Persistence across sessions using SQLite, Redis, or flat files  
  Let the AI recall things like:

> “Generate a new robot like the one I created last Thursday — but this time, with wings.”

---

## 🛠 The Pipeline

User Prompt
↓
Local LLM (DeepSeek or LLaMA)
↓
Text-to-Image App (Openfabric)
↓
Image Output
↓
Image-to-3D App (Openfabric)
↓
3D Model Output

Simple. Elegant. Powerful.

---

## 📦 Deliverables

What we expect:

- ✅ Fully working Python project
- ✅ `README.md` with clear instructions
- ✅ Prompt → Image → 3D working example
- ✅ Logs or screenshots
- ✅ Memory functionality (clearly explained)

---

## 🧠 What We’re Really Testing

- Your grasp of the **Openfabric SDK** (`Stub`, `Remote`, `schema`, `manifest`)
- Your **creativity** in prompt-to-image generation
- Your **engineering intuition** with LLMs
- Your ability to manage **context and memory**
- Your **attention to quality** — code, comments, and clarity

---

## 🚀 Bonus Points

- 🎨 Visual GUI with Streamlit or Gradio
- 🔍 FAISS/ChromaDB for memory similarity
- 🗂 Local browser to explore generated 3D assets
- 🎤 Voice-to-text interaction

---

## ✨ Example Experience

Prompt:
> “Design a cyberpunk city skyline at night.”

→ LLM expands into vivid, textured visual descriptions  
→ Text-to-Image App renders a cityscape  
→ Image-to-3D app converts it into depth-aware 3D  
→ The system remembers the request for remixing later

That’s not automation. That’s imagination at scale.

---

## 💡 Where to start
You’ll find the project structure set, the entrypoint is in `main.py` file.
```python
############################################################
# Execution callback function
############################################################
def execute(model: AppModel) -> None:
    """
    Main execution entry point for handling a model pass.

    Args:
        model (AppModel): The model object containing request and response structures.
    """

    # Retrieve input
    request: InputClass = model.request

    # Retrieve user config
    user_config: ConfigClass = configurations.get('super-user', None)
    logging.info(f"{configurations}")

    # Initialize the Stub with app IDs
    app_ids = user_config.app_ids if user_config else []
    stub = Stub(app_ids)

    # ------------------------------
    # TODO : add your magic here
    # ------------------------------
                                
                                
                                
    # Prepare response
    response: OutputClass = model.response
    response.message = f"Echo: {request.prompt}"
```


## How to start
The application can be executed in two different ways:
* locally by running the `start.sh` 
* on in a docker container using `Dockerfile`

If all is fine you should be able to access the application on `http://localhost:8888/swagger-ui/#/App/post_execution` and see the following screen:

![Swagger UI](./swagger-ui.png)

## Ground Rules
Step up with any arsenal (read: libraries or packages) you believe in, but remember:
* 👎 External services like chatGPT are off-limits. Stand on your own.
* 👎 Plagiarism is for the weak. Forge your own path.
* 👎 A broken app equals failure. Non-negotiable.

## This Is It
We're not just evaluating a project; we're judging your potential to revolutionize our 
landscape. A half-baked app won’t cut it.

We're zeroing in on:
* 👍 Exceptional documentation.
* 👍 Code that speaks volumes.
* 👍 Inventiveness that dazzles.
* 👍 A problem-solving beast.
* 👍 Unwavering adherence to the brief