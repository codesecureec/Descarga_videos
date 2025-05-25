# 🎥 Descargador de Videos de YouTube

Un script en Python que permite descargar videos y audio de YouTube de manera sencilla y eficiente.

## ✨ Características

- 📥 Descarga de videos en alta calidad
- 🎵 Opción para descargar solo audio en formato MP3
- 📊 Barra de progreso visual durante la descarga
- 🔄 Soporte para múltiples formatos de video
- 🌐 Compatible con Windows, macOS y Linux
- 🛡️ Manejo de errores y verificaciones de seguridad
- 🎨 Interfaz de usuario amigable con emojis
- 🔒 Uso de User-Agents aleatorios para evitar bloqueos

## 📋 Requisitos

- Python 3.6 o superior
- yt-dlp (se instalará automáticamente con pip)
- ffmpeg (opcional, pero recomendado para mejor calidad)

## 🚀 Instalación

1. Clona este repositorio o descarga los archivos
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Instalación de ffmpeg (recomendado)

#### Windows
```bash
winget install ffmpeg
```
O descarga desde: https://ffmpeg.org/download.html

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

## 💻 Uso

1. Ejecuta el script:
```bash
python main.py
```

2. Ingresa la URL del video de YouTube cuando se te solicite

3. Selecciona el tipo de descarga:
   - 1: Video completo
   - 2: Solo audio (MP3)

4. Espera a que se complete la descarga

Los archivos se guardarán en tu carpeta de Descargas:
- Windows: `C:\Users\<usuario>\Downloads`
- macOS/Linux: `/Users/<usuario>/Downloads`

## ⚠️ Notas importantes

- El programa requiere conexión a internet
- Algunos videos pueden requerir verificación de edad o estar restringidos
- La calidad del video dependerá de la disponibilidad en YouTube
- Se recomienda tener ffmpeg instalado para mejor calidad de video y audio

## 🔧 Solución de problemas

Si encuentras algún error:

1. Verifica tu conexión a internet
2. Asegúrate de que la URL del video sea válida
3. Si el video requiere verificación:
   - Abre el video en tu navegador
   - Completa la verificación si es necesario
   - Intenta descargar nuevamente
4. Actualiza yt-dlp si hay problemas de formato:
```bash
pip install -U yt-dlp
```

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## ⚠️ Aviso legal

Este programa es solo para uso personal y educativo. Respeta los derechos de autor y las políticas de YouTube. El uso de este programa para descargar contenido protegido por derechos de autor sin permiso puede ser ilegal en tu jurisdicción. 