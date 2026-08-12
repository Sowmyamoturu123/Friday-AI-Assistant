from memory import (
    remember,
    recall,
    get_all_memories,
    load_memory,
)

import logging
import os
import smtplib
from typing import Optional

import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from langchain_community.tools import DuckDuckGoSearchRun
from livekit.agents import function_tool, RunContext


@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str
) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3",
            timeout=10
        )

        if response.status_code == 200:
            logging.info(
                f"Weather for {city}: {response.text.strip()}"
            )
            return response.text.strip()

        logging.error(
            f"Failed to get weather for {city}: "
            f"{response.status_code}"
        )

        return f"Could not retrieve weather for {city}."

    except Exception as e:
        logging.error(
            f"Error retrieving weather for {city}: {e}"
        )

        return (
            f"An error occurred while retrieving "
            f"weather for {city}."
        )


@function_tool()
async def search_web(
    context: RunContext,  # type: ignore
    query: str
) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        search = DuckDuckGoSearchRun()
        results = search.invoke(query)

        logging.info(
            f"Search results for '{query}': {results}"
        )

        return str(results)

    except Exception as e:
        logging.error(
            f"Error searching the web for '{query}': {e}"
        )

        return (
            f"An error occurred while searching the web "
            f"for '{query}': {e}"
        )


@function_tool()
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
) -> str:
    """
    Send an email through Gmail.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            logging.error(
                "Gmail credentials not found in environment variables"
            )

            return (
                "Email sending failed: "
                "Gmail credentials not configured."
            )

        # Create email
        msg = MIMEMultipart()

        msg["From"] = gmail_user
        msg["To"] = to_email
        msg["Subject"] = subject

        # Add CC if provided
        recipients = [to_email]

        if cc_email:
            msg["Cc"] = cc_email
            recipients.append(cc_email)

        # Add message body
        msg.attach(
            MIMEText(message, "plain")
        )

        # Connect to Gmail SMTP server
        server = smtplib.SMTP(
            smtp_server,
            smtp_port
        )

        server.starttls()

        # Login using Gmail App Password
        server.login(
            gmail_user,
            gmail_password
        )

        # Send email
        text = msg.as_string()

        server.sendmail(
            gmail_user,
            recipients,
            text
        )

        server.quit()

        logging.info(
            f"Email sent successfully to {to_email}"
        )

        return (
            f"Email sent successfully to {to_email}"
        )

    except smtplib.SMTPAuthenticationError:
        logging.error(
            "Gmail authentication failed"
        )

        return (
            "Email sending failed: Authentication error. "
            "Please check your Gmail App Password."
        )

    except smtplib.SMTPException as e:
        logging.error(
            f"SMTP error occurred: {e}"
        )

        return (
            f"Email sending failed: SMTP error - {str(e)}"
        )

    except Exception as e:
        logging.error(
            f"Error sending email: {e}"
        )

        return (
            f"An error occurred while sending email: {str(e)}"
        )


@function_tool()
async def remember_information(
    context: RunContext,  # type: ignore
    memory: str
) -> str:
    """
    Save an important piece of information provided by the user.

    Use this when the user explicitly asks Friday to remember something.

    Args:
        memory: The complete information to remember.
    """
    try:
        # Load existing memories
        memory_data = load_memory()

        # Create a unique memory key
        key = f"memory_{len(memory_data) + 1}"

        # Save the complete natural-language memory
        result = remember(
            key,
            memory
        )

        logging.info(
            f"Memory saved: {key} = {memory}"
        )

        return result

    except Exception as e:
        logging.error(
            f"Error saving memory: {e}"
        )

        return (
            f"I couldn't save that information: {e}"
        )


@function_tool()
async def recall_information(
    context: RunContext,  # type: ignore
    key: str
) -> str:
    """
    Recall information from Friday's persistent memory.

    Args:
        key: The topic or information the user wants to find.
    """
    try:
        memory_data = load_memory()

        if not memory_data:
            return (
                "I don't have any memories stored yet."
            )

        search_text = (
            key.lower()
            .replace("_", " ")
        )

        matches = []

        for stored_key, value in memory_data.items():

            stored_key_text = (
                stored_key
                .lower()
                .replace("_", " ")
            )

            value_text = str(value).lower()

            if (
                search_text in stored_key_text
                or search_text in value_text
            ):
                matches.append(str(value))

        if matches:
            return " | ".join(matches)

        return (
            f"I don't have any information stored "
            f"about {key}."
        )

    except Exception as e:
        logging.error(
            f"Error recalling memory: {e}"
        )

        return (
            f"I couldn't retrieve that information: {e}"
        )


@function_tool()
async def list_memories(
    context: RunContext,  # type: ignore
) -> str:
    """
    Retrieve all information currently stored
    in Friday's persistent memory.
    """
    try:
        result = get_all_memories()

        logging.info(
            "Retrieved all stored memories"
        )

        return result

    except Exception as e:
        logging.error(
            f"Error retrieving memories: {e}"
        )

        return (
            f"I couldn't retrieve your memories: {e}"
        )