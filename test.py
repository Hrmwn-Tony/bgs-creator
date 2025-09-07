import os
import json
from dotenv import load_dotenv
from google import genai
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()
OUTPUT_DIR = "/home/ubuntu-victus/project/bgs-creator/output"
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key = ELEVEN_KEY)
#geminiclient = genai.Client(api_key=api_key)
USER_PROMPT = "tldr"
def generate_prompt(text):
    try:
        with open('/home/ubuntu-victus/project/bgs-creator/prompt.json', 'r') as f:
            content_prompt = json.load(f)
            return content_prompt
    except Exception as e:
        print(f"Error accessing prompt JSON: {e}")


def generate_sound(content_prompt, OUTPUT_DIR):
    for layer, prompts in content_prompt.items():
        prefix = layer
        suffix = 0
        print(f"---{layer}---")
        for prompt in prompts:
            print(f"Generating sound: {prompt[:50]}")
            try:
                audio = elevenlabs.text_to_sound_effects.convert(
                    text = prompt,
                    duration_seconds = 10.0,
                    loop = "true")
                output_filename = f"{OUTPUT_DIR}/output_{prefix}_{suffix}.mp3"
                try:
                    with open(output_filename, "wb") as f:
                        for chunk in audio:
                            f.write(chunk)
                    suffix += 1
                except Exception as e:
                    print(f"Error ocured: {e}")
            except Exception as e :
                print(f"Error in API request: {e}")

def main():
    if not GEMINI_KEY and ELEVEN_KEY:
        print("Error: API Key not found")
        return

    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating output directory: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR)

    prompts = generate_prompt(USER_PROMPT)
    generate_sound(prompts, OUTPUT_DIR)


if __name__ == "__main__":
    main()
#check if directory exist
#check API needed
#get the json file





    

#def #call

