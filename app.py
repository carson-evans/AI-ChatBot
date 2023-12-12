from transformers import AutoModelForCasualLM, AutoTokenizer
import gradio as gr
import torch

title = "AI ChatBot"
description = "Building a chatbot using HuggingFace's transformers library and Gradio."
examples = [["How are you?"]]

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCasualLM.from_pretrained("microsoft/DialoGPT-large")

def predict(input, history=[]):
    # tokenize the new input sentence
    new_user_input_ids = tokenizer.encode(
        input + tokenizer.eos_token, return_tensors="pt"
    )

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([torch.LongTensor(history), new_user_input_ids], dim=-1)

    # generate a response
    history = model.generate(
        bot_input_ids, max_length=4000, pad_token_id=tokenizer.eos_token_id
    ).tolist()

    # convert the tokens to text, and then split the responses into lines
    response = tokenizer.decode(history[0]).split("<|endoftext|>")
    # print('decoded_response-->>'+str(response))
    response = [
        (response[i], response[i + 1]) for i in range(0, len(response) - 1, 2)
    ]  # convert to tuples of list
    # print('response-->>'+str(response))
    return response, history


gr.Interface(
    fn=predict,
    title=title,
    description=description,
    examples=examples,
    inputs=["text", "state"],
    outputs=["chatbot", "state"],
    theme="finlaymacklon/boxy_violet",
).launch()