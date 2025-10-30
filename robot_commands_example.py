from local_llm import LocalLLM


if __name__ == "__main__":
    llm = LocalLLM()
    few_shot_examples = """
User command: Move ahead quickly -> Action: forward
User command: Go back a little -> Action: back
User command: Turn to your left -> Action: left
User command: Rotate right -> Action: right
User command: Please stop now -> Action: stop
"""
    
command = "Turn to your left"   # example command

    prompt = f"{few_shot_examples}\nUser command: {command} -> Action:"
    out = llm.generate(prompt, max_length=5, num_beams=4, early_stopping=True).lower()
    allowed = {"forward", "back", "left", "right", "stop"}
    action = out if out in allowed else "stop"
    print(f"Command: {command} -> Action: {action}")
