from langgraph.graph import StateGraph, START, END
from app.schemas.core_schemas import GraphState
from app.utils.core_utils import checkpointer_conn
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from app.utils.core_utils import checkpointer_conn

from app.nodes import (
    extract_pdf_node,
    create_invoice_node,
    make_invoice_completed_node,
    parse_invoice_node,
    pop_next_file_node,
    revert_to_sender_node,
    review_invoice_node,
)

def route_review_decision(state: GraphState) -> str:
    """Branches workflow based on review decision."""
    if state.review_approved:
        return "save_invoice"
    return "revert_to_sender"

builder = StateGraph(GraphState)
# Nodes
builder.add_node("create_invoice", create_invoice_node)
builder.add_node("pop_next_file", pop_next_file_node)
builder.add_node("extract_pdf", extract_pdf_node)
builder.add_node("parse_invoice", parse_invoice_node)
builder.add_node("review", review_invoice_node)
builder.add_node("revert_to_sender", revert_to_sender_node)
builder.add_node("make_invoice_completed", make_invoice_completed_node)

# Core Flow
builder.add_edge(START, "create_invoice")
builder.add_edge("create_invoice", "extract_pdf")
builder.add_edge("extract_pdf", "parse_invoice")
builder.add_edge("parse_invoice", "review")

# review decision - conditional edge
builder.add_conditional_edges(
    "review",
    route_review_decision,
    {
        "save_invoice": "make_invoice_completed",
        "revert_to_sender": "revert_to_sender",
    }
)

builder.add_edge("make_invoice_completed", END)
builder.add_edge("revert_to_sender", END)

conn = checkpointer_conn()
checkpointer = SqliteSaver(conn)
checkpointer.setup()
invoice_graph = builder.compile(checkpointer=checkpointer)