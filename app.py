from flask import Flask, request, render_template, redirect, url_for, flash
import uuid
from agents.classifier_agent import ClassifierAgent

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

classifier = ClassifierAgent()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file:
            # Save uploaded file temporarily
            filepath = f"uploads/{uuid.uuid4()}_{file.filename}"
            file.save(filepath)
            
            conversation_id = str(uuid.uuid4())
            try:
                result = classifier.route(filepath, conversation_id)
                return render_template("result.html", result=result, conv_id=conversation_id)
            except Exception as e:
                flash(f"Error processing file: {e}")
                return redirect(request.url)

    return render_template("index.html")

if __name__ == "__main__":
    import os
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
