
import streamlit as st
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

st.set_page_config(
    page_title="Tamil Nadu Scheme Assistant",
    page_icon="🏛️"
)

st.title("Tamil Nadu Government Scheme Assistant")

st.write(
    "Ask questions about government schemes, "
    "departments and beneficiaries."
)

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


@st.cache_resource
def get_driver():
    return GraphDatabase.driver(
        uri,
        auth=(username, password)
    )


def get_schemes():
    driver = get_driver()

    query = """
    MATCH (d:Department)-[:OFFERS]->(s:Scheme)
    OPTIONAL MATCH (s)-[:TARGETS]->(b:Beneficiary)
    RETURN s.scheme_name AS scheme,
           s.description AS description,
           d.department_name AS department,
           collect(b.beneficiary_type) AS beneficiaries
    """

    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


question = st.chat_input("Ask your question here...")

if question:
    st.chat_message("user").write(question)

    if "scheme" in question.lower():

        try:
            schemes = get_schemes()

            with st.chat_message("assistant"):

                if schemes:
                    st.write("Schemes found in Knowledge Graph:")

                    for item in schemes:
                        st.subheader(item["scheme"])
                        st.write("Department:", item["department"])
                        st.write("Description:", item["description"])
                        st.write("Beneficiaries:", item["beneficiaries"])
                else:
                    st.warning(
                        "No schemes found in Neo4j."
                    )

        except Exception as e:
            st.error(f"Neo4j connection error: {e}")

    else:
        st.info(
            "Currently, this version supports scheme listing. "
            "Hybrid RAG will be added in the next phase."
        )
