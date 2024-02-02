# 🍳 항해 요리사(8조)

- 자신이 알고 있는 맛있는 요리의 레시피를 자랑하고 공유해보세요!
- 배포 주소: http://openmpy.pythonanywhere.com/

## 📚 스택

- Python
- Flask
- SQL3Lite
- SQLAlchemy
- Pythonanywhere
- Html, Css, Javascript

## 🔧 기능

- 레시피 전체 목록/개수 보기
- 레시피 상세보기
- 레시피 작성하기(이미지 업로드)
- 레시피 수정하기
- 레시피 삭제하기
- 레시피 좋아요 누르기

## 🖼️ ERD

<img width="360" alt="스크린샷 2024-02-02 오후 5 27 25" src="https://github.com/miniprojectinyoung/project/assets/150704638/b31031f4-7364-4be3-b292-b4aecb17b3a3">

## 📄 API 명세서

<details>
<summary>더보기</summary>

### 전체 조회

`GET` 요청을 사용해서 레시피를 전체 조회할 수 있습니다.

#### Response fields

| Path                    | Type      | Description      |
| ----------------------- | --------- | ---------------- |
| `total`                 | `Integer` | 레시피 전체 개수 |
| `id`                    | `Integer` | 아이디           |
| `title`                 | `String`  | 레시피 제목      |
| `cookingMinutes`        | `Integer` | 예상 조리 시간   |
| `cookingExplanation`    | `String`  | 요리 설명        |
| `ingredientExplanation` | `String`  | 재료 설명        |
| `imageUrl`              | `String`  | 이미지 URL       |
| `likes`                 | `Integer` | 좋아요 수        |

#### Example response

```http request
{
    "total": 2,
    "recipes": [
        {
            "id": 1
            "title": "토마토 바질파스타",
            "cookingMinute": 60,
            "ingredientExplanation": "파스타면, 토마토 500g, 바질페스토",
            "imageUrl": "test.png",
            "likes": 3
        },
        {
            "id": 2
            "title": "감자 파스타",
            "cookingMinute": 45,
            "ingredientExplanation": "파스타면, 감자 500g, 바질페스토",
            "imageUrl": "test2.png",
            "likes": 3
        }
    ]
}
```

### 조회

`GET` 요청을 사용해서 레시피를 조회할 수 있습니다.

#### Response fields

| Path                    | Type      | Description    |
| ----------------------- | --------- | -------------- |
| `id`                    | `Integer` | 아이디         |
| `title`                 | `String`  | 레시피 제목    |
| `difficulty`            | `Integer` | 난이도         |
| `cookingMinutes`        | `Integer` | 예상 조리 시간 |
| `cookingExplanation`    | `String`  | 요리 설명      |
| `ingredientPrice`       | `Integer` | 예상 재료 비용 |
| `ingredientExplanation` | `String`  | 재료 설명      |
| `caution`               | `String`  | 주의점         |
| `likes`                 | `Integer` | 좋아요 수      |
| `imageUrl`              | `String`  | 이미지 URL     |
| `recipeExplanation`     | `String`  | 레시피 설명    |

#### Example response

```http request
{
    "id": 1
    "title": "토마토 바질파스타",
    "difficulty": 3,
    "cookingMinutes": 60,
    "cookingExplanation": "제가 밭에서 직접 기른 토마토로 토마토 바질 파스타를 만들어보았어요!",
    "ingredientPrice": 27000,
    "ingredientExplanation": "파스타면, 토마토 500g, 바질페스토",
    "caution": "불 사용할때 주의해주세요!",
    "likes": 100,
    "imageUrl": "test.png",
    "recipeExplanation": "1. 토마토를 썰어줍니다."
}
```

### 등록

`POST` 요청을 사용해서 새 레시피를 등록할 수 있습니다.

#### Request fields

| Path                    | Type      | Description    |
| ----------------------- | --------- | -------------- |
| `title`                 | `String`  | 레시피 제목    |
| `difficulty`            | `Integer` | 난이도         |
| `password`              | `String`  | 비밀번호       |
| `cookingMinutes`        | `Integer` | 예상 조리 시간 |
| `cookingExplanation`    | `String`  | 요리 설명      |
| `ingredientPrice`       | `Integer` | 예상 재료 비용 |
| `ingredientExplanation` | `String`  | 재료 설명      |
| `caution`               | `String`  | 주의점         |
| `image`                 | `String`  | 이미지         |
| `recipeExplanation`     | `String`  | 레시피 설명    |

#### Example request

```http request
POST /api/recipes

{
    "title": "토마토 바질파스타",
    "difficulty": 3,
    "password": "1234",
    "cookingMinutes": 60,
    "cookingExplanation": "제가 밭에서 직접 기른 토마토로 토마토 바질 파스타를 만들어보았어요!",
    "ingredientPrice": 27000,
    "ingredientExplanation": "파스타면, 토마토 500g, 바질페스토",
    "caution": "불 사용할때 주의해주세요!",
    "image": "이미지",
    "recipeExplanation": "1. 토마토를 썰어줍니다."
}
```

#### Response fields

| Path      | Type      | Description |
| --------- | --------- | ----------- |
| `success` | `Boolean` | 성공/실패   |
| `message` | `String`  | 반환 내용   |

#### Example response

```http request
{
    "success": true,
    "message": "요청에 성공했습니다."
}
```

### 수정

`PUT` 요청을 사용해서 레시피를 수정할 수 있습니다.

#### Request fields

| Path                    | Type      | Description    |
| ----------------------- | --------- | -------------- |
| `title`                 | `String`  | 레시피 제목    |
| `difficulty`            | `Integer` | 난이도         |
| `password`              | `String`  | 비밀번호       |
| `cookingMinutes`        | `Integer` | 예상 조리 시간 |
| `cookingExplanation`    | `String`  | 요리 설명      |
| `ingredientPrice`       | `Integer` | 예상 재료 비용 |
| `ingredientExplanation` | `String`  | 재료 설명      |
| `caution`               | `String`  | 주의점         |
| `image`                 | `String`  | 이미지         |
| `recipeExplanation`     | `String`  | 레시피 설명    |

#### Example request

```http request
PUT /api/recipes/{id}

{
    "title": "토마토 바질파스타",
    "difficulty": 3,
    "password": "1234",
    "cookingMinutes": 60,
    "cookingExplanation": "제가 밭에서 직접 기른 토마토로 토마토 바질 파스타를 만들어보았어요!",
    "ingredientPrice": 27000,
    "ingredientExplanation": "파스타면, 토마토 500g, 바질페스토",
    "caution": "불 사용할때 주의해주세요!",
    "image": "이미지",
    "recipeExplanation": "1. 토마토를 썰어줍니다."
}
```

#### Response fields

| Path      | Type      | Description |
| --------- | --------- | ----------- |
| `success` | `Boolean` | 성공/실패   |
| `message` | `String`  | 반환 내용   |

#### Example response

```http request
{
    "success": true,
    "message": "요청에 성공했습니다."
}
```

### 삭제

`DELETE` 요청을 사용해서 레시피를 삭제할 수 있습니다.

#### Request fields

| Path       | Type     | Description |
| ---------- | -------- | ----------- |
| `password` | `String` | 비밀번호    |

#### Example request

```http request
DELETE /api/recipes/{id}

{
    "password": "1234"
}
```

#### Response fields

| Path      | Type      | Description |
| --------- | --------- | ----------- |
| `success` | `Boolean` | 반환 유무   |
| `message` | `String`  | 반환 내용   |

#### Example response

```http request
{
    "success": true,
    "message": "요청에 성공했습Ï니다."
}
```

### 좋아요

`POST` 요청을 사용해서 레시피를 좋아요할 수 있습니다.

#### Example request

```http request
POST /api/recipes/{id}/likes
```

#### Example response

```http request
"OK"
```

</details>

## 👥 조원

- 황인영(https://github.com/inyoungfriend) ⭐
- 유하정(https://github.com/yuha00e)
- 윤형식(https://github.com/nyeongsik13)
- 김수환(https://github.com/openmpy)
