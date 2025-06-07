import os
from google import genai
from google.genai import types
from nova_act import NovaAct

# Gemini API key
API_KEY = "AIzaSyB2nmWsJ4zLqOG2Q1fFZEnfMKRG325yIhk"

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Step 1: Open Tinkercad and log in
with NovaAct(starting_page="https://www.tinkercad.com/dashboard") as nova:
    nova.start()
    #nova.act("wait for login button to appear")
    #nova.act("click on login")
    nova.act("wait for personal account option")
    nova.act("click on personal account")
   
   
    input("\U0001F449 Please complete the Google sign-in and 2-Step Verification manually, then press ENTER to continue...") # May require credentials setup in browser session

    # Step 2: Create a new circuit project
    nova.act("wait for create button to appear")
    nova.act("click on create new")
    nova.act("select circuits")

    # Step 3: Ask user for natural language prompt
    query_re = input("What project do you want to build? (e.g., 'Build a circuit to blink an LED using Arduino')\n>> ")

    # Step 4: Send user prompt to Gemini
    try:
        gemini_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query_re,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a circuit planner for Tinkercad. Understand the user's request, analyze which components are required, how they should be connected, and provide exact NovaAct-style step-by-step action instructions to build the circuit.\n"
                    "Return only a Python list of strings, each string being a valid NovaAct action (e.g., 'click on resistor', 'drag from pin A to pin B'). Do not include nova.act() wrapper."
                )
            )
        )

        # Step 5: Extract action steps from Gemini response
        instructions_code = gemini_response.text.strip()
        action = eval(instructions_code) if instructions_code.startswith('[') else []

        # Step 6: Execute the action list
        for j in action:
            print(f"Executing: {j}")
            nova.act(j)

        # Step 7: Start simulation
        nova.act("wait for start simulation button")
        nova.act("click on start simulation")

    except Exception as e:
        print("[Error during Gemini interaction or execution]", e)
