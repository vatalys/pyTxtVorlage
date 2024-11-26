from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Flask-Instanz erstellen
app = Flask(__name__)

# SQLite-Datenbank konfigurieren
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///textvorlagen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Datenbankmodell
class TextTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Tabellen erstellen, falls sie nicht existieren
with app.app_context():
    db.create_all()

# Route: Index (Frontend-Seite)
@app.route('/')
def index():
    return render_template('index.html')

# API: Alle Vorlagen abrufen oder nach Suchbegriffen filtern
@app.route('/api/templates', methods=['GET'])
def get_templates():
    query = request.args.get('query', '').strip()
    print(f"Suchbegriff: {query}")  # Debugging

    if not query:
        templates = TextTemplate.query.all()  # Alle Vorlagen abrufen
        print(f"Alle Vorlagen: {[t.title for t in templates]}")  # Debugging
    else:
        # Suche in `title` und `content`
        templates = TextTemplate.query.filter(
            (TextTemplate.title.ilike(f"%{query}%")) |
            (TextTemplate.content.ilike(f"%{query}%"))
        ).all()
        print(f"Gefundene Vorlagen: {[t.title for t in templates]}")  # Debugging

    return jsonify([{'id': t.id, 'title': t.title, 'content': t.content} for t in templates])

# API: Neue Vorlage hinzufügen
@app.route('/api/templates', methods=['POST'])
def add_template():
    data = request.json
    print(f"Eingehende Daten: {data}")  # Debugging
    new_template = TextTemplate(title=data['title'], content=data['content'])
    db.session.add(new_template)
    db.session.commit()
    return jsonify({'message': 'Template added successfully!'})

# Hauptprogramm starten
if __name__ == '__main__':
    app.run(debug=True)
