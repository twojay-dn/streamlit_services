import streamlit as st
from typing import Callable, Literal, List, Tuple

title_description = "Sidebar"
page_choise_description = "Sidebar"

class Sidebar:
    name = title_description
    
    @classmethod
    def render(cls):
        from src.Views import View_pages
       
        st.sidebar.title(cls.name)
        cls.page = st.sidebar.selectbox(
            page_choise_description,
            options=View_pages.get_view_list(retrieve_value=True), 
            index=0
        )
        
    @classmethod
    def get_selected_page(cls):
        return cls.page

class BaseColumns:
    def __init__(self,
            column_callbacks : List[Callable] = None,
            widths : List[int] = None,
            gap : Literal["small", "medium", "large"] = "small"
        ):
        if column_callbacks is None:
            column_callbacks = []
        if not all(isinstance(column_callback, Callable) for column_callback in column_callbacks):
            raise ValueError("All column_callbacks must be callable")
        if widths is None:
            self.columns_count_with_widths = [1] * len(column_callbacks)
        else:
            self.columns_count_with_widths = widths
        self.columns = enumerate(column_callbacks)
        self.gap = gap

    def add_column(self, column_callback : Callable):
        if not isinstance(column_callback, Callable):
            raise ValueError("column_callback must be a callable")
        self.columns.append(column_callback)

    def render(self):
        col_list = st.columns(
            self.columns_count_with_widths,
            gap = self.gap
        )
        for index, column_callback in self.columns:
            with col_list[index]:
                column_callback()

class VerticalColumns(BaseColumns):
    def __init__(self,
            column_callbacks : List[Callable] = None,
            widths : List[int] = None,
            gap : Literal["small", "medium", "large"] = "small",
        ):
        super().__init__(column_callbacks, widths, gap)
        self.columns = column_callbacks

    def render(self):
        containers = [st.container() for _ in range(len(self.columns))]
        for callback, container in zip(self.columns, containers):
            with container:
                callback()
                st.divider()

class BasePage:
    def __init__(self, name : str, description : str = None):
        self.name = name
        self.description = description
        
    def render(self, impl_callback : Callable):
        st.title(self.name)
        if self.description is not None:
            st.subheader(self.description)
        impl_callback()

from functools import wraps
def render_page(name: str, description: str = None):
    def decorator(func):
        assert name is not None, "Name is required"
        assert hasattr(func, '__call__'), "Function is required"
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = BasePage(name, description)
            page.render(func)
        return wrapper
    return decorator

from src.Controllers.ChatMemory import BaseMemoryController
from src.Controllers.LLM import BaseLLMController

class ChatBoxComponent:
    def __init__(self, memory : BaseMemoryController, llm : BaseLLMController, height : int = 600):
        self.memory = memory
        self.llm = llm
        self.height = height
        self.history_container = st.container(height=round(self.height * 0.85))
        self.input_container = st.container(height=round(self.height * 0.15))
        
    def render(self):
        with self.input_container:
            if prompt := st.chat_input("Enter your message"):
                self.memory.add_message("user", prompt)
                response = self.llm.inference("user", prompt, self.memory)
                self.memory.add_message("assistant", response)

        with self.history_container:
            for message in self.memory.get_memory():
                st.chat_message(message["role"]).write(message["content"])


from typing import Callable
from src.Controllers import BaseController
from src.Controllers.LLM import HyperParameter

def hyperparameter_config_asset(target_params_getter: Callable[[], HyperParameter]) -> Callable:
    def hyperparameter(func: Callable) -> Callable:
        def wrapper(label, min_value, max_value, step, value):
            target_params = target_params_getter()
            result = func(label, min_value, max_value, step, value)
            if target_params is not None:
                target_params.set(label, result)
            return result
        return wrapper
    return hyperparameter

@hyperparameter_config_asset(lambda: BaseController.get_state("params"))
def slider(label, min_value, max_value, step, value):
    return st.slider(
        label=label, 
        min_value=min_value, 
        max_value=max_value, 
        step=step, 
        value=value,
    )

@hyperparameter_config_asset(lambda: BaseController.get_state("params"))
def number_inputbox(label, min_value, max_value, step, value):
    return st.number_input(
        label=label,
        min_value=min_value,
        max_value=max_value,
        step=step,
        value=value,
    )

class BaseTabs:
    def __init__(self, tabs_pages : List[Tuple[str, Callable]]):
        self.tab_labels = [label for label, _ in tabs_pages]
        self.callbacks = [callback for _, callback in tabs_pages]
        
    def render(self):
        tabs = st.tabs(self.tab_labels)
        for tab, callback in zip(tabs, self.callbacks):
            with tab:
                callback()