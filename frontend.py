import os
import streamlit.components.v1 as components

_RELEASE = True

def get_my_component_fuc(name):
    if not _RELEASE:
        return components.declare_component(
            name ,
            url="http://localhost:5173/src/" + name  + "/"
        )

    return components.declare_component(
        name,
        os.path.join(os.path.dirname(str(os.path.abspath(__file__))), "src/", name)
    )

def my_component(name, data, key=None):
    _component_func = get_my_component_fuc(name)
    component_value = _component_func(data=data, key=key, default=0)
    return component_value