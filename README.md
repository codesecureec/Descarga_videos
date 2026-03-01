# 🎥 Descargador de Videos de YouTube

Un script en Python para descargar videos y audio de YouTube, ahora con **selección de calidad de video** para priorizar mejor resolución según tus necesidades.

## ✨ Características

- 📥 Descarga de videos en la mejor calidad disponible
- 🎚️ Selector de resolución máxima (4K, 2K, 1080p, 720p o mejor disponible)
- 🎵 Opción para descargar solo audio en formato MP3
- 📊 Barra de progreso visual durante la descarga
- 🌐 Compatible con Windows, macOS y Linux
- 🛡️ Manejo de errores y recomendaciones cuando YouTube exige verificación
- 🔒 Uso de User-Agents aleatorios para reducir bloqueos

## 📋 Requisitos

- Python 3.8 o superior
- `yt-dlp`
- `ffmpeg` (**muy recomendado** para mezclar video+audio en la mejor calidad)

## 🚀 Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Instalación de ffmpeg

#### Windows
```bash
winget install ffmpeg
```

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

2. Ingresa la URL del video de YouTube.
3. Elige el tipo de descarga:
   - `1`: Video completo
   - `2`: Solo audio (MP3)
4. Si eliges video, selecciona la calidad máxima:
   - `1`: Mejor disponible
   - `2`: 2160p (4K)
   - `3`: 1440p (2K)
   - `4`: 1080p (Full HD)
   - `5`: 720p (HD)

Los archivos se guardan en tu carpeta de Descargas (`~/Downloads` en macOS/Linux y `C:\Users\<usuario>\Downloads` en Windows).

## 🔧 Solución de problemas

- Si no se descarga en alta calidad, verifica que `ffmpeg` esté instalado.
- Si YouTube muestra "Sign in to confirm", abre ese video en navegador y completa la verificación.
- Si hay errores de formatos, actualiza yt-dlp:

```bash
pip install -U yt-dlp
```

## ⚖️ Aviso legal

Este programa es solo para uso personal y educativo. Respeta derechos de autor y términos de uso de YouTube.
