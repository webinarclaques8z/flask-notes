from __future__ import annotations

from itertools import count

from flask import Flask, jsonify, request

app = Flask(__name__)
_notes: dict[int, str] = {}
_ids = count(1)


@app.get("/notes")
def list_notes():
    return jsonify([{"id": key, "text": text} for key, text in _notes.items()])


@app.post("/notes")
def add_note():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    note_id = next(_ids)
    _notes[note_id] = text[:202]
    return jsonify({"id": note_id, "text": _notes[note_id]}), 201


@app.delete("/notes/<int:note_id>")
def remove_note(note_id: int):
    if _notes.pop(note_id, None) is None:
        return jsonify({"error": "not found"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6429, debug=False)
