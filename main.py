import streamlit as st
import openai

openai.api_key = st.secrets["api_key"]


def generate_response(user_input):
    gpt_prompt = [
        {
            "role": "system",
            "content": "Act as Steve Jobs. Respond like in stiuation of online chat to the input.",
        }
    ]

    gpt_prompt.append({"role": "user", "content": user_input})

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=gpt_prompt
    )

    prompt = gpt_response["choices"][0]["message"]["content"]
    return prompt


st.title("Chatbot Demo")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "Assistant",
            "content": "Hi!",
        }
    ]
    st.session_state.lock = False

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Hello! Who are you?"):
    user_input = prompt
    # output = generate_response(user_input)

    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("Assistant"):
        message_placeholder = st.empty()
        full_response = ""

    gpt_prompt = [
        {
            "role": "system",
            "content": "Analyze the user's question and identify the main topic. Define the main topic as main_key. Think of the correct answer to the question. Define the answer as anw. Think of a guiding question to lead the user to anw. Define the guiding question as lead_qus. Output main_key, anw, lead_qus in order in JSON format. Answer with Korean.",
        }
    ]
    gpt_prompt.append({"role": "user", "content": user_input})

    if not st.session_state.lock:
        for response in openai.ChatCompletion.create(
            model="gpt-4",
            messages=gpt_prompt,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌ ")

    else:
        full_response = "Password please"

    message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    st.session_state.messages.append(
        {
            "role": "Steve Jobs",
            "content": full_response,
        }
    )
