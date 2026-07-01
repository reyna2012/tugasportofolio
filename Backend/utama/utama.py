from flask import Blueprint, render_template, jsonify
from model import get_db
import traceback

utama_bp = Blueprint('utama', __name__)


@utama_bp.route('/health')
def health():
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        conn.close()
        print("✅ Database health check passed")
        return jsonify({'success': True, 'status': 'ok', 'database': 'connected'})
    except Exception as e:
        print(f"❌ Health check error: {e}")
        traceback.print_exc()
        return jsonify({'success': True, 'status': 'ok', 'database': f'disconnected: {str(e)}'}), 200


@utama_bp.route('/api/profile')
def api_profile():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM profiles ORDER BY id DESC LIMIT 1")
                profile = cur.fetchone()
            if profile:
                print(f"✅ Profile loaded: {profile.get('name', 'Unknown')}")
                return jsonify({'success': True, 'data': profile})
            else:
                print("⚠️  No profile found in database - returning default")
                return jsonify({'success': True, 'data': {
                    'name': 'Portfolio',
                    'title': 'Web Developer',
                    'bio': 'Welcome to my portfolio',
                    'photo_url': None
                }})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error fetching profile: {e}")
        traceback.print_exc()
        return jsonify({'success': True, 'data': {
            'name': 'Portfolio',
            'title': 'Web Developer',
            'bio': 'Welcome to my portfolio',
            'photo_url': None
        }}), 200


@utama_bp.route('/api/skills')
def api_skills():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM skills ORDER BY category, level DESC")
                skills = cur.fetchall()
            count = len(skills) if skills else 0
            print(f"✅ Loaded {count} skills")
            return jsonify({'success': True, 'data': skills if skills else []})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error fetching skills: {e}")
        traceback.print_exc()
        return jsonify({'success': True, 'data': []}), 200


@utama_bp.route('/api/experiences')
def api_experiences():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM experiences ORDER BY is_current DESC, id DESC")
                exps = cur.fetchall()
            count = len(exps) if exps else 0
            print(f"✅ Loaded {count} experiences")
            return jsonify({'success': True, 'data': exps if exps else []})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error fetching experiences: {e}")
        traceback.print_exc()
        return jsonify({'success': True, 'data': []}), 200


@utama_bp.route('/api/projects')
def api_projects():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM projects ORDER BY is_featured DESC, id DESC")
                projects = cur.fetchall()
            count = len(projects) if projects else 0
            print(f"✅ Loaded {count} projects")
            return jsonify({'success': True, 'data': projects if projects else []})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error fetching projects: {e}")
        traceback.print_exc()
        return jsonify({'success': True, 'data': []}), 200
