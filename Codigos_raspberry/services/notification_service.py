import requests


class NotificationService:

    def enviar_whatsapp(self, telefono, mensaje):

        url = f"https://api.callmebot.com/whatsapp.php"

        payload = {
            "phone": telefono,
            "text": mensaje,
            "apikey": "9733456"
        }

        response = requests.get(url, params=payload)

        print(response.status_code)