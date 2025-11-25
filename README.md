# 🚀 Releasy - AI Powered Update Notes Generator

**Releasy** is a modern desktop application designed to help developers create release notes quickly, professionally, and effortlessly. It takes raw developer notes and transforms them into a polished, user-friendly format using Artificial Intelligence (AI).

![Releasy Screenshot](https://cdn.discordapp.com/attachments/780456382431756308/1442988140313972857/image.png?ex=69276eee&is=69261d6e&hm=b2c7ff0df788761f90609597a1e8b4dfcc41e9d02df75a0b56d56e88ec8e4067)

## ✨ Features

* **🤖 AI-Powered Generation:** Converts your notes into a professional tone using Google Gemini or compatible AI models.
* **🎨 Modern & Sleek UI:** Dark theme, custom title bar, smooth transitions, and a clean visual style.
* **⚙️ Fully Customizable:**
  * **API Key Management:** Use your own API key (OpenRouter/OpenAI compatible).
  * **System Prompt Control:** Customize the AI's tone and style directly from the settings menu.
  * **Model Selection:** Choose any AI model you prefer.
* **📝 User-Friendly Tools:**
  * Character counter
  * One-click copy button
  * Clear text button
  * Draggable custom window structure

## 🛠️ Installation

To run this application, **Python** must be installed on your system.

1. **Install Dependencies**
   Open your terminal or command prompt and install the required library:
   ```
   pip install openai
   ```
   *(Tkinter comes built-in with Python, so no extra installation is needed.)*

2. **Download the Application**
   Save the `Releasy.py` file to your computer.

## 🚀 Usage

1. **Run the Application**
   ```
   python Releasy.py
   ```

2. **Configure Settings (First Launch)**
   * Click the **Settings (⚙️)** icon in the top-left corner.
   * **API Key:** Enter your OpenRouter or OpenAI API key.
   * **Base URL:** Default is set to OpenRouter, but you can change it.
   * **System Prompt:** Adjust how the AI writes the notes.
   * Click **Save Settings** to apply changes.

3. **Generate Release Notes**
   * **Version Number:** Enter the version (e.g., v1.0.2).
   * **Developer Notes:** Write your changes as bullet points or raw text.
   * Press **✨ Generate** to create your release notes.

4. **Output**
   * Your professionally generated notes will appear on the right (or bottom).
   * Use the **📋 Copy** button to copy them to your clipboard.

## 📁 Configuration (config.json)

Releasy saves your settings in a `config.json` file.
This file is generated automatically on the first run.

```
{
    "api_key": "sk-...",
    "base_url": "https://openrouter.ai/api/v1",
    "model": "google/gemini-2.0-flash-exp:free",
    "system_prompt": "..."
}
```

## ⚠️ Troubleshooting

* **401 Authentication Error:** Your API key is invalid. Check the settings.
* **429 Rate Limit:** Free rate limits may be reached. Make sure you are using your own API key.

---

*Made with 💜 for alwiss*
