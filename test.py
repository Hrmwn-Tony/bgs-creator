import os
import glob
import json
import shlex
from dotenv import load_dotenv
from google import genai
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import subprocess

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

def combine_sounds(OUTPUT_DIR, pattern, layer):
    print(f"Combining {pattern} audiofiles...")
    input_command = "ffmpeg"
    output_files = glob.glob(f"{OUTPUT_DIR}/*{pattern}*")
    temp = ""
    file_count = len(output_files)

    for file in output_files:
        temp_command = f"{input_command} -i {file}"
        input_command = temp_command
        temp += f"[{output_files.index(file)}:a] "
    
    combine_command = f"{temp}amix=inputs={file_count}[a_mixed]"
    full_command_str = f"{input_command} -filter_complex \"{combine_command}\" -map \"[a_mixed]\" {OUTPUT_DIR}/group_{pattern}.mp3"
    shell_command = shlex.split(full_command_str)
    print(shell_command)
    
    try:
        subprocess.run(shell_command, check=True, capture_output=True, text=True)
        print(f"Sucessfully combined {pattern} audiofiles")
    except FileNotFoundError:
        print("Error: FFmpeg is not installed or not in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg command:")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


    #search file pattern
    #put that file into array
    #use for loop


    #file_count = 
    #filename =
    # ffmpeg -i groupA_file1.mp3 -i groupA_file2.mp3 \ -filter-complex "[0:a] [1:a] amix=inputs=2 [groupA]"
    

def main():
    if not GEMINI_KEY and ELEVEN_KEY:
        print("Error: API Key not found")
        return

    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating output directory: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR)
    
    combine_sounds(OUTPUT_DIR,"layer1", 1)
    combine_sounds(OUTPUT_DIR,"layer2", 2)
    combine_sounds(OUTPUT_DIR,"layer3", 3)
    '''
    prompts = generate_prompt(USER_PROMPT)
    generate_sound(prompts, OUTPUT_DIR)
    '''
   
if __name__ == "__main__":
    main()
#check if directory exist
#check API needed
#get the json file





    

#def #call

