def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
            "Access-Control-Allow-Origin": "*"
        },
        "body": """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Editor de cronograma</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    * {
      box-sizing: border-box;
      font-family: Arial, sans-serif;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: #f4f6f8;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .container {
      background: #ffffff;
      width: 100%;
      max-width: 600px;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    h2 {
      margin-top: 0;
      text-align: center;
    }

    textarea {
      width: 100%;
      min-height: 200px;
      padding: 10px;
      resize: vertical;
      border-radius: 4px;
      border: 1px solid #ccc;
      font-size: 14px;
    }

    button {
      margin-top: 15px;
      width: 100%;
      padding: 12px;
      font-size: 16px;
      border: none;
      border-radius: 4px;
      background: #007bff;
      color: white;
      cursor: pointer;
    }

    button:hover {
      background: #0056b3;
    }

    #estado {
      margin-top: 10px;
      text-align: center;
      font-weight: bold;
    }
  </style>
</head>

<body>
  <div class="container">
    <h2>Editar cronograma</h2>

    <textarea id="texto" placeholder="Escribí el cronograma acá..."></textarea>

    <button onclick="guardar()">Guardar</button>

    <p id="estado"></p>
  </div>

<script>
const ID = "cronograma";
const API = "REEMPLAZAR_URL_API";

async function cargar() {
  const r = await fetch(API);
  const j = await r.json();
  document.getElementById("texto").value = j.texto || "";
}

async function guardar() {
  const texto = document.getElementById("texto").value;
  const r = await fetch(API, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ texto })
  });

  const j = await r.json();
  document.getElementById("estado").innerText =
    j.ok ? "✅ Guardado correctamente" : "❌ " + j.error;
}

cargar();
</script>
</body>
</html>
"""
    }
