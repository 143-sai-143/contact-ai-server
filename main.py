from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

# ✅ ROOT ROUTE (fix for your issue)
@app.get("/")
def home():
    return {"message": "API is running successfully"}

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory DB
contacts = []

# ---------- Models ----------

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str

# ---------- Helpers ----------

def format_contacts():
    if not contacts:
        return "No contacts found"
    return "\n".join(
        f"{c['name']} - {c['phone']} ({c['city']})"
        for c in contacts
    )

def is_duplicate(phone):
    return any(c["phone"] == phone for c in contacts)

# ---------- Chat API ----------

@app.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest):
    text = data.message.lower().strip()
    session_id = str(uuid.uuid4())

    # ➕ ADD
    if "add" in text:
        try:
            words = text.split()
            name, phone, city = "", "", ""

            for i, word in enumerate(words):
                if word == "add" and i + 1 < len(words):
                    name = words[i + 1]
                elif word == "phone" and i + 1 < len(words):
                    phone = words[i + 1]
                elif word == "city" and i + 1 < len(words):
                    city = words[i + 1]

            if not name or not phone:
                return {"reply": "Please provide name and phone", "session_id": session_id}

            if is_duplicate(phone):
                return {"reply": "Contact already exists", "session_id": session_id}

            contacts.append({
                "name": name,
                "phone": phone,
                "city": city
            })

            return {"reply": f"{name} added successfully", "session_id": session_id}

        except Exception:
            return {"reply": "Use: add name phone 123 city xyz", "session_id": session_id}

    # 📄 SHOW
    elif "show" in text or "list" in text:
        return {"reply": format_contacts(), "session_id": session_id}

    # 🔍 FIND
    elif "find" in text or "search" in text:
        query = text.replace("find", "").replace("search", "").strip()

        for c in contacts:
            if query in c["name"] or query in c["phone"]:
                return {
                    "reply": f"{c['name']} - {c['phone']} ({c['city']})",
                    "session_id": session_id
                }

        return {"reply": "Contact not found", "session_id": session_id}

    # ❌ DELETE
    elif "delete" in text or "remove" in text:
        query = text.replace("delete", "").replace("remove", "").strip()

        for c in contacts:
            if query in c["name"] or query in c["phone"]:
                contacts.remove(c)
                return {"reply": "Contact deleted successfully", "session_id": session_id}

        return {"reply": "Contact not found", "session_id": session_id}

    # 🤖 Default
    return {"reply": "Hi, how can I help you?", "session_id": session_id}


# ---------- Contacts API ----------

@app.get("/contacts")
def get_contacts():
    return contacts