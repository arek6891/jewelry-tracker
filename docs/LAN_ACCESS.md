# How to Connect Devices (LAN Access)

Your application is configured to run on your local network (Intranet). This allows tablets, phones, and other computers to access the dashboard without needing internet cloud hosting.

## 1. Start the Server
1.  Open the folder containing the project files.
2.  Run the **`run_lan.py`** script (double-click or run from terminal: `python run_lan.py`).
3.  A black window (console) should appear. Look for a message like:

    ```
    ==================================================
     JEWELRY TRACKER - LAN MODE
    ==================================================
     Server is starting...
     -> On this computer: http://localhost:5000
     -> ON OTHER DEVICES: http://192.168.1.15:5000
    ==================================================
    ```

    **Write down the address listed under "ON OTHER DEVICES"**.

## 2. Connect a Tablet / Phone
1.  Ensure the tablet/phone is connected to the **SAME Wi-Fi** network as your computer.
2.  Open the web browser (Chrome, Safari, etc.).
3.  Type the address you wrote down into the address bar (e.g., `http://192.168.1.15:5000`).
4.  Log in!

## Troubleshooting

### "This site can't be reached"
If devices cannot connect:
1.  **Check Network**: Are both devices on the same Wi-Fi? (Guest networks usually block connections).
2.  **Windows Firewall**:
    -   When you first run the script, Windows might ask for permission. Click **"Allow Access"**.
    -   If you already clicked "Cancel", you need to allow Python through the firewall manually.
    -   **Quick Test**: Temporarily turn off Windows Firewall to see if that fixes it. If yes, add an exception for port `5000`.

### The IP address changes?
Your computer's IP address (`192.168.x.x`) might change if you restart your router. 
-   Always check the screen when you start `run_lan.py` to see the current address.
-   (Advanced) Ask your IT admin to set a "Static IP" for your computer.
