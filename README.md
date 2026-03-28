# 📝 Sistema de Gestión de Cronograma (Iglesia)

Aplicación desarrollada para la gestión y visualización en tiempo real de un cronograma compartido.

Incluye:

* Editor web
* API serverless en AWS
* Base de datos DynamoDB
* Cliente de escritorio en Python

---

## 🎯 Objetivo del proyecto

Este proyecto fue desarrollado como solución práctica para la gestión de información en tiempo real, aplicando conceptos de:

* Arquitectura serverless
* Comunicación cliente-servidor
* Sincronización de estado
* Testing manual con Insomnia
* Diseño funcional

---

## 🚀 Tecnologías utilizadas

* Python (Tkinter, Requests)
* AWS Lambda
* Amazon DynamoDB
* API Gateway
* HTML / JavaScript
* Pillow (manejo de imágenes)

---

## 🧩 Arquitectura

![Arquitectura](docs/arquitectura.png)

* Frontend web consume API REST
* Backend serverless procesa requests
* DynamoDB almacena el estado
* Cliente desktop sincroniza en tiempo real mediante long polling

---

## 🔄 Flujo de funcionamiento

![Flujo](docs/flujo.png)

1. Cliente consulta el estado actual (GET)
2. Usuario edita contenido (PATCH)
3. Se incrementa versión en base de datos
4. Clientes reciben actualización automáticamente

---

## ✨ Funcionalidades

* Edición de texto en tiempo real
* Sincronización automática entre clientes
* Renderizado de emojis en aplicación desktop
* Sistema de versionado para evitar conflictos
* Indicador de estado de conexión
* Configuración persistente

---

## ⚙️ Configuración

El proyecto utiliza URLs configurables a través del json que genera automáticamente la aplicación:

```json
{
  "url_crud": "REEMPLAZAR_URL_API",
  "url_web": "REEMPLAZAR_URL_WEB"
}
```

---

## ⚠️ Consideraciones
Debido a que se utiliza en un entorno controlado:
* No incluye autenticación 
* CORS abiertos

---

## 📸 Capturas

![App](docs/screenshot.png)


---

## 👤 Autor

Agustín Cardozo - Estudiante de Ingeniería en Sistemas de Información
