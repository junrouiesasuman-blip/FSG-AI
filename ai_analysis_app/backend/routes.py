from functools import wraps

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import desc

from .extensions import bcrypt, db
from .model_service import FEATURE_META, get_feature_names, predict
from .models import AnalysisHistory, User

bp = Blueprint('main', __name__, template_folder='../frontend/templates', static_folder='../frontend/static')


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            if request.path.startswith('/api/'):
                return jsonify({'ok': False, 'message': 'Authentication required.'}), 401
            return redirect(url_for('main.login_page'))
        return view(*args, **kwargs)
    return wrapped


@bp.get('/')
def landing_page():
    return render_template('index.html')


@bp.get('/login')
def login_page():
    if session.get('user_id'):
        return redirect(url_for('main.dashboard_page'))
    return render_template('login.html')


@bp.get('/signup')
def signup_page():
    if session.get('user_id'):
        return redirect(url_for('main.dashboard_page'))
    return render_template('signup.html')


@bp.get('/dashboard')
@login_required
def dashboard_page():
    features = get_feature_names(current_app.config['MODEL_PATH'])
    return render_template('dashboard.html', features=features, feature_meta=FEATURE_META)


@bp.get('/history')
@login_required
def history_page():
    return render_template('history.html')


@bp.post('/api/auth/signup')
def signup():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not name or not email or len(password) < 6:
        return jsonify({'ok': False, 'message': 'Name, valid email, and 6+ character password are required.'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'ok': False, 'message': 'An account with this email already exists.'}), 409

    user = User(name=name, email=email, password_hash=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'ok': True, 'message': 'Account successfully created. Redirecting to login...'})


@bp.post('/api/auth/login')
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'ok': False, 'message': 'Invalid email or password.'}), 401

    session['user_id'] = user.id
    session['user_name'] = user.name
    return jsonify({'ok': True, 'message': 'Login successful.', 'user': {'name': user.name, 'email': user.email}})


@bp.post('/api/auth/logout')
def logout():
    session.clear()
    return jsonify({'ok': True, 'message': 'Logged out.'})


@bp.get('/api/me')
def me():
    if not session.get('user_id'):
        return jsonify({'ok': False, 'authenticated': False})
    return jsonify({'ok': True, 'authenticated': True, 'name': session.get('user_name')})


@bp.get('/api/features')
@login_required
def features():
    names = get_feature_names(current_app.config['MODEL_PATH'])
    return jsonify({'ok': True, 'features': [{'name': item, 'hint': FEATURE_META.get(item, 'Model feature')} for item in names]})


@bp.post('/api/analyze')
@login_required
def analyze():
    data = request.get_json(silent=True) or {}
    result, status = predict(data, current_app.config['MODEL_PATH'])
    if not result.get('ok'):
        return jsonify(result), status

    record = AnalysisHistory(
        user_id=session['user_id'],
        input_data=result['input_data'],
        prediction=result['prediction'],
        confidence=result.get('confidence'),
        probabilities=result.get('probabilities')
    )
    db.session.add(record)
    db.session.commit()
    result['history_id'] = record.id
    return jsonify(result), status


@bp.get('/api/history')
@login_required
def history():
    rows = (AnalysisHistory.query
            .filter_by(user_id=session['user_id'])
            .order_by(desc(AnalysisHistory.created_at))
            .limit(50)
            .all())
    return jsonify({
        'ok': True,
        'history': [
            {
                'id': row.id,
                'prediction': row.prediction,
                'confidence': row.confidence,
                'probabilities': row.probabilities,
                'input_data': row.input_data,
                'created_at': row.created_at.isoformat(),
            } for row in rows
        ]
    })


@bp.delete('/api/history/<int:item_id>')
@login_required
def delete_history(item_id):
    row = AnalysisHistory.query.filter_by(id=item_id, user_id=session['user_id']).first_or_404()
    db.session.delete(row)
    db.session.commit()
    return jsonify({'ok': True, 'message': 'History item deleted.'})
