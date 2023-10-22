from flask import Flask, render_template, request, jsonify
import json
from ca_csmgpt.agents import ca_csmgpt
from langchain.chat_models import ChatLiteLLM

app = Flask(__name__)

# Load configuration from config.json
with open('config.json', 'r') as file:
    config = json.load(file)

@app.route('/')
def index():
    return render_template('index.html', custom_css=config['style']['custom_css'])

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    
    # Initialize the chatbot using your existing logic
    llm = ChatLiteLLM(temperature=0.2)
    sales_agent = ca_csmgpt.from_llm(llm, **config['agent_setup'])
    
    # Process the user_message using your chatbot logic
    sales_agent.human_step(user_message)
    bot_response = sales_agent.conversation_history[-1]
    
    return jsonify(bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)
