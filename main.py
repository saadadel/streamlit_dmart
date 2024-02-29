import asyncio
import streamlit as st

from utils.dmart import DMart
from utils.enums import ResourceType


st.title("Streamlit serving Dmart data")

dmart = DMart()


async def dmart_login():
    await dmart.login("dmart", "Password1234")


async def get_data_asset():
    return await dmart.query_data_asset(
            space_name="oodi",
            subpath="my_assets",
            shortname="vouchers",
            data_asset_type="csv",
            query_string="SELECT * FROM 'vouchers_csv'",
            resource_type=ResourceType.content
    )

data_load_state = st.text('Loading data...')

asyncio.run(dmart_login())

res = asyncio.run(get_data_asset())

data_load_state.text('Loading data...done!')



st.write(res)