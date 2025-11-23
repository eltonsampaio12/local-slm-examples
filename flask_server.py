from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask, request, jsonify
from flasgger import Swagger

from local_llm import LocalLLM
from latimer_client import LatimerClient


app = Flask(__name__)
swagger = Swagger(app)
llm = LocalLLM()


@app.route("/generate", methods=["POST"])
def generate():
    """
    Generate text from a prompt using local LLM
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
              example: "You are a robot command interpreter. Given a user command in plain English, return a single key 'action' whose value is ONE of => forward, back, left, right, or stop. Always return lowercase, without punctuation or extra words. Just return the action, no other text."
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
      500:
        description: Generation error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json(silent=True) or {}
        user_prompt = data.get("prompt", "").strip()
        system_prompt = data.get("system", "").strip()

        if not user_prompt:
            return jsonify({"error": "Missing 'prompt' in JSON body"}), 400

        if system_prompt:
            prompt = f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
        else:
            prompt = user_prompt

        text = llm.generate(prompt)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": f"Generation error: {str(e)}"}), 500


@app.route("/generate/latimer", methods=["POST"])
def generate_latimer():
    """
    Generate text from a prompt using Latimer API
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
              example: "You are a robot command interpreter. Given a user command in plain English, return a single key 'action' whose value is ONE of => forward, back, left, right, or stop. Always return lowercase, without punctuation or extra words. Just return the action, no other text."
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
        description: Missing required fields or API key not set
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: API error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json(silent=True) or {}
        user_prompt = data.get("prompt", "").strip()
        system_prompt = data.get("system", "").strip()

        if not user_prompt:
            return jsonify({"error": "Missing 'prompt' in JSON body"}), 400

        latimer_client = LatimerClient()
        text = latimer_client.generate(user_prompt, system_prompt=system_prompt)
        if text is None:
            return jsonify({"error": "Failed to generate response from Latimer API"}), 500
        return jsonify({"text": text})
    except ValueError:
        return (
            jsonify(
                {
                    "error": "Latimer API not available. Set LATIMER_API_KEY environment variable."
                }
            ),
            400,
        )
    except Exception as e:
        return jsonify({"error": f"Latimer API error: {str(e)}"}), 500


if __name__ == "__main__":
    # Run with: FLASK_APP=flask_server.py flask run --host=0.0.0.0 --port=5000
    app.run(host="0.0.0.0", port=8000, debug=True)


