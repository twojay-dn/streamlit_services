import streamlit as st
from default_value import config

def config_data_init(state_manager : st.session_state = st.session_state):
	state_manager.setdefault("model", "gpt-3.5-turbo")
	state_manager.setdefault("temperature", config["temperature"])
	state_manager.setdefault("max_tokens", config["max_tokens"])
	state_manager.setdefault("top_p", config["top_p"])
	state_manager.setdefault("frequency_penalty", config["frequency_penalty"])
	state_manager.setdefault("presence_penalty", config["presence_penalty"])

def sidebar(component : st.sidebar = st.sidebar, state_manager : st.session_state = st.session_state):
	config_data_init(state_manager)
	component.title("설정")
	component.write("모델: ", state_manager.model)
	temperature = component.slider("temperature", min_value=0.0, max_value=float(1.0), value=float(state_manager.temperature), step=0.1)
	max_tokens = component.slider("max_tokens", min_value=10, max_value=1024, value=state_manager.max_tokens, step=10)
	top_p = component.slider("top_p", min_value=0.0, max_value=float(1.0), value=float(state_manager.top_p), step=0.1)
	frequency_penalty = component.slider("frequency_penalty", min_value=0.0, max_value=float(1.0), value=float(state_manager.frequency_penalty), step=0.1)
	presence_penalty = component.slider("presence_penalty", min_value=0.0, max_value=float(1.0), value=float(state_manager.presence_penalty), step=0.1)
	if component.button("적용"):
		state_manager.temperature = temperature
		state_manager.max_tokens = max_tokens
		state_manager.top_p = top_p
		state_manager.frequency_penalty = frequency_penalty
		state_manager.presence_penalty = presence_penalty
	component.write("현재 적용된 설정값")
	config_dict = {
		"temperature": state_manager.temperature,
		"max_tokens": state_manager.max_tokens,
		"top_p": state_manager.top_p,
		"frequency_penalty": state_manager.frequency_penalty,
		"presence_penalty": state_manager.presence_penalty
	}
	component.write(config_dict)