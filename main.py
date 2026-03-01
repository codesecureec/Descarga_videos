import yt_dlp
import os
import sys
import subprocess
import platform
import random


VIDEO_QUALITY_PRESETS = {
    "1": ("Mejor disponible", None),
    "2": ("2160p (4K)", 2160),
    "3": ("1440p (2K)", 1440),
    "4": ("1080p (Full HD)", 1080),
    "5": ("720p (HD)", 720),
}

def get_random_user_agent():
    """Retorna un user agent aleatorio de navegador moderno"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def is_ffmpeg_installed():
    """Verifica si ffmpeg está instalado"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_download_path():
    """Obtiene la ruta de descargas según el sistema operativo"""
    if platform.system() == "Windows":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    return os.path.join(os.path.expanduser("~"), "Downloads")

def format_duration(seconds):
    """Convierte segundos a formato HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def download_progress_hook(d):
    """Función para mostrar el progreso de la descarga"""
    if d['status'] == 'downloading':
        # Obtener el progreso
        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        downloaded = d.get('downloaded_bytes', 0)
        
        if total > 0:
            percentage = (downloaded / total) * 100
            # Crear barra de progreso
            bar_length = 50
            filled_length = int(bar_length * downloaded // total)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            # Limpiar línea actual y mostrar progreso
            sys.stdout.write('\r')
            sys.stdout.write(f'[{bar}] {percentage:.1f}%')
            sys.stdout.flush()

def get_download_format(download_type, max_height=None):
    """Obtiene el formato de descarga según el tipo seleccionado"""
    if download_type == "1":  # Video
        if is_ffmpeg_installed():
            if max_height:
                return (
                    f'bestvideo[vcodec!=none][height<={max_height}]+'
                    f'bestaudio[acodec!=none]/best[height<={max_height}]/best'
                )
            return 'bestvideo[vcodec!=none]+bestaudio[acodec!=none]/best'
        if max_height:
            return f'best[height<={max_height}]/best'
        return 'best'
    elif download_type == "2":  # Solo Audio
        return 'bestaudio/best'
    return 'best'


def choose_video_quality():
    """Permite seleccionar la calidad máxima deseada para video."""
    print("\n🎚️ Selecciona la calidad máxima de video:")
    for option, (label, _) in VIDEO_QUALITY_PRESETS.items():
        print(f"{option}. {label}")

    while True:
        selected = input("\n📝 Opción de calidad (1-5): ").strip()
        if selected in VIDEO_QUALITY_PRESETS:
            label, height = VIDEO_QUALITY_PRESETS[selected]
            print(f"✅ Calidad seleccionada: {label}")
            return height
        print("❌ Por favor, selecciona una opción válida (1-5)")

def get_output_template(download_type):
    """Obtiene la plantilla de nombre de archivo según el tipo de descarga"""
    if download_type == "2":  # Solo Audio
        return os.path.join(get_download_path(), "%(title)s.%(ext)s")
    return os.path.join(get_download_path(), "%(title)s.%(ext)s")

def download_video(url, download_type, max_height=None):
    """Función principal para descargar el video o audio"""
    try:
        print("\n🔄 Conectando a YouTube...")
        
        # Obtener formato según el tipo de descarga
        format_option = get_download_format(download_type, max_height)
        is_audio_only = download_type == "2"
        
        # Configuración base de yt-dlp
        ydl_opts = {
            'format': format_option,
            'progress_hooks': [download_progress_hook],
            'quiet': True,
            'no_warnings': True,
            'outtmpl': get_output_template(download_type),
            'http_headers': {
                'User-Agent': get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['js', 'configs', 'webpage'],
                }
            },
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_color': True,
            'geo_bypass': True,
            'geo_verification_proxy': None,
            'merge_output_format': 'mp4',
        }
        
        # Configurar postprocesadores según el tipo de descarga
        if is_audio_only:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        # Para video evitamos FFmpegVideoConvertor porque cambia entre versiones
        # de yt-dlp (preferedformat/preferredformat) y puede romper la descarga.
        # merge_output_format=mp4 ya se encarga de la salida cuando ffmpeg está disponible.
        
        # Primero obtener información del video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\n📹 Obteniendo información del video...")
            try:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("No se pudo obtener información del video")
            except Exception as e:
                if "Sign in to confirm" in str(e):
                    print("\n⚠️  YouTube está solicitando verificación.")
                    print("💡 Intenta estos pasos:")
                    print("1. Abre el video en tu navegador")
                    print("2. Completa la verificación si es necesario")
                    print("3. Intenta descargar nuevamente")
                    return False
                raise e
            
            # Mostrar información del video
            print("\n📹 Información del video:")
            print(f"Título: {info['title']}")
            print(f"Duración: {format_duration(info['duration'])}")
            print(f"Vistas: {info.get('view_count', 'N/A'):,}")
            
            # Descargar el video o audio
            print("\n📥 Iniciando descarga...")
            if is_audio_only:
                print("🎵 Descargando solo audio...")
            else:
                print("🎥 Descargando video...")
                if max_height:
                    print(f"🎯 Resolución máxima solicitada: {max_height}p")
                else:
                    print("🎯 Resolución: mejor disponible")
            
            ydl.download([url])
        
        # Mostrar mensaje de éxito
        print("\n\n✅ ¡Descarga completada!")
        print(f"📁 Archivo guardado en: {get_download_path()}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if "Sign in to confirm" in str(e):
            print("\n⚠️  YouTube está solicitando verificación.")
            print("💡 Intenta estos pasos:")
            print("1. Abre el video en tu navegador")
            print("2. Completa la verificación si es necesario")
            print("3. Intenta descargar nuevamente")
        elif "format not available" in str(e).lower():
            print("\n💡 Sugerencia: Intenta actualizar yt-dlp con el comando:")
            print("pip install -U yt-dlp")
        return False
    
    return True

def main():
    """Función principal del programa"""
    # Configurar la consola para Windows
    if platform.system() == "Windows":
        os.system('color')  # Habilitar colores en Windows
        os.system('cls')    # Limpiar pantalla en Windows
    else:
        os.system('clear')  # Limpiar pantalla en Unix/Mac
    
    print("=" * 80)
    print("🎥 Descargador de Videos de YouTube - Versión Windows")
    print("=" * 80)
    
    # Verificar ffmpeg
    if not is_ffmpeg_installed():
        print("\n⚠️  ffmpeg no está instalado.")
        print("💡 Para mejor calidad, instala ffmpeg desde: https://ffmpeg.org/download.html")
        print("   O ejecuta: winget install ffmpeg")
    
    while True:
        # Obtener URL del usuario
        url = input("\n📝 Ingresa la URL del video (o 'q' para salir): ").strip()
        
        if url.lower() == 'q':
            print("\n👋 ¡Gracias por usar el descargador!")
            break
        
        if not url:
            print("❌ Por favor, ingresa una URL válida")
            continue
        
        # Preguntar tipo de descarga
        print("\n📋 Selecciona el tipo de descarga:")
        print("1. Video completo")
        print("2. Solo audio (MP3)")
        
        while True:
            download_type = input("\n📝 Selecciona una opción (1-2): ").strip()
            if download_type in ["1", "2"]:
                break
            print("❌ Por favor, selecciona una opción válida (1-2)")
        
        # Intentar descargar
        max_height = None
        if download_type == "1":
            max_height = choose_video_quality()

        success = download_video(url, download_type, max_height)
        
        if success:
            print("\n" + "=" * 80)
            print("¿Deseas descargar otro archivo?")
        else:
            print("\n" + "=" * 80)
            print("Hubo un error en la descarga. ¿Deseas intentar con otro archivo?")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa terminado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
    finally:
        print("\n" + "=" * 80)
        if platform.system() == "Windows":
            input("\nPresiona Enter para salir...") 
