# robo_script_generator.py

def generate_robo_script(actions):
    """
    Generates a Robo script from a list of actions.
    """
    script = []
    for action in actions:
        if action['type'] == 'click':
            script.append(f"adb shell input tap {action['x']} {action['y']}")
        elif action['type'] == 'type':
            script.append(f"adb shell input text '{action['text']}'")
    
    return "\n".join(script)
