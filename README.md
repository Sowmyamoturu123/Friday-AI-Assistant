# 🤖 Friday AI Assistant

> A real-time AI voice personal assistant built with Python, LiveKit, and Google Gemini.

Friday is an AI-powered voice assistant designed to interact naturally with users, answer questions, search the web, provide weather information, and send emails through Gmail.

## ✨ Features

- 🎙️ **Real-time voice conversation**
- 🧠 **Google Gemini Realtime AI**
- 🌐 **Web search using DuckDuckGo**
- 🌤️ **Weather information**
- 📧 **Gmail email sending**
- 🔊 **LiveKit real-time audio**
- 🚫 **Noise cancellation**
- 🛠️ **Modular tool-based architecture**
- 🔐 **Environment-variable based API credentials**

## 🏗️ Architecture

```text
User
  │
  ▼
LiveKit Console
  │
  ▼
Friday AI Agent
  │
  ├── Google Gemini Realtime AI
  │
  ├── Weather Tool
  │
  ├── Web Search Tool
  │
  └── Gmail Email Tool