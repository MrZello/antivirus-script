from flask import Flask, request

app = Flask(__name__)
files = list()
out = list()

@app.route("/api/add",methods=['POST'])
def api_add():
        msg = ''
        fName = request.args.get('fileName', files)
        md5 = request.args.get('md5', files)
        if type(fName) == list:
                return ''
        else:
                files.append(fName)
                files.append(md5)
                if len(out) >= 1: out.clear()
                
        for each in range(0,len(files)-1,2):
                msg = f'Deleted file {files[each]} with MD5 checksum {files[each+1]}<br>'
                out.append(msg)
                if each+1 == len(files)-1:
                        return ''



@app.route("/")
def root():
        run = api_add()
        str1 = ''
        for each in out:
                str1 += each

        return f'{str1}'



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
