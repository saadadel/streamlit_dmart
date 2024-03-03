import asyncio
import streamlit as st
import yaml

from utils.dmart import DMart
from utils.enums import ResourceType


def main():
    import streamlit as st
    import streamlit_authenticator as stauth

    st.write("# Welcome to Streamlit! 👋")

    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )
    name, authentication_status, username = authenticator.login()

    dmart_instance_print = st.text(f"IS DMART INSTANCE EXIST? {'dmart_instance' in st.session_state}")
    if authentication_status:
        authenticator.logout("Logout", "main")
        st.write(f"Welcome *{name}*, your username is *{username}*")

        dmart = DMart()
        # TODO: replace the static password with the input from the form
        asyncio.run(dmart.login(username, "Password1234"))
        if "dmart_instance" not in st.session_state:
            st.session_state["dmart_instance"] = dmart

        # def get_dmart_instance():
        if "dmart_instance" in st.session_state:
            st.text(f"DMART INSTANCE ID: {id(st.session_state['dmart_instance'])}")

    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")

    dmart_instance_print.text(f"IS DMART INSTANCE EXIST? {'dmart_instance' in st.session_state}")
    if "dmart_instance" in st.session_state:
        data_load_state = st.text('Loading data...')
        data = asyncio.run(
            st.session_state["dmart_instance"].query_data_asset(
                space_name="oodi",
                subpath="my_assets",
                shortname="vouchers",
                data_asset_type="csv",
                query_string="SELECT * FROM 'vouchers_csv'",
                resource_type=ResourceType.content,
            )
        )
        data_load_state.text('Loading data...done!')
        
        st.write(data)
        
    


page_names_to_funcs = {"Main": main}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
