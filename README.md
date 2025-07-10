# 🚀 PyQt Jupiter-Style Editor & Integrated Design Tool

> A standalone desktop application that brings the interactivity of Jupyter Notebooks together with a powerful built‑in design canvas!

---

## 🔥 Overview

**PyQt Jupyter-Style Editor** empowers you to:

* Write, execute, and document Python code in cells (code & markdown) 🐍
* Enjoy real-time smart autocompletion with Jedi integration ⚡
* Render beautifully formatted Markdown with live previews 📝
* Visualize DataFrames and Matplotlib plots inline 📊
* Save/load sessions as JSON or native `.ipynb` notebooks 💾
* Export your entire notebook to PDF (print‑ready) 📄

**Design Canvas Tool** is embedded directly in the editor toolbar. Instantly create and insert custom graphics: flowcharts, diagrams, callouts, shapes, arrows, and more. All graphics are exported as SVG/HTML snippets into your notebook for seamless documentation.

---

## ✨ Key Features

| Feature                     | Description                                                                             |
| --------------------------- | --------------------------------------------------------------------------------------- |
| **Code & Markdown Cells**   | Structured cells for code execution and Markdown documentation.                         |
| **Inline Output**           | Auto-capture stdout, DataFrames, plots, and display under each cell.                    |
| **Smart Autocomplete**      | Jedi-powered suggestions triggered on `.` or `Ctrl+Space`.                              |
| **Session Management**      | Save and load sessions (`.json` or `.ipynb`) preserving cell types and order.           |
| **PDF Export**              | One-click PDF export of your entire notebook via Qt's `printToPdf`.                     |
| **Design Tool Integration** | Launch a full-featured canvas (`Design` button) to draw shapes, arrows, text, and more. |
| **Graphic Insertion**       | Apply your design to insert as an SVG/HTML Markdown cell in the notebook.               |
| **Crop & Transparent BG**   | Define crop areas and toggle background transparency before export.                     |
| **Flowchart & Misc Shapes** | Parallelogram, trapezoid, cylinder, cloud, lightning bolt, heart, and other built‑ins.  |
| **Arrows & Callouts**       | Single/double arrows, speech/thought bubbles with customizable styling.                 |
| **Text Tool**               | Add and edit text objects with font size, family, and color controls.                   |

---

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/LifelessA/jupiter-like-editor-with-VScode-feature.git
   cd jupiter-like-editor-with-VScode-feature
   ```

2. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### `requirements.txt`

```
PyQt6
PyQt6-WebEngine
matplotlib
pandas
jedi
```

---

## ▶️ run server version
```bash
python server.py
```

## ▶️ Quick Start

```bash
python main.py
```

This opens the editor. Use the toolbar:

* `+ Code` / `+ Markdown`: Add new cells
* `▶ Run All`: Execute all cells
* `Design`: Open the integrated design canvas
* **Cell Controls**: Run, Stop, Delete, Move Up/Down

---

## 🖼️ Screenshots

**Main Editor Interface**

![image](https://github.com/user-attachments/assets/d8e1176d-e6f4-4f82-8fc9-f35aec147ff6)


**Autocomplete Suggestions**

![image](https://github.com/user-attachments/assets/208ba602-d9ff-4eba-aaef-4994e5d2f05d)


**Design Canvas Tool**

![image](https://github.com/user-attachments/assets/22504d76-78cc-4100-83b6-d8d5181b41c4)

![image](https://github.com/user-attachments/assets/741eda2c-e933-4709-af9e-b4e263e631a0)



---

## 📐 Architecture

### Backend (PythonBridge)

* Executes user code securely via `exec`/`eval`.
* Captures stdout, exceptions, Matplotlib figures, and Pandas DataFrames.
* Maintains a persistent `locals` dict for state across cells.
* Exposes slots: `run_code`, `get_completions`, and `open_design_tool`.

### Frontend (HTML + JavaScript)

* **CodeMirror** for code/markdown editing with custom theme.
* **Marked.js** for Markdown rendering.
* **QWebChannel** bridges JS ↔ Python.
* Dynamic cell management: add, run, stop, delete, reorder.

---

## 🎨 Design Canvas Details

* **Tools Panel**: Select, Crop, Text, Delete.
* **Basic Shapes**: Rectangle (rounded), Circle/Oval, Triangle, Diamond, Pentagon, Hexagon, Octagon, Star, Cross, Ring.
* **Flowchart & Misc**: Parallelogram, Trapezoid, Cylinder, Document, Cloud, Heart, Moon, Lightning Bolt.
* **Arrows & Callouts**: Arrow, Double Arrow, Speech Bubble, Thought Bubble.
* **Settings**:

  * Fill color, stroke color, stroke width
  * Font size & family for text
  * Canvas background color / transparent toggle
* **Canvas Interaction**:

  * Mouse-driven drawing, dragging, resizing via handles
  * Crop area selection for focused export
* **Export**:

  * Generate clean SVG/HTML snippet
  * Automatically insert into a new Markdown cell

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feat/my-feature`
3. Commit changes: `git commit -m 'Add my feature'`
4. Push branch: `git push origin feat/my-feature`
5. Open a Pull Request

---

## 📄 License

Licensed under the **MIT License**.

> Crafted with ❤️ through Vibe Coding by Aniket Raj — built in flow, refined with purpose.
