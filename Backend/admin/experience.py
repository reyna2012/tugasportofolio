from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from model import get_db
from functools import wraps

experience_bp = Blueprint('experience', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated


@experience_bp.route('/admin/experience')
@login_required
def experience_page():
    try:
        return render_template('admin/experience.html')
    except Exception as e:
        print(f"❌ Error in experience_page: {e}")
        return {"error": str(e)}, 500


@experience_bp.route('/api/admin/experiences', methods=['GET'])
@login_required
def get_experiences():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM experiences ORDER BY is_current DESC, id DESC")
                data = cur.fetchall()
            print(f"✅ Experiences fetched: {len(data)} records")
            return jsonify({'success': True, 'data': data if data else []})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in get_experiences: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e), 'data': []}), 500


@experience_bp.route('/api/admin/experiences', methods=['POST'])
@login_required
def create_experience():
    try:
        data = request.get_json(silent=True) or {}
        print(f"📝 Creating experience: {data.get('company')}")
        
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO experiences (company, position, start_date, end_date, is_current, description, logo_url)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (data.get('company'), data.get('position'), data.get('start_date'),
                      data.get('end_date'), data.get('is_current', 0), data.get('description'), data.get('logo_url')))
                conn.commit()  # Commit after insert
                cur.execute("SELECT * FROM experiences ORDER BY id DESC LIMIT 1")
                saved = cur.fetchone()
            print(f"✅ Experience created")
            return jsonify({'success': True, 'message': 'Pengalaman berhasil ditambahkan', 'data': saved})
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in create_experience: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@experience_bp.route('/api/admin/experiences/<int:eid>', methods=['PUT'])
@login_required
def update_experience(eid):
    try:
        data = request.get_json(silent=True) or {}
        print(f"📝 Updating experience {eid}")
        
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE experiences SET company=%s, position=%s, start_date=%s, end_date=%s,
                    is_current=%s, description=%s, logo_url=%s WHERE id=%s
                """, (data.get('company'), data.get('position'), data.get('start_date'),
                      data.get('end_date'), data.get('is_current', 0), data.get('description'),
                      data.get('logo_url'), eid))
            conn.commit()  # Commit after update
            print(f"✅ Experience updated")
            return jsonify({'success': True, 'message': 'Pengalaman berhasil diupdate'})
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in update_experience: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@experience_bp.route('/api/admin/experiences/<int:eid>', methods=['DELETE'])
@login_required
def delete_experience(eid):
    try:
        print(f"🗑️  Deleting experience {eid}")
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM experiences WHERE id=%s", (eid,))
            conn.commit()  # Commit after delete
            print(f"✅ Experience deleted")
            return jsonify({'success': True, 'message': 'Pengalaman berhasil dihapus'})
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in delete_experience: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
