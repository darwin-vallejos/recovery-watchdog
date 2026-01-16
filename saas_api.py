"""
saas_api.py

REST API for SaaS Recovery Watchdog
"""

from flask import Flask, request, jsonify
from functools import wraps
from src.models import Database
from src.recovery.detector import RecoveryDebtDetector
from src.recovery.coherence import compute_coherence_from_pod_metrics, compute_stress_factor
import os


app = Flask(__name__)
db = Database()

# Initialize detector
detector = RecoveryDebtDetector(beta_base=1.1, c_baseline=0.6)


def require_api_key(f):
    """Decorator to require valid API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        org = db.verify_api_key(api_key)
        if not org:
            return jsonify({'error': 'Invalid API key'}), 403
        
        # Add organization to request context
        request.organization = org
        return f(*args, **kwargs)
    
    return decorated_function


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'service': 'Recovery Watchdog SaaS'
    })


@app.route('/api/v1/organizations', methods=['POST'])
def create_organization():
    """Create new organization (signup)"""
    data = request.json
    
    if not data.get('name'):
        return jsonify({'error': 'Organization name required'}), 400
    
    org = db.create_organization(
        name=data['name'],
        tier=data.get('tier', 'trial')
    )
    
    return jsonify({
        'organization': org,
        'message': 'Organization created successfully. Save your API key!'
    }), 201


@app.route('/api/v1/agents/register', methods=['POST'])
@require_api_key
def register_agent():
    """Register new monitoring agent"""
    data = request.json
    
    if not data.get('hostname'):
        return jsonify({'error': 'Hostname required'}), 400
    
    agent_id = db.register_agent(
        organization_id=request.organization['id'],
        hostname=data['hostname']
    )
    
    return jsonify({
        'agent_id': agent_id,
        'hostname': data['hostname'],
        'message': 'Agent registered successfully'
    }), 201


@app.route('/api/v1/metrics', methods=['POST'])
@require_api_key
def submit_metrics():
    """Submit metrics from agent"""
    data = request.json
    
    if not data.get('agent_id'):
        return jsonify({'error': 'Agent ID required'}), 400
    
    # Extract system metrics
    metrics = {
        'cpu_usage': data.get('cpu_usage', 0),
        'mem_usage': data.get('mem_usage', 0),
        'error_rate': data.get('error_rate', 0),
        'response_p95': data.get('response_p95', 100),
        'restart_count': data.get('restart_count', 0)
    }
    
    # Compute coherence and detection
    C = compute_coherence_from_pod_metrics(metrics)
    beta = compute_stress_factor(metrics)
    margin_result, alert_level = detector.update(C, beta)
    
    # Store in database
    db_metrics = {
        'coherence': C,
        'recovery_margin': margin_result.recovery_margin,
        'alert_level': alert_level,
        'cpu_usage': metrics['cpu_usage'],
        'mem_usage': metrics['mem_usage'],
        'error_rate': metrics['error_rate']
    }
    
    db.store_metrics(data['agent_id'], db_metrics)
    
    return jsonify({
        'coherence': C,
        'recovery_margin': margin_result.recovery_margin,
        'alert_level': alert_level,
        'message': 'Metrics processed successfully'
    })


@app.route('/api/v1/agents', methods=['GET'])
@require_api_key
def list_agents():
    """List all agents for organization"""
    agents = db.get_organization_agents(request.organization['id'])
    
    return jsonify({
        'organization': request.organization['name'],
        'agents': agents,
        'count': len(agents)
    })


@app.route('/api/v1/dashboard/<agent_id>', methods=['GET'])
@require_api_key
def get_dashboard_data(agent_id):
    """Get dashboard data for specific agent"""
    # TODO: Implement dashboard data retrieval
    return jsonify({
        'agent_id': agent_id,
        'message': 'Dashboard data endpoint (coming soon)'
    })


if __name__ == '__main__':
    import os
    
    # Initialize database
    db.init_db()
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("=" * 60)
    print("Recovery Watchdog SaaS API Starting")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print("=" * 60)
    print()
    
    # Run with production settings
    app.run(host=host, port=port, debug=False)