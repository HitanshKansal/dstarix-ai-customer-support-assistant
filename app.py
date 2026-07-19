"""Streamlit chatbot for the DStarix Techno AI Customer Support Assistant."""

import base64
import html
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from knowledge import OFFICIAL_LINKS, get_company_context
from prompts import build_prompt_template


DEFAULT_MODEL = "openai/gpt-oss-20b"
CHAT_HISTORY_FILE = Path("chat_sessions.json")
LOGO_PATH = Path("assets/logo-cropped.png")
WELCOME_MESSAGE = (
    "Hello. I am the DStarix Techno AI Assistant. Ask me about services, "
    "solutions, industries, careers, pricing guidance, or project enquiries."
)


def get_image_data_uri(image_path: Path) -> str:
    """Return a data URI for small local images used in custom HTML."""
    if not image_path.exists():
        return ""

    encoded_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
    mime_type = "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime_type};base64,{encoded_image}"

def apply_customer_ui_styles() -> None:
    """Style the page: branded shell, simple ChatGPT-like messages."""
    st.markdown(
        """
        <style>
            :root {
                --brand-blue: #2563eb;
                --brand-ink: #0f172a;
                --brand-muted: #64748b;
                --panel-line: #e5e7eb;
            }

            #MainMenu,
            footer,
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"],
            .stDeployButton {
                display: none !important;
                visibility: hidden !important;
            }

            header {
                background: transparent !important;
                box-shadow: none !important;
            }

            [data-testid="stToolbar"] {
                visibility: visible !important;
            }

            [data-testid="stSidebarCollapseButton"],
            button[title="Close sidebar"],
            button[aria-label="Close sidebar"] {
                display: inline-flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                pointer-events: auto !important;
            }

            [data-testid="stSidebarCollapsedControl"],
            [data-testid="collapsedControl"],
            button[title="Open sidebar"],
            button[aria-label="Open sidebar"] {
                display: inline-flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                pointer-events: auto !important;
                z-index: 999999 !important;
            }

            .stApp {
                background: #ffffff;
            }

            .block-container {
                padding: 0.75rem 1.5rem 6.25rem;
                max-width: 820px;
            }

            [data-testid="stSidebar"] {
                background: #f7f7f8;
                border-right: 1px solid #ececf1;
            }

            [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
                padding: 0.55rem 0.5rem 1rem;
            }

            [data-testid="stSidebarHeader"] {
                position: absolute;
                top: 0.45rem;
                right: 0.55rem;
                z-index: 30;
                padding: 0 !important;
                min-height: 2rem;
                width: 2rem;
                background: #f7f7f8;
                border-bottom: 0;
            }

            [data-testid="stSidebarHeader"] img,
            [data-testid="stLogo"] img {
                max-height: 22px !important;
                width: auto !important;
                object-fit: contain !important;
            }

            .brand-lockup {
                display: flex;
                align-items: center;
                gap: 0.7rem;
                justify-content: flex-start;
                min-height: 2rem;
                margin: -0.55rem -0.5rem 0.8rem;
                padding: 0.62rem 2.6rem 0.45rem 0.75rem;
                position: sticky;
                top: 0;
                z-index: 20;
                background: #f7f7f8;
            }

            .assistant-mark {
                display: grid;
                place-items: center;
                color: white;
                background: linear-gradient(135deg, #1e40af, #2563eb 52%, #7c3aed);
                box-shadow: 0 14px 30px rgba(37, 99, 235, 0.22);
                font-weight: 800;
            }

            .brand-logo {
                display: block;
                width: 68px;
                height: 22px;
                object-fit: contain;
                object-position: center;
                mix-blend-mode: multiply;
            }

            .assistant-mark {
                position: relative;
                width: 58px;
                height: 58px;
                border-radius: 14px;
                padding: 0.4rem;
                flex: 0 0 auto;
                background: white;
                border: 1px solid rgba(37, 99, 235, 0.10);
                box-shadow: 0 14px 34px rgba(37, 99, 235, 0.16);
            }

            .assistant-mark img {
                width: 100%;
                height: 100%;
                object-fit: contain;
                object-position: center;
            }

            .assistant-mark::after {
                content: "";
                position: absolute;
                right: 5px;
                bottom: 5px;
                width: 14px;
                height: 14px;
                border-radius: 50%;
                background: #22c55e;
                border: 3px solid white;
            }

            .brand-name {
                color: var(--brand-ink);
                font-size: 1rem;
                font-weight: 800;
                line-height: 1;
                letter-spacing: 0.01em;
            }

            .brand-subtitle {
                color: var(--brand-blue);
                font-size: 0.64rem;
                font-weight: 700;
                letter-spacing: 0.28em;
                margin-top: 0.2rem;
            }

            .sidebar-section-title {
                color: #111827;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.02em;
                margin: 1.2rem 0.55rem 0.45rem;
            }

            .sidebar-note {
                margin: 1.35rem 0.55rem 0;
                padding-top: 0.85rem;
                border-top: 1px solid #e5e7eb;
                color: #6b7280;
                font-size: 0.78rem;
                line-height: 1.45;
            }

            .sidebar-note strong {
                color: #111827;
                font-size: 0.82rem;
            }

            .hero-panel {
                position: sticky;
                top: 0.75rem;
                width: 100%;
                box-sizing: border-box;
                z-index: 9999;
                margin-bottom: 1.25rem;
                padding: 1.5rem 1.85rem;
                border: 1px solid rgba(37, 99, 235, 0.10);
                border-radius: 24px;
                background:
                    radial-gradient(circle at 88% 14%, rgba(124, 58, 237, 0.17), transparent 12rem),
                    linear-gradient(135deg, #eef5ff 0%, #ffffff 70%);
                box-shadow: 0 24px 70px rgba(15, 23, 42, 0.08);
                backdrop-filter: blur(14px);
            }

            .hero-scroll-shield {
                display: none;
            }

            .hero-spacer {
                display: none;
            }

            .hero-content {
                display: flex;
                align-items: center;
                gap: 1.15rem;
            }

            .hero-panel .hero-title {
                color: var(--brand-ink);
                font-size: clamp(1.75rem, 4vw, 2.4rem);
                font-weight: 800;
                line-height: 1.1;
                margin: 0;
            }

            .hero-subtitle {
                color: #475569;
                margin-top: 0.35rem;
                font-size: 1rem;
            }

            /* ChatGPT/Codex-like messages: no card box around every message. */
            [data-testid="stChatMessage"] {
                background: transparent !important;
                border: 0 !important;
                box-shadow: none !important;
                padding: 0.35rem 0 !important;
                margin-bottom: 0.85rem !important;
            }

            [data-testid="stChatMessageContent"] {
                background: transparent !important;
                border: 0 !important;
                box-shadow: none !important;
            }

            [data-testid="stChatMessage"] p {
                line-height: 1.7;
            }

            .user-message-row {
                display: flex;
                justify-content: flex-end;
                align-items: flex-start;
                gap: 0.5rem;
                margin: 0.25rem 0 1rem auto;
                width: 100%;
            }

            .user-message-text {
                max-width: min(76%, 680px);
                text-align: right;
                color: #0f172a;
                line-height: 1.7;
                overflow-wrap: anywhere;
            }

            .user-message-avatar {
                display: grid;
                place-items: center;
                width: 2rem;
                height: 2rem;
                flex: 0 0 auto;
                border: 1px solid #cbd5e1;
                border-radius: 0.55rem;
                color: #0f172a;
                background: #ffffff;
                font-family: "Material Symbols Rounded";
                font-size: 1.1rem;
            }

            [data-testid="stChatInput"] {
                max-width: 820px;
                margin: 0 auto;
                border-radius: 18px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
            }

            .privacy-note {
                color: #64748b;
                text-align: center;
                font-size: 0.82rem;
                margin-top: 0.6rem;
            }

            div.stButton > button,
            div.stLinkButton > a {
                border-radius: 8px;
                min-height: 2.25rem;
                font-weight: 550;
            }

            [data-testid="stSidebar"] div.stButton > button {
                justify-content: flex-start !important;
                border: 1px solid transparent;
                background: transparent;
                color: #202123;
                box-shadow: none;
                text-align: left !important;
                padding: 0.42rem 0.62rem;
                width: 100%;
            }

            [data-testid="stSidebar"] div.stButton > button > div,
            [data-testid="stSidebar"] div.stButton > button span {
                justify-content: flex-start !important;
                text-align: left !important;
            }

            [data-testid="stSidebar"] div.stButton > button p {
                width: 100%;
                margin: 0;
                overflow: hidden;
                text-align: left !important;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            [data-testid="stSidebar"] div.stButton > button:hover {
                border-color: transparent;
                background: #ececf1;
                color: #111827;
            }

            [data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
                border-color: transparent;
                background: transparent;
            }

            [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
                color: #111827;
                border-color: transparent;
                background: #e9e9eb;
                box-shadow: none;
            }

            .sidebar-chat-row {
                display: flex;
                align-items: center;
                gap: 0.2rem;
                min-height: 2.45rem;
                margin: 0.22rem 0;
                border-radius: 8px;
            }

            .sidebar-chat-row.active {
                background: #e9e9eb;
            }

            .sidebar-chat-link,
            .sidebar-chat-delete {
                color: #202123 !important;
                text-decoration: none !important;
            }

            .sidebar-chat-link {
                display: flex;
                align-items: center;
                gap: 0.55rem;
                flex: 1 1 auto;
                min-width: 0;
                padding: 0.52rem 0.3rem 0.52rem 0.58rem;
                border-radius: 8px;
            }

            .sidebar-chat-row:not(.active) .sidebar-chat-link:hover {
                background: #ececf1;
            }

            .sidebar-chat-icon,
            .sidebar-chat-delete .material-symbols-rounded {
                font-family: "Material Symbols Rounded";
                font-weight: normal;
                font-style: normal;
                font-size: 1rem;
                line-height: 1;
                letter-spacing: normal;
                text-transform: none;
                display: inline-block;
                white-space: nowrap;
                direction: ltr;
                font-feature-settings: "liga";
                -webkit-font-feature-settings: "liga";
            }

            .sidebar-chat-title {
                display: block;
                min-width: 0;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                font-size: 0.9rem;
            }

            .sidebar-chat-delete {
                display: grid;
                place-items: center;
                flex: 0 0 1.9rem;
                width: 1.9rem;
                height: 1.9rem;
                margin-right: 0.25rem;
                border-radius: 7px;
                opacity: 0;
                transition: background 160ms ease, color 160ms ease, opacity 160ms ease;
            }

            .sidebar-chat-row:hover .sidebar-chat-delete,
            .sidebar-chat-delete:focus {
                opacity: 1;
            }

            .sidebar-chat-delete:hover {
                background: #fee2e2;
                color: #b91c1c !important;
            }

            [data-testid="stSidebar"] [class*="st-key-chat_row_"] {
                margin: 0.22rem 0;
            }

            [data-testid="stSidebar"] [class*="st-key-chat_row_"] div.stButton:first-of-type {
                flex: 1 1 auto;
                min-width: 0;
            }

            [data-testid="stSidebar"] [class*="st-key-delete_chat_"] {
                opacity: 0;
                flex: 0 0 auto;
                transition: opacity 160ms ease;
            }

            [data-testid="stSidebar"] [class*="st-key-chat_row_"]:hover [class*="st-key-delete_chat_"],
            [data-testid="stSidebar"] [class*="st-key-delete_chat_"]:focus-within {
                opacity: 1;
            }

            [data-testid="stSidebar"] [class*="st-key-delete_chat_"] button {
                align-items: center !important;
                justify-content: center !important;
                width: 1.9rem !important;
                min-width: 1.9rem !important;
                height: 1.9rem !important;
                min-height: 1.9rem !important;
                padding: 0 !important;
                border-radius: 7px !important;
            }

            [data-testid="stSidebar"] [class*="st-key-delete_chat_"] button:hover {
                background: #fee2e2 !important;
                color: #b91c1c !important;
            }

            [data-testid="stSidebar"] [class*="st-key-delete_chat_"] button p {
                display: none;
            }

            @media (min-width: 701px) {
                [data-testid="stSidebarHeader"],
                [data-testid="stSidebarCollapseButton"],
                [data-testid="stSidebarCollapsedControl"],
                [data-testid="collapsedControl"],
                button[title="Close sidebar"],
                button[title="Open sidebar"],
                button[title*="sidebar" i],
                button[aria-label="Close sidebar"],
                button[aria-label="Open sidebar"],
                button[aria-label*="sidebar" i] {
                    display: none !important;
                    visibility: hidden !important;
                    opacity: 0 !important;
                    pointer-events: none !important;
                }

                [data-testid="stSidebar"] {
                    min-width: 260px;
                    max-width: 280px;
                    visibility: visible !important;
                    opacity: 1 !important;
                    pointer-events: auto !important;
                }

                .block-container {
                    max-width: 820px;
                }

                .brand-lockup {
                    padding-right: 0.75rem;
                }
            }

            @media (max-width: 700px) {
                .block-container {
                    padding: 0.75rem 1rem 6rem;
                }

                .sidebar-chat-delete {
                    opacity: 0.78;
                }

                [data-testid="stSidebar"] [class*="st-key-delete_chat_"] {
                    opacity: 0.78;
                }

                .hero-panel {
                    position: static;
                    width: auto;
                    padding: 1.2rem;
                }

                .hero-scroll-shield {
                    display: none;
                }

                .hero-spacer {
                    display: none;
                }

                [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
                    padding-left: 0.55rem;
                    padding-right: 0.55rem;
                }

                .hero-content {
                    align-items: flex-start;
                    gap: 0.8rem;
                }

                .assistant-mark {
                    width: 48px;
                    height: 48px;
                }

                .brand-logo {
                    width: 64px;
                    height: 20px;
                }

                .hero-panel .hero-title {
                    font-size: 1.7rem !important;
                    line-height: 1.12 !important;
                }

                .user-message-text {
                    max-width: 82%;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_settings() -> tuple[str, str]:
    """Load safe runtime settings from .env without printing secrets."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model_name = os.getenv("GROQ_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    return api_key, model_name


def current_timestamp() -> str:
    """Return a stable UTC timestamp for saved chats."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_chat_sessions() -> dict[str, dict]:
    """Load previous chat sessions from local storage."""
    if not CHAT_HISTORY_FILE.exists():
        return {}

    try:
        data = json.loads(CHAT_HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    if not isinstance(data, dict):
        return {}
    return data


def save_chat_sessions() -> None:
    """Save chat sessions locally for this project."""
    CHAT_HISTORY_FILE.write_text(
        json.dumps(st.session_state.chat_sessions, indent=2),
        encoding="utf-8",
    )


def make_chat_title(messages: list[dict[str, str]]) -> str:
    """Create a short sidebar title from the first user message."""
    first_user_message = next(
        (message["content"] for message in messages if message["role"] == "user"),
        "",
    ).strip()

    if not first_user_message:
        return "New chat"

    return (
        first_user_message
        if len(first_user_message) <= 36
        else f"{first_user_message[:33]}..."
    )


def create_chat_session() -> None:
    """Create and activate a new chat session."""
    chat_id = uuid.uuid4().hex
    timestamp = current_timestamp()
    messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]

    st.session_state.chat_sessions[chat_id] = {
        "title": "New chat",
        "messages": messages,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    st.session_state.active_chat_id = chat_id
    st.session_state.messages = messages.copy()
    st.session_state.pending_question = None
    save_chat_sessions()


def load_chat_session(chat_id: str) -> None:
    """Switch the UI to a saved chat session."""
    chat = st.session_state.chat_sessions.get(chat_id)
    if not chat:
        return

    st.session_state.active_chat_id = chat_id
    st.session_state.messages = chat.get("messages", []).copy()
    st.session_state.pending_question = None


def delete_chat_session(chat_id: str) -> None:
    """Delete a saved chat and keep the UI on a valid conversation."""
    if chat_id not in st.session_state.chat_sessions:
        return

    was_active_chat = chat_id == st.session_state.get("active_chat_id")
    del st.session_state.chat_sessions[chat_id]

    if not st.session_state.chat_sessions:
        create_chat_session()
        return

    if was_active_chat:
        next_chat_id = get_sorted_chat_sessions()[0][0]
        load_chat_session(next_chat_id)

    st.session_state.pending_question = None
    save_chat_sessions()


def persist_active_chat() -> None:
    """Persist the active chat after messages change."""
    chat_id = st.session_state.get("active_chat_id")
    if not chat_id:
        return

    chat = st.session_state.chat_sessions.setdefault(chat_id, {})
    messages = st.session_state.get("messages", [])

    chat["messages"] = messages
    chat["title"] = make_chat_title(messages)
    chat.setdefault("created_at", current_timestamp())
    chat["updated_at"] = current_timestamp()
    save_chat_sessions()


def reset_chat() -> None:
    """Start a fresh conversation."""
    create_chat_session()


def initialize_chat() -> None:
    """Set up Streamlit session state for the visible conversation."""
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = load_chat_sessions()

    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    if not st.session_state.chat_sessions:
        create_chat_session()
        return

    if "active_chat_id" not in st.session_state:
        latest_chat_id = max(
            st.session_state.chat_sessions,
            key=lambda chat_id: st.session_state.chat_sessions[chat_id].get(
                "updated_at", ""
            ),
        )
        load_chat_session(latest_chat_id)

    if "messages" not in st.session_state:
        load_chat_session(st.session_state.active_chat_id)


def get_sorted_chat_sessions() -> list[tuple[str, dict]]:
    """Return saved chats newest first for sidebar rendering."""
    return sorted(
        st.session_state.chat_sessions.items(),
        key=lambda item: item[1].get("updated_at", ""),
        reverse=True,
    )


def render_saved_chat_row(chat_id: str, title: str, is_active: bool) -> None:
    """Render a responsive saved-chat row without browser navigation."""
    button_type = "primary" if is_active else "secondary"

    with st.container(
        horizontal=True,
        vertical_alignment="center",
        gap="xxsmall",
        key=f"chat_row_{chat_id}",
    ):
        st.button(
            title,
            key=f"saved_chat_{chat_id}",
            icon=":material/history:",
            type=button_type,
            width="stretch",
            on_click=load_chat_session,
            args=(chat_id,),
        )
        st.button(
            "Delete chat",
            key=f"delete_chat_{chat_id}",
            icon=":material/delete:",
            help=f"Delete chat: {title}",
            type="tertiary",
            width=34,
            on_click=delete_chat_session,
            args=(chat_id,),
        )


def format_chat_history(messages: list[dict[str, str]]) -> str:
    """Convert recent Streamlit messages into plain text for the prompt."""
    if not messages:
        return "No previous conversation."

    recent_messages = messages[-8:]
    return "\n".join(
        f"{message['role'].title()}: {message['content']}"
        for message in recent_messages
    )


def build_customer_support_chain(model_name: str):
    """Build the beginner-friendly LangChain flow: prompt -> model -> parser."""
    prompt = build_prompt_template()
    model = ChatGroq(
        model=model_name,
        temperature=0.2,
        max_tokens=700,
    )
    parser = StrOutputParser()
    return prompt | model | parser


def generate_response(question: str, chat_history: str, model_name: str) -> str:
    """Generate an assistant response using verified context and Groq."""
    chain = build_customer_support_chain(model_name)
    return chain.invoke(
        {
            "company_context": get_company_context(),
            "chat_history": chat_history,
            "question": question,
        }
    )


def show_header() -> None:
    """Render the branded header used before."""
    logo_data_uri = get_image_data_uri(LOGO_PATH)
    assistant_brand = (
        f'<img src="{logo_data_uri}" alt="DStarix Techno logo">'
        if logo_data_uri
        else "D"
    )
    st.markdown(
        f"""
        <div class="hero-scroll-shield"></div>
        <div class="hero-panel">
            <div class="hero-content">
                <div class="assistant-mark">{assistant_brand}</div>
                <div>
                    <h1 class="hero-title">DStarix Techno AI Assistant</h1>
                </div>
            </div>
        </div>
        <div class="hero-spacer"></div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Render the desktop brand panel and quick actions."""
    logo_data_uri = get_image_data_uri(LOGO_PATH)
    logo_markup = (
        f'<img class="brand-logo" src="{logo_data_uri}" alt="DStarix Techno logo">'
        if logo_data_uri
        else """
            <div>
                <div class="brand-name">DSTARIX</div>
                <div class="brand-subtitle">TECHNO</div>
            </div>
        """
    )
    with st.sidebar:
        st.markdown(
            f"""
            <div class="brand-lockup">
                {logo_markup}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "New chat",
            icon=":material/add_comment:",
            type="secondary",
            width="stretch",
        ):
            reset_chat()
            st.rerun()

        if st.session_state.chat_sessions:
            st.markdown(
                '<div class="sidebar-section-title">Previous chats</div>',
                unsafe_allow_html=True,
            )

            sorted_chats = get_sorted_chat_sessions()
            for chat_id, chat in sorted_chats[:12]:
                title = chat.get("title") or "New chat"
                render_saved_chat_row(
                    chat_id=chat_id,
                    title=title,
                    is_active=chat_id == st.session_state.active_chat_id,
                )

        quick_questions = globals().get("QUICK_QUESTIONS", {})
        if quick_questions:
            st.markdown(
                '<div class="sidebar-section-title">Quick questions</div>',
                unsafe_allow_html=True,
            )

            for index, (label, question) in enumerate(quick_questions.items()):
                if st.button(
                    label,
                    key=f"quick_question_{index}",
                    icon=":material/chat:",
                    width="stretch",
                ):
                    st.session_state.pending_question = question
                    st.rerun()

        st.markdown(
            """
            <div class="sidebar-note">
                <strong>DStarix Techno AI Assistant</strong><br>
                Your intelligent support partner for DStarix services and enquiries.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_chat_history() -> None:
    """Display previous user and assistant messages."""
    for message in st.session_state.messages:
        if message["role"] == "user":
            render_user_message(message["content"])
        else:
            with st.chat_message("assistant", avatar=":material/support_agent:"):
                st.markdown(message["content"])


def render_user_message(content: str) -> None:
    """Render a user message on the right side of the chat."""
    escaped_content = html.escape(content).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="user-message-row">
            <div class="user-message-text">{escaped_content}</div>
            <div class="user-message-avatar">person</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Run the Streamlit app."""
    if "desktop_sidebar_reset_done" not in st.session_state:
        st.session_state.desktop_sidebar_reset_done = True
        st.set_page_config(
            page_title="DStarix Techno AI Assistant",
            page_icon=":material/support_agent:",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
        st.rerun()

    st.set_page_config(
        page_title="DStarix Techno AI Assistant",
        page_icon=":material/support_agent:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_customer_ui_styles()

    api_key, model_name = load_settings()
    api_key_configured = bool(api_key)

    initialize_chat()
    render_sidebar()
    show_header()
    render_chat_history()

    typed_question = st.chat_input(
        "Ask a question about DStarix Techno",
        submit_mode="disable",
    )
    question = st.session_state.pending_question or typed_question
    st.session_state.pending_question = None

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        persist_active_chat()
        render_user_message(question)

        with st.chat_message("assistant", avatar=":material/support_agent:"):
            if not api_key_configured:
                response = (
                    "The assistant is not available yet because the Groq API key "
                    "has not been configured. Please contact the site owner."
                )
                st.warning(response)
            else:
                try:
                    with st.spinner("Generating response..."):
                        chat_history = format_chat_history(
                            st.session_state.messages[:-1]
                        )
                        response = generate_response(
                            question=question,
                            chat_history=chat_history,
                            model_name=model_name,
                        )
                    st.markdown(response)
                except Exception as exc:
                    response = (
                        "Sorry, I could not generate a response right now. "
                        "Please check your Groq API key, model name, and internet "
                        "connection, then try again."
                    )
                    st.error(response)
                    st.caption(f"Technical detail: {type(exc).__name__}")

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
        persist_active_chat()

    st.markdown(
        '<div class="privacy-note">AI responses may need verification for important business decisions.</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
