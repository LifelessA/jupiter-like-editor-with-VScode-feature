import sys
import os
import json
import base64
import io
import ast
import asyncio
import logging
from html import escape
from contextlib import redirect_stdout

try:
    import fastapi
    import uvicorn
    from fastapi.responses import HTMLResponse
    from starlette.websockets import WebSocket, WebSocketDisconnect
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import pandas as pd
    import jedi
except ImportError:
    print("Installing required packages: fastapi uvicorn python-multipart matplotlib pandas jedi")
    # Use sys.executable to ensure pip is from the correct env
    os.system(f'"{sys.executable}" -m pip install "fastapi[all]" uvicorn python-multipart matplotlib pandas jedi')
    import fastapi
    import uvicorn
    from fastapi.responses import HTMLResponse
    from starlette.websockets import WebSocket, WebSocketDisconnect
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import pandas as pd
    import jedi

app = fastapi.FastAPI()
logging.getLogger('websockets').setLevel(logging.ERROR)

class NotebookServer:
    def __init__(self):
        self.locals = {'plt': plt, 'pd': pd}
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        print(f"Client connected: {session_id}")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            print(f"Client disconnected: {session_id}")

    async def handle_message(self, websocket: WebSocket, session_id: str, message: str):
        data = json.loads(message)
        msg_type = data.get('type')
        loop = asyncio.get_event_loop()

        if msg_type == 'run_code':
            # Run the blocking code execution in a thread pool
            output = await loop.run_in_executor(
                None, self.execute, data['code']
            )
            await websocket.send_json({
                'type': 'output',
                'cell_id': data['cell_id'],
                'output': output
            })
        elif msg_type == 'get_completions':
            completions = self.get_completions(data['code'], data['line'], data['column'])
            await websocket.send_json({
                'type': 'completions',
                'completions': completions
            })
        elif msg_type == 'apply_design':
            notebook_session_id = data.get('session_id')
            if notebook_session_id in self.active_connections:
                target_ws = self.active_connections[notebook_session_id]
                await target_ws.send_json({
                    'type': 'design_applied',
                    'html': data['html']
                })

    def execute(self, code):
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                tree = ast.parse(code)
                if tree.body and isinstance(tree.body[-1], ast.Expr):
                    if len(tree.body) > 1:
                        exec_code = compile(ast.Module(tree.body[:-1], type_ignores=[]), '<string>', 'exec')
                        exec(exec_code, self.locals)
                    eval_code = compile(ast.Expression(tree.body[-1].value), '<string>', 'eval')
                    result = eval(eval_code, self.locals)
                    if isinstance(result, pd.DataFrame):
                        buf.write(result.to_html())
                    elif result is not None:
                        buf.write(str(result))
                else:
                    exec(code, self.locals)
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

    def get_completions(self, code, line, column):
        try:
            interpreter = jedi.Interpreter(code, [self.locals])
            completions = interpreter.complete(line=line + 1, column=column)
            return [c.name for c in completions]
        except Exception as e:
            print(f"Completion error: {e}")
            return []

server = NotebookServer()

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/design", response_class=HTMLResponse)
async def get_design():
    with open("design_animation.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await server.connect(websocket, session_id)
    try:
        while True:
            message = await websocket.receive_text()
            await server.handle_message(websocket, session_id, message)
    except WebSocketDisconnect:
        server.disconnect(session_id)
    
@app.post("/save")
async def save_file(request: fastapi.Request):
    data = await request.json()
    filename = data.get("filename")
    content = data.get("content")

    if not filename or content is None:
        return fastapi.Response(content=json.dumps({"status": "error", "message": "Filename or content missing."}), status_code=400)

    try:
        # Basic security check to prevent path traversal
        if ".." in filename or os.path.isabs(filename):
             return fastapi.Response(content=json.dumps({"status": "error", "message": "Invalid filename."}), status_code=400)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"File saved: {filename}")
        return {"status": "ok", "message": f"File '{filename}' saved successfully."}
    except Exception as e:
        print(f"Error saving file {filename}: {e}")
        return fastapi.Response(content=json.dumps({"status": "error", "message": str(e)}), status_code=500)

if __name__ == "__main__":
    print("Starting server...")
    print("Open http://localhost:8000 in your browser.")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
