import os
import resend
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from model import get_db
from config import Config
from functools import wraps

contact_bp = Blueprint('contact', __name__)

resend.api_key = os.getenv('RESEND_API_KEY') or Config.RESEND_API_KEY


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated


@contact_bp.route('/api/contact', methods=['POST'])
def send_contact():
    try:
        data = request.get_json(silent=True) or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', 'Pesan dari Portofolio').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return jsonify({'success': False, 'message': 'Nama, email, dan pesan wajib diisi'}), 400

        print(f"📧 Saving contact from {name} ({email})")

        # Save to database
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO contacts (name, email, subject, message)
                    VALUES (%s, %s, %s, %s)
                """, (name, email, subject, message))
            conn.commit()  # Commit setelah insert
            print(f"✅ Contact saved to database")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

        # Send email via Resend (optional - doesn't fail if missing)
        try:
            if Config.RESEND_API_KEY and Config.RESEND_TO_EMAIL:
                resend.Emails.send({
                    "from": Config.RESEND_FROM_EMAIL,
                    "to": Config.RESEND_TO_EMAIL,
                    "subject": f"[Portofolio] {subject} - dari {name}",
                    "html": f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                        <h2 style="color: #7c6f9f; border-bottom: 2px solid #e8e4f0; padding-bottom: 10px;">
                            📬 Pesan Baru dari Portofolio
                        </h2>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr><td style="padding: 8px; color: #666; width: 100px;"><strong>Nama</strong></td><td style="padding: 8px;">{name}</td></tr>
                            <tr><td style="padding: 8px; color: #666;"><strong>Email</strong></td><td style="padding: 8px;">{email}</td></tr>
                            <tr><td style="padding: 8px; color: #666;"><strong>Subjek</strong></td><td style="padding: 8px;">{subject}</td></tr>
                        </table>
                        <div style="margin-top: 16px; padding: 16px; background: #fff; border-radius: 8px; border-left: 4px solid #b8a9d4;">
                            <strong style="color: #666;">Pesan:</strong>
                            <p style="margin-top: 8px; color: #333; line-height: 1.6;">{message}</p>
                        </div>
                    </div>
                    """
                })
                print(f"✅ Email sent via Resend")
        except Exception as e:
            print(f"⚠️  Email send error (non-critical): {e}")
            # Don't fail the request if email fails

        return jsonify({'success': True, 'message': 'Pesan berhasil dikirim!'})
    except Exception as e:
        print(f"❌ Error in send_contact: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


# Admin: view contacts
@contact_bp.route('/admin/contacts')
@login_required
def contacts_page():
    try:
        return render_template('admin/contacts.html')
    except Exception as e:
        print(f"❌ Error in contacts_page: {e}")
        return {"error": str(e)}, 500


@contact_bp.route('/api/admin/contacts', methods=['GET'])
@login_required
def get_contacts():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM contacts ORDER BY created_at DESC")
                data = cur.fetchall()
                # Mark all as read
                cur.execute("UPDATE contacts SET is_read = 1")
            conn.commit()  # Commit setelah update
            print(f"✅ Contacts fetched: {len(data)} records")
            return jsonify({'success': True, 'data': data if data else []})
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in get_contacts: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e), 'data': []}), 500


@contact_bp.route('/api/admin/contacts/<int:cid>', methods=['DELETE'])
@login_required
def delete_contact(cid):
    try:
        print(f"🗑️  Deleting contact {cid}")
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contacts WHERE id=%s", (cid,))
            conn.commit()  # Commit setelah delete
            print(f"✅ Contact deleted")
            return jsonify({'success': True, 'message': 'Pesan berhasil dihapus'})
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error in delete_contact: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
