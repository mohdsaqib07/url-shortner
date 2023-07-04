from flask import Flask,render_template,request,abort,redirect,url_for,flash,session,jsonify
import json
import os
from werkzeug.utils import secure_filename
def run_app():
    app=Flask(__name__)
    app.secret_key="any random string can be a secret key"
    app.config['UPLOAD_FOLDER'] = 'C:\\Users\saqib\\PycharmProjects\\url-shortner\static\\user_files'

    @app.route('/', methods=['GET'])
    def index():
        return render_template('home.html',codes=session.keys(),title='Home')

    @app.route('/yoururl',methods=['POST','GET'])
    def your_url():
        if request.method == 'POST':
            # url={'url':request.form['url'],'shortenurl':request.form['code']}
            url=dict()
            url.clear()
            if os.path.exists('config.json'):
                with open('config.json') as f:
                    url=json.loads(f.read())
            if request.form['code'] in url.keys():
                flash("That short name is already been taken please provide a different short name for your url ","warning")
                return redirect(url_for('index'))

            if 'url' in request.form.keys():
                url[request.form['code']]={'url':request.form['url']}
            else:
                file=request.files['file']
                fullname=request. form['code'] + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],fullname))
                url[request.form['code']] = {'file': fullname}
            with open('config.json','w') as f:
                f.write(json.dumps(url))
            session[request.form['code']] = True
            code=request.form['code']
            return render_template('yoururl.html',code=code,title=f'Your url {code}',url=f'http://localhost:5000/{code}')

        else:
            # abort(401)
            return(redirect(url_for('index')))

    @app.route('/<string:code>')
    def redirect_to_url(code):
        if os.path.exists('config.json'):
            with open('config.json') as f:
                url=json.load(f)
                if code in url.keys():
                    if 'url' in url[code].keys():
                        return redirect(url[code]['url'])
                    else:
                        return(redirect(url_for('static',filename='user_files/' + url[code]['file'])))
                        #   webbrowser.open_new_tab(url[code]['url'])
                else:
                    abort(404)

    # By default a black and white error page is shown for each error code. If you want to customize the error page, you can use the errorhandler() decorator:
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('url_not_found.html'), 404
    # Note the 404 after the render_template() call. This tells Flask that the status code of that page should be 404 which means not found. By default 200 is assumed which translates to: all went well.

    @app.route('/api')
    def session_api():
        return jsonify(list(session.keys()))
    app.run(debug=True)
    # app.run(host='0.0.0.0')
if __name__=='__main__':
    run_app()