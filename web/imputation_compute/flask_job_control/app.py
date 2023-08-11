from subprocess import Popen, TimeoutExpired, PIPE

from flask import Flask, jsonify, abort, request

app = Flask(__name__)


def rsyncJob(filePATH,):
    proc = Popen(["bash", f"""rsync -avzrtP   --info=progress2 --zc=lz4 -e "ssh -p 22" { filePATH } soliva@89.207.132.170:/home/soliva/ """], stdout=PIPE, stderr=PIPE,shell=True)
    try:
        outs, errs = proc.communicate(timeout=1)
    except TimeoutExpired:
        proc.kill()
        abort(500, description="The timeout is expired!")
    return outs


@app.route("/", methods=["POST"])
def index():
    req_json = request.get_json()

    if req_json is None or "command" not in req_json:
        abort(400, description="Please provide command in JSON request!")

    proc = Popen(req_json["command"], stdout=PIPE, stderr=PIPE, shell=True)

    try:
        outs, errs = proc.communicate(timeout=1)
    except TimeoutExpired:
        proc.kill()
        abort(500, description="The timeout is expired!")

    if errs:
        abort(500, description=errs.decode('utf-8'))

    return jsonify(success=True, message=outs.decode('utf-8'))

@app.errorhandler(400)
def bad_request(error):
    return jsonify(success=False, message=error.description), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify(success=False, message=error.description) , 500