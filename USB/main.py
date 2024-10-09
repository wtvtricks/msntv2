from flask import Flask, Response

bootstrap = Flask(__name__)

@bootstrap.route('/')
def returnBootstrap():
    return Response("<script>window.location='msntv:/../hard disk/putonusb.html'</script>")

if __name__ == '__main__':
    bootstrap.run(host='0.0.0.0', port=80)
