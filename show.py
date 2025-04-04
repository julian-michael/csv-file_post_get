from flask import request, redirect

@app.route("/showdata", methods=["GET"])
def show_data():
    filename = request.args.get("filename")
    
    if not filename:
        return "No file selected.", 400

    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(full_path):
        return "File does not exist.", 404

    try:
        df = pd.read_csv(full_path)
        return render_template("data.html", tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
