# jupiter-like-editor-with-VScode-feature


* Feature explanations
* Emphasis on **crafted through Vibe Coding**
* Screenshots for both the **GUI interface** and the **autocomplete suggestions popup**

---

### ✅ Before using:

Make sure the following image files are placed in a folder named `screenshots/` in your project directory:

| Image Name              | Description                   |
| ----------------------- | ----------------------------- |
| `gui-interface.png`     | Full view of your editor GUI  |
| `suggestions-popup.png` | Autocomplete dropdown feature |

---

### ✅ Full `README.md` content:

````markdown
# 🚀 PyQt Jupyter-Style Editor

> Experience the power of a Jupyter-like notebook in a standalone desktop application!

---

## 🔥 Overview

> ## Crafted through Vibe Coding – built in the flow, with love for interactive tools and Python power!

The ## PyQt Jupyter-Style Editor brings the dynamic feel of Jupyter Notebooks into a sleek and customizable desktop app:

- Powered by ### PyQt6 & ###QtWebEngine for smooth GUI rendering
- Enhanced with ### CodeMirror and ### Marked.js for rich code + markdown editing
- Integrated with ### Jedi to enable smart, real-time Python autocompletion
- Designed for ### data science, ### prototyping, and ###teaching workflows

---

## ✨ Key Features

| Feature                   | Description                                                                                 |
|---------------------------|---------------------------------------------------------------------------------------------|
| Code Cells                | Write and execute Python code in structured cells.                                          |
| Markdown Cells            | Document your work beautifully using Markdown with live previews.                           |
| Inline Output             | Instantly visualize DataFrames and plots beneath each cell.                                 |
| Session Management        | Save/load your work in JSON format for portability.                                         |
| PDF Export                | Export entire notebooks to professional-looking PDFs.                                       |
| Autocompletion            | Context-aware suggestions using Jedi — activated with `.` or Ctrl+Space.                    |
| Suggestion Dropdown       | Elegant autocompletion popup for quick keyword or object access (see preview below).        |
| Keyboard Shortcuts        | Familiar keybindings like Shift+Enter, Ctrl+/, and more.                                    |
| Dark Theming              | Aesthetic dark UI with CSS-based styling.                                                   |

---

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/LifelessA/jupiter-like-editor-with-VScode-feature
   cd jupiter-like-editor-with-VScode-feature
````

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate      # On macOS/Linux
   venv\Scripts\activate         # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

> Sample `requirements.txt`:
>
> ```
> PyQt6
> PyQt6-WebEngine
> matplotlib
> pandas
> jedi
> ```

---

## ▶️ Quick Start

To launch the editor:

```bash
python main.py
```

### 🧪 How to Use:

* **Add Cells**: Click **+ Code** or **+ Markdown** to add content.
* **Run Cells**: Click **Run** or press **Shift+Enter**.
* **Reorder/Remove**: Use **↑ ↓ Delete** buttons to modify layout.
* **Save/Load Session**: Use menu to store or reopen `.json` sessions.
* **Export as PDF**: One-click export to `.pdf` using Qt's `printToPdf`.

---

## 📐 Architecture & How It Works

### 🧠 Backend (PythonBridge)

* Executes Python code securely via `exec` and `eval`
* Captures:

  * Standard output
  * Exceptions
  * Matplotlib visualizations
  * Pandas DataFrames
* Maintains variables using `self.locals`
* Handles cell serialization and JSON save/load

### 🌐 Frontend (HTML + JavaScript)

* Uses **CodeMirror** for editing
* Markdown rendered live via **Marked.js**
* Communicates via `QWebChannel`
* Custom CSS and JavaScript control layout and logic

---

## 🎨 Customization & Theming

Update your UI through CSS variables in the HTML:

```css
:root {
  --bg-color: #1e1e1e;
  --cell-bg: #2d2d2d;
  --border-color: #3a3a3a;
  --toolbar-bg: #252526;
}
```

You can also:

* Modify font families and sizes
* Tweak CodeMirror settings
* Add new keyboard shortcuts or UI widgets

---

## 🖼️ UI Previews

### 🧪 Main GUI Interface

> Sleek, dark-themed PyQt interface replicating Jupyter functionality:

![image](https://github.com/user-attachments/assets/54b57519-51a0-45d3-bb06-07dc551f3876)


---

### 💡 Autocomplete Suggestion Feature

> Powered by Jedi — get intelligent keyword completions and Python hints:

![Autocomplete Suggestions]![image](https://github.com/user-attachments/assets/6b48c16f-100f-4aab-8038-8e4c7a7ab96c)


---

## 🤝 Contributing

Your contributions are welcome!
To contribute:

1. Fork the project
2. Create your feature branch: `git checkout -b feat/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push: `git push origin feat/new-feature`
5. Submit a Pull Request

---

## 📄 License

Licensed under the **MIT License**.
See [LICENSE](LICENSE) for full license text.

---

> 💡 Crafted with ❤️ through **Vibe Coding** by Aniket Raj
> *Built in flow, refined with purpose.*

```

---


