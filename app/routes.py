from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, ListForm
from app.models import User, ItemList, Item


@app.route('/')
@app.route('/index')
@login_required
def index():
    lists = ItemList.query.filter_by(owner_id=current_user.id).all()
    return render_template('main_page.html', lists=lists)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/list/<int:list_id>')
@app.route('/list', methods=['GET', 'POST'])
def list(list_id=None):
    if list_id:
        obj = ItemList.query.filter_by(id=list_id).first()
        form = ListForm(obj=obj)
    else:
        form = ListForm()

    if form.add_item.data:
        form.items.append_entry()
        return render_template('list.html', form=form)
    
    if form.remove_item.data:
        form.items.pop_entry()
        return render_template('list.html', form=form)

    if form.validate_on_submit():
        if form.data['id'] != '':
            itemlist = ItemList.query.filter_by(id=int(form.data['id'])).first()
            itemlist.name = form.data['name']
        else:
            itemlist = ItemList(name=form.data['name'], owner_id=current_user.id)
        db.session.add(itemlist)
        db.session.commit()
        
        Item.query.filter_by(list_id=itemlist.id).delete()
        db.session.commit()
        
        for i in form.data['items']:
            item = Item(name=i['name'], quantity=i['quantity'], list_id=itemlist.id)
            db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('list.html', form=form)

@app.route('/list/<int:list_id>/delete', methods=['POST'])
def list_delete(list_id):
    if request.method == 'POST':
        obj = ItemList.query.filter_by(id=list_id).delete()
        db.session.commit()
        return redirect(url_for('index'))
