let pyodide;

async function startGame() {
  pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip"); // if you plan to use pip packages
  const response = await fetch("game.py");
  await pyodide.runPythonAsync(await response.text());
}


function submitInput() {
  const input = document.getElementById("user-input").value;
  document.getElementById("user-input").value = "";
  pyodide.runPythonAsync(`handle_input("${input}")`);
}

function printToScreen(text) {
  const outputDiv = document.getElementById("output");
  outputDiv.innerHTML += `<div>${text}</div>`;
  outputDiv.scrollTop = outputDiv.scrollHeight;
}

startGame();
