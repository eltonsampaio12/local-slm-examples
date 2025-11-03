from flask import Flask, request, jsonify
from flasgger import Swagger

from local_llm import LocalLLM


app = Flask(__name__)
swagger = Swagger(app)
llm = LocalLLM()


@app.route("/generate", methods=["POST"])
def generate():
    """
    Generate text from a prompt using the local LLM
    ---
    tags:
      - generation
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            system:
              type: string
              description: Optional system guidance prepended to the prompt
              example: "You are a robot command interpreter. Given a user command in plain English, return a single key 'action' whose value is ONE of => forward, back, left, right, or stop. Always return lowercase, without punctuation or extra words."
            prompt:
              type: string
              description: The user prompt text
              example: "User command: Move to forward ->"
    responses:
      200:
        description: Successful generation
        schema:
          type: object
          properties:
            text:
              type: string
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            error:
              type: string
    """
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


