from flask import Flask, request, jsonify

from local_llm import LocalLLM


app = Flask(__name__)
llm = LocalLLM()


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    user_prompt = data.get("prompt", "").strip()
    system_prompt = data.get("system", "").strip()
    if system_prompt:
        prompt = f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
    else:
        prompt = user_prompt
    if not prompt:
        return jsonify({"error": "Missing 'prompt' in JSON body"}), 400

    text = llm.generate(prompt)
    return jsonify({"text": text})


if __name__ == "__main__":
    # Run with: FLASK_APP=flask_server.py flask run --host=0.0.0.0 --port=5000
    app.run(host="0.0.0.0", port=8000, debug=True)


