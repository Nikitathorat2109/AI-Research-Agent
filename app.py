from flask import Flask, render_template, request, jsonify, redirect, url_for
from agent import ResearchAgent
from database import Database
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
agent = ResearchAgent()
db = Database()

@app.route('/')
def index():
    """Main page showing query form and recent reports"""
    reports = db.get_all_reports()
    return render_template('index.html', reports=reports, config=os.environ)

@app.route('/research', methods=['POST'])
def research():
    """Handle research request"""
    query = request.form.get('query', '').strip()
    
    if not query:
        if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            return jsonify({'error': 'Query is required'}), 400
        return jsonify({'error': 'Query is required'}), 400
    
    # Perform research
    result = agent.research(query)
    
    if 'error' in result:
        return jsonify(result), 500
    
    # For AJAX requests, return JSON with redirect URL
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'redirect': url_for('view_report', report_id=result['id'])})
    
    return redirect(url_for('view_report', report_id=result['id']))

@app.route('/report/<int:report_id>')
def view_report(report_id):
    """View a specific report"""
    report = db.get_report(report_id)
    
    if not report:
        return "Report not found", 404
    
    return render_template('report.html', report=report)

@app.route('/api/reports')
def api_reports():
    """API endpoint to get all reports"""
    reports = db.get_all_reports()
    return jsonify(reports)

if __name__ == '__main__':
    app.run(debug=True)