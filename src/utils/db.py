import streamlit as st
from src.screener.engine import ScreenerEngine


@st.cache_data(ttl=600)
def get_companies():
    engine = ScreenerEngine()
    return engine.apply_filters()


@st.cache_data(ttl=600)
def get_company(company_id):
    df = get_companies()
    return df[df["company_id"] == company_id]


@st.cache_data(ttl=600)
def get_ratios(company_id=None, year=None):
    df = get_companies()

    if company_id:
        df = df[df["company_id"] == company_id]

    return df


@st.cache_data(ttl=600)
def get_sectors():
    df = get_companies()
    return sorted(df["broad_sector"].dropna().unique())


@st.cache_data(ttl=600)
def get_peers(group_name=None):
    df = get_companies()

    if (
        group_name is not None
        and "peer_group_name" in df.columns
    ):
        return df[df["peer_group_name"] == group_name]

    return df


@st.cache_data(ttl=600)
def get_valuation(company_id=None):
    df = get_companies()

    if company_id:
        df = df[df["company_id"] == company_id]

    return df


@st.cache_data(ttl=600)
def get_pl(company_id=None):
    return get_company(company_id) if company_id else get_companies()


@st.cache_data(ttl=600)
def get_bs(company_id=None):
    return get_company(company_id) if company_id else get_companies()


@st.cache_data(ttl=600)
def get_cf(company_id=None):
    return get_company(company_id) if company_id else get_companies()