import socket
from app import app, init_db

def get_ip_address():
    try:
        # Connect to a public DNS server to determine the best local IP
        # We don't actually send data, just initiating the socket logic
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    ip = get_ip_address()
    port = 5000
    
    print("\n" + "="*50)
    print(f" JEWELRY TRACKER - LAN MODE")
    print("="*50)
    print(f" Server is starting...")
    print(f" -> On this computer: http://localhost:{port}")
    print(f" -> ON OTHER DEVICES: http://{ip}:{port}")
    print("="*50 + "\n")
    
    # Ensure DB is initialized
    with app.app_context():
        init_db()
        
    app.run(host='0.0.0.0', port=port, debug=False)
