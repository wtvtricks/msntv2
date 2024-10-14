from flask import Flask, send_from_directory, abort, request, Response
import os
import logging
from datetime import datetime

#log = logging.getLogger('werkzeug')
#werkzeug_logger = logging.getLogger('werkzeug')
#werkzeug_logger.setLevel(logging.ERROR)
#log.disabled = False

home_directory = os.path.join(os.getcwd(), 'Home')
home_directory2 = os.path.join(os.getcwd(), 'MoreHome')
images_shared_directory = os.path.join(home_directory2, 'Images', 'Shared')

# Define the directory for HTML files
html_directory = os.path.join(os.getcwd(), 'ServerHTML')  # Change this to the path where your HTML files are stored
hour_mapping = {
    0: 17,  # 5pm
    1: 18,  # 6pm
    2: 19,  # 7pm
    3: 20,  # 8pm
    4: 21,  # 9pm
    5: 22,  # 10pm
    6: 23,  # 11pm
    7: 0,   # 12am
    8: 1,   # 1am
    9: 2,   # 2am
    10: 3,  # 3am
    11: 4,  # 4am
    12: 5,  # 5am
    13: 6,  # 6am
    14: 7,  # 7am
    15: 8,  # 8am
    16: 9,  # 9am
    17: 10, # 10am
    18: 11, # 11am
    19: 12, # 12pm
    20: 13, # 1pm
    21: 14, # 2pm
    22: 15, # 3pm
    23: 16  # 4pm
}

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

@service.route('/mid')
def returnmid():
    return send_from_directory(html_directory, 'mid.mid')

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
    

@service.route('/clock')
def time():
    now = datetime.now()
    mapped_hour = hour_mapping.get(now.hour)
    
    if mapped_hour is None:
        print(f"Hour {now.hour} is not mapped, using fallback.")
        mapped_hour = now.hour  # Fallback if mapping is missing
    
    # Ensure formatting is correct
    clock = f"{mapped_hour:02},{now.minute:02},{now.second:02},{now.month},{now.day},{now.year}"
    
    # Debug the final clock string
    print(f"Clock string: {clock}")
    
    return Response(clock)



@headwaiter.route('/')
def returnBootstrap():
    requester = request.remote_addr
    print(f"Got request from: {requester}, bootstrap.html")
    return send_from_directory(html_directory, 'bootstrap.html')
