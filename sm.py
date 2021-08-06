import africastalking

class SMS:
    def __init__(self):

    # Set your app credentials
        self.username = "heskay32"
        self.api_key = "089bbd4a7a1f1c1f9f2fc5dfb3c21493ef38b4b28d878ae635ba65fcc593ec9a"

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self):
            # Set the numbers you want to send to in international format
            recipients = ["+23408068725871"]

            # Set your message
            message = "I'm a lumberjack and it's ok, I sleep all night and I work all day";

            # Set your shortCode or senderId
            #sender = "KPTC20"
            try:
        # Thats it, hit send and we'll take care of the rest.
                response = self.sms.send(message, recipients)
                print (response)
            except Exception as e:
                print ('Encountered an error while sending: %s' % str(e))

if __name__ == '__main__':
    SMS().send()