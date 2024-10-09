from flask import Flask, send_from_directory, abort, request
import os
import logging

log = logging.getLogger('werkzeug')
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)
log.disabled = True

home_directory = os.path.join(os.getcwd(), 'Home')
home_directory2 = os.path.join(os.getcwd(), 'MoreHome')
images_shared_directory = os.path.join(home_directory2, 'Images', 'Shared')

# Define the directory for HTML files
html_directory = os.path.join(os.getcwd(), 'ServerHTML')  # Change this to the path where your HTML files are stored

headwaiter = Flask(__name__)
service = Flask(__name__)
home = Flask(__name__)

@home.route('/Pages/<path:filename>')
def serve_file(filename):
    try:
        requester = request.remote_addr
        print(f"Got request from: {requester}, {filename}")
        return send_from_directory(home_directory, filename)
    except FileNotFoundError:
        abort(404)

@home.route('/Images/Shared/<path:filename>')
def serve_image(filename):
    try:
        requester = request.remote_addr
        print(f"Got request from: {requester}, {filename}")
        return send_from_directory(images_shared_directory, filename)
    except FileNotFoundError:
        abort(404)

@service.route('/')
def returnNilIfNoHTML():
    requester = request.remote_addr
    print(f"Got request from: {requester}, eval.html ")
    return send_from_directory(html_directory, 'eval.html')

@service.route('/connection/bootstrap.html', methods=['POST', 'GET'])
def strap():
    requester = request.remote_addr
    print(f"Got request from: {requester}, bootstrap.html")
    return send_from_directory(html_directory, 'bootstrap.html')

@service.route('/connection/boxcheck.html', methods=['POST', 'GET'])
def returnboxcheck():
    requester = request.remote_addr
    print(f"Got request from: {requester}, boxcheck.html")
    return send_from_directory(html_directory, 'boxcheck.html')

@service.route('/connection/usercheck.html')
def returnusercheck():
    requester = request.remote_addr
    print(f"Got request from: {requester}, usercheck_mock.html")
    return send_from_directory(html_directory, 'usercheck_mock.html')

@service.route('/connection/kickstart.aspx')
def returnkickstart():
    requester = request.remote_addr
    print(f"Got request from: {requester}, kickstart.aspx")
    return send_from_directory(html_directory, 'kickstart.aspx')

@service.route('/connection/GatePage.aspx', methods=['GET'])
def gate_page():
    requester = request.remote_addr
    print(f"Got request from: {requester}, GatePage.aspx")
    if request.args.get('phase') == 'Bootstrap' and request.args.get('purpose') == 'Authorize':
        return send_from_directory(html_directory, 'GatePage.aspx')
    else:
        return send_from_directory(html_directory, 'GatePage.aspx')

@headwaiter.route('/')
def returnBootstrap():
    requester = request.remote_addr
    print(f"Got request from: {requester}, bootstrap.html")
    return send_from_directory(html_directory, 'bootstrap.html')
