from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def root():
    #  The form which POSTs the data must cause the browser to transmit the file that we want to upload and our method that the route executes must also access the request and do something with the transmitted file. Otherwise the file will sit by default either in memory or in temptorary storage rather then being saved for later reuse


    # allows user to upload files to site. First checks if file is present when submit button pressed
    # NOTE this can overwrite current files in upload directory
    if request.method == 'POST':
        # checks post request has the file part
        if 'file' not in request.files:
            return "No files uploaded"
        else:
            file = request.files['file']
            # if user does not select a file, browser submits an empty file without a filename
            if file.filename == '':
                return "No file selected"
            else:
                file.save('static/uploads/'+file.filename) # saves in a subdirectory of static - subdirectory MUST be present
        return "File Uploaded"
    else:
        page='''
        <html>
        <body>
        <form action="" method="post" name="form" enctype="multipart/form-data">
            <input type="file" name="file" />
            <input type="submit" name="submit" id="submit"/>
        </form>
        </body>
        </html>
        '''

    return page, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)