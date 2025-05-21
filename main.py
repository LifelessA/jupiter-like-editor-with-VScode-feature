import sys
import os
try:
    import json
    import base64
    import io
    from html import escape
    from contextlib import redirect_stdout
    import ast

    from PyQt6.QtCore import QObject, pyqtSlot
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                                QMenu, QFileDialog, QMessageBox)
    from PyQt6.QtGui import QAction
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebChannel import QWebChannel
    import matplotlib.pyplot as plt
    import pandas as pd
    import jedi
except Exception:
    os.system('pip install PyQt6 PyQt6-WebEngine matplotlib pandas jedi')
    import json
    import base64
    import io
    from html import escape
    from contextlib import redirect_stdout
    import ast

    from PyQt6.QtCore import QObject, pyqtSlot
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                                QMenu, QFileDialog, QMessageBox)
    from PyQt6.QtGui import QAction
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebChannel import QWebChannel
    import matplotlib.pyplot as plt
    import pandas as pd
    import jedi

# Configure matplotlib
plt.switch_backend('agg')

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PyQt Jupyter Editor</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/theme/material-darker.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/addon/hint/show-hint.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/mode/markdown/markdown.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/addon/comment/comment.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/addon/edit/matchbrackets.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/addon/edit/closebrackets.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/addon/selection/active-line.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/addon/hint/show-hint.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <style>
        :root {
            --bg-color: #1e1e1e;
            --cell-bg: #2d2d2d;
            --border-color: #3a3a3a;
            --toolbar-bg: #252526;
        }
        body {
            margin: 0;
            background: var(--bg-color);
            color: #d4d4d4;
            font-family: 'Segoe UI', sans-serif;
        }
        #toolbar {
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 8px;
            background: var(--toolbar-bg);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            gap: 8px;
        }
        #cells { padding: 16px; }
        .cell {
            margin: 12px 0;
            background: var(--cell-bg);
            border-radius: 6px;
            border: 1px solid var(--border-color);
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        .controls {
            padding: 6px;
            background: #333;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            gap: 6px;
            border-radius: 6px 6px 0 0;
        }
        .controls button {
            background: #404040;
            border: 1px solid #4d4d4d;
            color: #d4d4d4;
            padding: 4px 12px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .controls button:hover {
            background: #2a2d2e;
        }
        .CodeMirror {
            font-family: 'Fira Code', monospace;
            font-size: 14px;
            background: #1e1e1e;
            color: #d4d4d4;
            height: auto;
            padding: 8px 0;
        }
        .output {
            padding: 12px;
            background: #1e1e1e;
            border-top: 1px solid var(--border-color);
            font-family: 'Consolas', monospace;
            white-space: pre-wrap;
            line-height: 1.5;
        }
        .error { color: #ff5555; background: #2d1e1e; padding: 8px; border-radius: 4px; }
        @media print {
            .cell {
                page-break-inside: avoid;
            }
            .controls {
                display: none;
            }
        }
        .CodeMirror-hints {
            background: #2d2d2d;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        }
        .CodeMirror-hint {
            color: #d4d4d4;
            padding: 4px 8px;
            cursor: pointer;
        }
        .CodeMirror-hint-active {
            background: #3a3a3a;
            color: #ffffff;
        }
    </style>
</head>
<body>
    <div id="toolbar">
        <button onclick="addCell('code')">+ Code</button>
        <button onclick="addCell('markdown')">+ Markdown</button>
        <button onclick="runAllCells()" style="margin-left: auto">▶ Run All</button>
    </div>
    <div id="cells"></div>
    <script>
        let python;
        new QWebChannel(qt.webChannelTransport, channel => {
            python = channel.objects.python;
            addCell('code');
        });

        const editors = {};

        function pythonHint(editor, options) {
            return new Promise((resolve) => {
                const cursor = editor.getCursor();
                const token = editor.getTokenAt(cursor);
                let from, to;
                if (token.type === "variable" || token.type === "property") {
                    from = CodeMirror.Pos(cursor.line, token.start);
                    to = cursor;
                } else {
                    from = cursor;
                    to = cursor;
                }
                const code = editor.getValue();
                python.get_completions(code, cursor.line, cursor.ch, (completions) => {
                    resolve({
                        list: completions,
                        from: from,
                        to: to
                    });
                });
            });
        }

        function addCell(type = 'code') {
            const cellId = 'cell_' + Math.random().toString(36).slice(2, 11);
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.id = cellId;
            cell.dataset.type = type;
            cell.innerHTML = `
                <div class="controls">
                    <button onclick="runCell('${cellId}')">Run</button>
                    ${type === 'code' ? `<button onclick="stopCell('${cellId}')">Stop</button>` : ''}
                    <button onclick="deleteCell('${cellId}')">Delete</button>
                    <button onclick="moveCell('${cellId}', 'up')">↑</button>
                    <button onclick="moveCell('${cellId}', 'down')">↓</button>
                </div>
                <textarea id="code_${cellId}"></textarea>
                <div id="output_${cellId}" class="output"></div>
            `;
            document.getElementById('cells').appendChild(cell);

            const editor = CodeMirror.fromTextArea(document.getElementById(`code_${cellId}`), {
                mode: type === 'code' ? 'python' : 'markdown',
                theme: 'material-darker',
                lineNumbers: true,
                matchBrackets: true,
                autoCloseBrackets: true,
                extraKeys: {
                    "Ctrl-Space": type === 'code' ? "autocomplete" : null,
                    "Ctrl-/": "toggleComment",
                    "Alt-Up": "addCursorToPrevLine",
                    "Alt-Down": "addCursorToNextLine",
                    "Shift-Enter": "newlineAndIndent",
                    "Tab": function(cm) {
                        if (cm.state.completionActive) {
                            const selected = cm.state.completionActive.data.list[cm.state.completionActive.widget.selectedHint];
                            cm.replaceSelection(selected);
                            cm.state.completionActive.close();
                        } else if (cm.somethingSelected()) {
                            cm.execCommand("indentMore");
                        } else {
                            cm.execCommand("insertTab");
                        }
                    }
                },
                hintOptions: type === 'code' ? { hint: pythonHint, completeSingle: false } : {}
            });
            editors[cellId] = editor;

            if (type === 'code') {
                let timeout;
                editor.on('keyup', (cm, event) => {
                    if (event.key === '.') {
                        CodeMirror.commands.autocomplete(cm);
                    } else if (/[a-zA-Z0-9_]/.test(event.key)) {
                        clearTimeout(timeout);
                        timeout = setTimeout(() => {
                            const cursor = cm.getCursor();
                            const line = cm.getLine(cursor.line);
                            const charBefore = cursor.ch > 0 ? line[cursor.ch - 1] : null;
                            if (charBefore && /[a-zA-Z0-9_]/.test(charBefore)) {
                                CodeMirror.commands.autocomplete(cm);
                            }
                        }, 300);
                    }
                });
            } else if (type === 'markdown') {
                let timeout;
                editor.on('change', () => {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => {
                        document.getElementById(`output_${cellId}`).innerHTML =
                            marked.parse(editor.getValue());
                    }, 500);
                });
            }
        }

        function runCell(cellId) {
            const cell = document.getElementById(cellId);
            if (cell.dataset.type === 'code') {
                python.run_code(cellId, editors[cellId].getValue());
            } else {
                document.getElementById(`output_${cellId}`).innerHTML =
                    marked.parse(editors[cellId].getValue());
            }
        }

        function stopCell(cellId) {
            document.getElementById(`output_${cellId}`).innerHTML =
                '<div class="error">Execution interrupted by user.</div>';
        }

        function deleteCell(cellId) {
            document.getElementById(cellId).remove();
            delete editors[cellId];
        }

        function moveCell(cellId, direction) {
            const cell = document.getElementById(cellId);
            const parent = cell.parentNode;
            if (direction === 'up' && cell.previousElementSibling) {
                parent.insertBefore(cell, cell.previousElementSibling);
            } else if (direction === 'down' && cell.nextElementSibling) {
                parent.insertBefore(cell.nextElementSibling, cell);
            }
        }

        function runAllCells() {
            Object.keys(editors).forEach(id => runCell(id));
        }

        function clearCells() {
            document.getElementById('cells').innerHTML = '';
            for (let id in editors) {
                delete editors[id];
            }
        }
    </script>
</body>
</html>
"""

class PythonBridge(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.locals = {}

    @pyqtSlot(str, str)
    def run_code(self, cell_id, code):
        result_html = self.execute(code)
        js = (
            f"document.getElementById('output_{cell_id}').innerHTML = "
            f"{json.dumps(result_html)};"
        )
        self.view.page().runJavaScript(js)

    @pyqtSlot(str, int, int, result=list)
    def get_completions(self, code, line, column):
        try:
            script = jedi.Script(code)
            completions = script.complete(line + 1, column)
            return [c.name for c in completions]
        except ImportError:
            print("Jedi not installed. Completion not available.")
            return []
        except Exception as e:
            print(f"Completion error: {e}")
            return []

    def execute(self, code):
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                tree = ast.parse(code)
                if tree.body and isinstance(tree.body[-1], ast.Expr):
                    if len(tree.body) > 1:
                        exec_code = compile(ast.Module(tree.body[:-1], type_ignores=[]), '<string>', 'exec')
                        exec(exec_code, {'plt': plt, 'pd': pd}, self.locals)
                    eval_code = compile(ast.Expression(tree.body[-1].value), '<string>', 'eval')
                    result = eval(eval_code, {'plt': plt, 'pd': pd}, self.locals)
                    if isinstance(result, pd.DataFrame):
                        buf.write(result.to_html())
                    elif result is not None:
                        buf.write(str(result))
                else:
                    exec(code, {'plt': plt, 'pd': pd}, self.locals)
                fig = plt.gcf()
                if fig.axes:
                    img_buf = io.BytesIO()
                    fig.savefig(img_buf, format='png', bbox_inches='tight')
                    img_buf.seek(0)
                    plt.close(fig)
                    img_html = base64.b64encode(img_buf.read()).decode()
                    buf.write(f'<img src="data:image/png;base64,{img_html}"><br>')
            except Exception:
                import traceback
                buf.truncate(0)
                buf.seek(0)
                tb = traceback.format_exc()
                buf.write(f'<div class="error">{escape(tb)}</div>')
        return buf.getvalue()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My QtEditor")
        self.resize(1200, 800)
        self.setStyleSheet("""
            QMainWindow { background: #252526; }
            QMenuBar { background: #333; }
            QMenuBar::item { color: #d4d4d4; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.view = QWebEngineView()
        layout.addWidget(self.view)

        self.create_menus()
        self.setup_web_channel()

    def create_menus(self):
        file_menu = QMenu("File", self)
        act_save = QAction("Save Session", self)
        act_save.triggered.connect(self.save_session)
        file_menu.addAction(act_save)
        act_load = QAction("Open Session", self)
        act_load.triggered.connect(self.load_session)
        file_menu.addAction(act_load)
        act_pdf = QAction("Export PDF", self)
        act_pdf.triggered.connect(self.export_to_pdf)
        file_menu.addAction(act_pdf)
        file_menu.addSeparator()
        act_exit = QAction("Exit", self)
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)
        self.menuBar().addMenu(file_menu)

    def setup_web_channel(self):
        self.channel = QWebChannel()
        self.bridge = PythonBridge(self.view)
        self.channel.registerObject('python', self.bridge)
        self.view.page().setWebChannel(self.channel)
        self.view.setHtml(HTML_CONTENT)

    def save_session(self):
        self.view.page().runJavaScript(
            """
            (() => {
                const cells = Array.from(document.querySelectorAll('.cell'));
                return JSON.stringify(cells.map(c => ({
                    type: c.dataset.type,
                    code: editors[c.id].getValue()
                })));
            })()
            """, self.handle_save)

    def handle_save(self, data):
        if not data:
            QMessageBox.critical(self, "Save Error", "No data to save.")
            return
        session = json.loads(data)
        path, selected_filter = QFileDialog.getSaveFileName(
            self, "Save Session", "", "JSON Files (*.json);;Jupyter Notebook (*.ipynb)"
        )
        if path:
            if selected_filter == "JSON Files (*.json)":
                if not path.endswith('.json'):
                    path += '.json'
                with open(path, 'w') as f:
                    json.dump(session, f, indent=2)
            elif selected_filter == "Jupyter Notebook (*.ipynb)":
                if not path.endswith('.ipynb'):
                    path += '.ipynb'
                notebook = self.to_notebook(session)
                with open(path, 'w') as f:
                    json.dump(notebook, f, indent=2)
            QMessageBox.information(self, "Saved", f"Session saved to {path}")

    def load_session(self):
        path, selected_filter = QFileDialog.getOpenFileName(
            self, "Load Session", "", "JSON Files (*.json);;Jupyter Notebook (*.ipynb)"
        )
        if not path:
            return
        with open(path) as f:
            data = json.load(f)
        if selected_filter == "JSON Files (*.json)":
            session = data
        elif selected_filter == "Jupyter Notebook (*.ipynb)":
            session = self.from_notebook(data)
        else:
            QMessageBox.critical(self, "Load Error", "Unsupported file format.")
            return
        js = "clearCells();" + ''.join(
            f"addCell('{c['type']}'); editors[document.querySelector('.cell:last-child').id].setValue({json.dumps(c['code'])});"
            for c in session
        )
        self.view.page().runJavaScript(js)

    def export_to_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF Files (*.pdf)")
        if not path:
            return
        self.view.page().printToPdf(lambda data: open(path, 'wb').write(data) if data else None)

    def to_notebook(self, session):
        cells = []
        for cell in session:
            source = cell['code'].splitlines(keepends=True)
            if source and not source[-1].endswith('\n'):
                source[-1] += '\n'
            if cell['type'] == 'code':
                cells.append({
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": source
                })
            elif cell['type'] == 'markdown':
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": source
                })
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        return notebook

    def from_notebook(self, notebook):
        session = []
        for cell in notebook['cells']:
            if cell['cell_type'] in ['code', 'markdown']:
                code = ''.join(cell['source'])
                session.append({
                    "type": cell['cell_type'],
                    "code": code
                })
        return session

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
