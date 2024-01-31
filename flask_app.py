from flask import Flask, render_template, request, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)

import os
import uuid

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

# 이미지 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = basedir + '/static/upload'
app.config['MAX_UPLOAD_SIZE'] = 5 * 1024 * 1024 # 5MB

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    cooking_minutes = db.Column(db.Integer, nullable=False)
    cooking_explanation = db.Column(db.String(1000), nullable=False)
    ingredient_price = db.Column(db.Integer, nullable=False)
    ingredient_explanation = db.Column(db.String(1000), nullable=False)
    caution = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    recipes = Recipe.query.order_by(Recipe.id.desc()).all()
    recipe_list = []

    for recipe in recipes:
        recipe_dict = {
            'id': recipe.id,
            'title': recipe.title,
            'cooking_minutes': recipe.cooking_minutes,
            'ingredient_explanation': recipe.ingredient_explanation,
            'image_url': recipe.image_url,
            'likes': recipe.likes
        }
        recipe_list.append(recipe_dict)

    result = {
        'total': len(recipes),
        'recipes': recipe_list
    }

    return render_template('index.html', data=result)

@app.route('/commiting')
def commiting():
    return render_template('commiting.html')

# 레시피 조회
@app.route('/recipes/<int:id>')
def recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()

    result = {
        'id': recipe.id,
        'title': recipe.title,
        'difficulty': recipe.difficulty,
        'cooking_minutes': recipe.cooking_minutes,
        'cooking_explanation': recipe.cooking_explanation,
        'ingredient_price': recipe.ingredient_price,
        'ingredient_explanation': recipe.ingredient_explanation,
        'caution': recipe.caution,
        'likes': recipe.likes,
        'image_url': recipe.image_url
    }
    return render_template('recipe.html', data=result)

# 레시피 수정
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()

    result = {
        'id': recipe.id,
        'title': recipe.title,
        'difficulty': recipe.difficulty,
        'cooking_minutes': recipe.cooking_minutes,
        'cooking_explanation': recipe.cooking_explanation,
        'ingredient_price': recipe.ingredient_price,
        'ingredient_explanation': recipe.ingredient_explanation,
        'caution': recipe.caution
    }
    return render_template('edit.html', data=result)

# 레시피 작성 API
@app.route('/api/recipes', methods=['POST'])
def create_recipe_api():
    if request.method == 'POST':
        title = request.form.get('title')
        difficulty = int(request.form.get('difficulty'))
        password = request.form.get('password')
        cooking_minutes = int(request.form.get('cookingMinutes'))
        cooking_explanation = request.form.get('cookingExplanation')
        ingredient_price = int(request.form.get('ingredientPrice'))
        ingredient_explanation = request.form.get('ingredientExplanation')
        caution = request.form.get('caution')

        # 이미지 업로드
        file = request.files['recipeImage']
        if file and (allowed_file(file.content_type) is False or file.content_length > app.config['MAX_UPLOAD_SIZE']):
            return make_response({'success': False, 'message': '요청에 실패했습니다.'})
        
        extension = file.content_type.split('/')[1].lower()
        filename = str(uuid.uuid4()) + '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        recipe = Recipe(
            title = title,
            difficulty = difficulty,
            cooking_minutes = cooking_minutes,
            cooking_explanation = cooking_explanation,
            ingredient_price = ingredient_price,
            ingredient_explanation = ingredient_explanation,
            caution = caution,
            password = password,
            likes = 0,
            image_url = filename
        )

        db.session.add(recipe)
        db.session.commit()

        return make_response({'success': True, 'message': '요청에 성공했습니다.'})

# 이미지 확장자 검사
def allowed_file(content_type):
    return content_type.split('/')[1].lower() in ALLOWED_EXTENSIONS

# 레시피 수정 API
@app.route('/api/recipes/<int:id>', methods=['PUT'])
def edit_recipe_api(id):
    if request.method == 'PUT':
        recipe = Recipe.query.filter_by(id=id).first()

        password = request.form.get('password')

        if recipe.password != password:
            return make_response({'success': False, 'message': '요청에 실패했습니다.'})
        
        title = request.form.get('title')
        difficulty = int(request.form.get('difficulty'))
        password = request.form.get('password')
        cooking_minutes = int(request.form.get('cookingMinutes'))
        cooking_explanation = request.form.get('cookingExplanation')
        ingredient_price = int(request.form.get('ingredientPrice'))
        ingredient_explanation = request.form.get('ingredientExplanation')
        caution = request.form.get('caution')

        recipe.title = title
        recipe.difficulty = difficulty
        recipe.cooking_minutes = cooking_minutes
        recipe.cooking_explanation = cooking_explanation
        recipe.ingredient_price = ingredient_price
        recipe.ingredient_explanation = ingredient_explanation
        recipe.caution = caution

        # 이미지 업로드
        if 'recipeImage' in request.files:
            file = request.files['recipeImage']

            if file and (allowed_file(file.content_type) is False or file.content_length > app.config['MAX_UPLOAD_SIZE']):
                return make_response({'success': False, 'message': '요청에 실패했습니다.'})
            
            extension = file.content_type.split('/')[1].lower()
            filename = str(uuid.uuid4()) + '.' + extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            recipe.image_url = filename

        db.session.add(recipe)
        db.session.commit()

    return make_response({'success': True, 'message': '요청에 성공했습니다.'})

# 레시피 삭제 API
@app.route('/api/recipes/<int:id>', methods=['DELETE'])
def delete_recipe_api(id):
    if request.method == 'DELETE':
        recipe = Recipe.query.filter_by(id=id).first()

        data = request.get_json(silent=True)
        password = data.get('password')

        print(recipe.password, password)

        if recipe.password != password:
            return make_response({'success': False, 'message': '요청에 실패했습니다.'})

        db.session.delete(recipe)
        db.session.commit()

    return make_response({'success': True, 'message': '요청에 성공했습니다.'})

# 레시피 좋아요 API
@app.route('/api/recipes/<int:id>/likes', methods=['PUT'])
def likes_api(id):
    recipe = Recipe.query.filter_by(id=id).first()

    recipe.likes += 1;

    db.session.add(recipe)
    db.session.commit()

    return make_response({'success': True, 'message': '요청에 성공했습니다.'})

if __name__ == '__main__':
    app.run(debug=True)