"""
dashboard.py

Simple web dashboard for Recovery Watchdog
"""

from flask import Flask, render_template_string
import csv
from pathlib import Path
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Recovery Watchdog Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        .status-card {
            display: inline-block;
            padding: 20px 30px;
            margin: 10px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
        }
        .status-GREEN { background-color: #d4edda; color: #155724; }
        .status-YELLOW { background-color: #fff3cd; color: #856404; }
        .status-RED { background-color: #f8d7da; color: #721c24; }
        .metric {
            font-size: 24px;
            margin: 10px 0;
        }
        #chart {
            margin-top: 30px;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Recovery Watchdog Dashboard</h1>
        
        <div class="status-card status-{{ alert_level }}">
            Current Status: {{ alert_level }}
        </div>
        
        <div class="metric">
            <strong>Coherence (C):</strong> {{ "%.3f"|format(current_C) }}
        </div>
        
        <div class="metric">
            <strong>Recovery Margin:</strong> {{ "%.3f"|format(current_margin) }}
        </div>
        
        <div class="metric">
            <strong>Data Points:</strong> {{ data_count }}
        </div>
        
        <div id="chart"></div>
        
        <div class="footer">
            <p>Recovery Watchdog v0.1.0 | Monitoring since {{ first_timestamp }}</p>
            <p><a href="javascript:location.reload()">Refresh Dashboard</a></p>
        </div>
    </div>
    
    <script>
        var timestamps = {{ timestamps|tojson }};
        var coherence = {{ coherence|tojson }};
        var margins = {{ margins|tojson }};
        
        var trace1 = {
            x: timestamps,
            y: coherence,
            name: 'Coherence C',
            type: 'scatter',
            line: {color: 'blue', width: 2}
        };
        
        var trace2 = {
            x: timestamps,
            y: margins,
            name: 'Recovery Margin',
            type: 'scatter',
            yaxis: 'y2',
            line: {color: 'orange', width: 2}
        };
        
        var layout = {
            title: 'System Health Over Time',
            xaxis: {title: 'Time'},
            yaxis: {title: 'Coherence C'},
            yaxis2: {
                title: 'Recovery Margin',
                overlaying: 'y',
                side: 'right'
            },
            hovermode: 'x unified'
        };
        
        Plotly.newPlot('chart', [trace1, trace2], layout);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard view"""
    csv_file = Path("pilot.csv")
    
    if not csv_file.exists():
        return "No data yet. Run watchdog_monitor.py first.", 404
    
    # Read CSV data
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    if not data:
        return "No data yet. Run watchdog_monitor.py first.", 404
    
    # Extract current state
    current = data[-1]
    first = data[0]
    
    # Prepare data for chart (last 100 points)
    recent_data = data[-100:]
    
    timestamps = [row['timestamp'][:19] for row in recent_data]
    coherence = [float(row['coherence_C']) for row in recent_data]
    margins = [float(row['recovery_margin']) for row in recent_data]
    
    return render_template_string(
        HTML_TEMPLATE,
        alert_level=current['alert_level'],
        current_C=float(current['coherence_C']),
        current_margin=float(current['recovery_margin']),
        data_count=len(data),
        first_timestamp=first['timestamp'][:19],
        timestamps=timestamps,
        coherence=coherence,
        margins=margins
    )

if __name__ == '__main__':
    print("=" * 60)
    print("Recovery Watchdog Dashboard Starting...")
    print("=" * 60)
    print()
    print("Open your browser to: http://localhost:5000")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)