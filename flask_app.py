from flask import Flask, render_template, request, make_response
app = Flask(__name__)

# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

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

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    recipes = Recipe.query.all()
    recipe_list = []

    for recipe in recipes:
        recipe_dict = {
            'id': recipe.id,
            'title': recipe.title,
            'cooking_minutes': recipe.cooking_minutes,
            'ingredient_explanation': recipe.ingredient_explanation,
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
        'likes': recipe.likes
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
        data = request.get_json(silent=True)

        title = data.get('title')
        difficulty = int(data.get('difficulty'))
        password = data.get('password')
        cooking_minutes = int(data.get('cookingMinutes'))
        cooking_explanation = data.get('cookingExplanation')
        ingredient_price = int(data.get('ingredientPrice'))
        ingredient_explanation = data.get('ingredientExplanation')
        caution = data.get('caution')

        recipe = Recipe(
            title = title,
            difficulty = difficulty,
            cooking_minutes = cooking_minutes,
            cooking_explanation = cooking_explanation,
            ingredient_price = ingredient_price,
            ingredient_explanation = ingredient_explanation,
            caution = caution,
            password = password,
            likes = 0
        )

        db.session.add(recipe)
        db.session.commit()

        return make_response({'success': True, 'message': '요청에 성공했습니다.'})

# 레시피 수정 API
@app.route('/api/recipes/<int:id>', methods=['PUT'])
def edit_recipe_api(id):
    if request.method == 'PUT':
        recipe = Recipe.query.filter_by(id=id).first()

        data = request.get_json(silent=True)
        password = data.get('password')

        print(recipe.password, password)

        if recipe.password != password:
            return make_response({'success': False, 'message': '요청에 실패했습니다.'})
        
        title = data.get('title')
        difficulty = int(data.get('difficulty'))
        password = data.get('password')
        cooking_minutes = int(data.get('cookingMinutes'))
        cooking_explanation = data.get('cookingExplanation')
        ingredient_price = int(data.get('ingredientPrice'))
        ingredient_explanation = data.get('ingredientExplanation')
        caution = data.get('caution')

        recipe.title = title
        recipe.difficulty = difficulty
        recipe.cooking_minutes = cooking_minutes
        recipe.cooking_explanation = cooking_explanation
        recipe.ingredient_price = ingredient_price
        recipe.ingredient_explanation = ingredient_explanation
        recipe.caution = caution

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