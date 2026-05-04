import json
import os

FILE_NAME = "contacts.json"

def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return json.load(f)

def save_contacts(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# ➕ ADD CONTACT
def add_contact(name: str, phone: str, email: str = "", city: str = ""):
    contacts = load_contacts()
    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "city": city
    })
    save_contacts(contacts)
    return f"{name} added successfully"

# 📋 GET ALL CONTACTS
def get_all_contacts():
    contacts = load_contacts()
    if not contacts:
        return "No contacts found"

    text = "Contacts:\n"
    for c in contacts:
        text += f"{c['name']} - {c['phone']} - {c.get('city','')}\n"
    return text

# 🔍 GET CONTACT
def get_contact(name: str):
    contacts = load_contacts()
    for c in contacts:
        if c["name"].lower() == name.lower():
            return f"{c['name']} - {c['phone']}"
    return "Contact not found"

# ✏ UPDATE CONTACT
def update_contact(name: str, phone: str):
    contacts = load_contacts()
    for c in contacts:
        if c["name"].lower() == name.lower():
            c["phone"] = phone
            save_contacts(contacts)
            return f"{name} updated"
    return "Contact not found"

# ❌ DELETE CONTACT
def delete_contact(name: str):
    contacts = load_contacts()
    contacts = [c for c in contacts if c["name"].lower() != name.lower()]
    save_contacts(contacts)
    return f"{name} deleted"