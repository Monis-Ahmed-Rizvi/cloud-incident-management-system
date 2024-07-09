from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import ChatLog
from app.forms import ChatForm
import openai

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = ChatForm()
    if form.validate_on_submit():
        user_message = form.message.data
        openai.api_key = current_app.config['OPENAI_API_KEY']
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        ai_message = response.choices[0].message['content'].strip()
        chat_log = ChatLog(user_id=current_user.id, user=current_user, message=user_message, response=ai_message)
        db.session.add(chat_log)
        db.session.commit()
        return jsonify({'message': ai_message})
    chat_logs = ChatLog.query.filter_by(user_id=current_user.id).order_by(ChatLog.timestamp.desc()).limit(10).all()
    return render_template('chat.html', form=form, chat_logs=chat_logs)

