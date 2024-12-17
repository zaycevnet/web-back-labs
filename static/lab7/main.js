function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function(data) {
        return data.json(); // Преобразуем ответ сервера из JSON-формата в объект JavaScript
    })
    .then(function(films){
        let tbody = document.getElementById('film-list'); // Получаем ссылку на элемент <tbody> таблицы, в котором будет отображен список
        tbody.innerHTML = ''; // Очищаем таблицу перед добавлением новых данных
        
        // Перебираем массив фильмов
        for (let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr'); // Создаем новую строку таблицы для текущего фильма
            let tdTitle = document.createElement('td'); // Создаем ячейку для оригинального названия
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            // Меняем местами и выделяем оригинальное название
            tdTitle.innerHTML = `<i>(${films[i].title})</i>`; // Устанавливаем текст оригинального названия в курсиве и в скобках
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;
            
            // Создаем кнопку "редактировать" и настраиваем её действие
            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function () {
                editFilm(i);
            };

            // Создаем кнопку "удалить" и настраиваем её действие
            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };

            // Добавляем кнопки в ячейку действий
            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus); // Русское название первым
            tr.append(tdTitle);   // Оригинальное название вторым
            tr.append(tdYear);
            tr.append(tdActions);
            tbody.append(tr);
        }
    });
}
function deleteFilm(id,title) {
    if (! confirm(`Вы точно желаете удалить фильм "${title}"?`))
        return;
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function(){
            fillFilmList();
        });
}
function showModal() {
    // Находим элемент с классом 'modal' на странице
    // и устанавливаем его стиль display в 'block', чтобы сделать его видимым.
    document.querySelector('div.modal').style.display = 'block';
}
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}
function cancel() {
    hideModal(); // Вызывает функцию hideModal(), чтобы закрыть модальное окно.
}
function addFilm() {
    document.getElementById('id').value = '';// Очищаем скрытое поле 'id', чтобы указать, что добавляется новый фильм. в отличие от редактирования существующего
    document.getElementById('title').value = '';// Очищаем поле для оригинального названия фильма.
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal(); // Это открывает форму для ввода нового фильма.
}
function sendFilm() {
    // Получаем значение поля 'id'. Если оно пустое, значит добавляется новый фильм.
    const id = document.getElementById('id').value;
    const film = { // Собираем данные фильма из полей формы в объект.
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }
    const url = `/lab7/rest-api/films/${id}`; // Формируем URL для запроса. Если ID отсутствует, URL указывает на создание нового фильма.
    const method = id === '' ? 'POST' : 'PUT'; // Определяем метод запроса: если ID пустое, то используется 'POST' (добавление),
    // иначе 'PUT' (обновление существующего фильма).
    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"}, // Указываем, что данные передаются в формате JSON
        body: JSON.stringify(film) // Преобразуем объект фильма в строку JSON для отправки
    })
    
    .then(function(resp) {
        if (resp.ok) { // Если запрос успешен, обновляем список фильмов и закрываем модальное окно.
        fillFilmList();
        hideModal();
        return {}; // Возвращаем пустой объект для последующей обработки.
        }
        return resp.json(); // Если произошла ошибка, преобразуем ответ сервера в JSON для анализа.
    })
    .then(function(errors) {
        if(errors.description) // Если сервер вернул ошибку валидации для описания, отображаем сообщение об ошибке.
            document.getElementById('description-error').innerHTML = errors.description;
    });

}

function editFilm(id) {
    fetch (`/lab7/rest-api/films/${id}`)
    .then (function(data) {
        return data.json(); // Преобразуем ответ от сервера из JSON-формата в объект JavaScript
    })
    .then(function (film) { // Устанавливаем полученный ID фильма в скрытое поле формы. Это используется для определения, что мы редактируем существующий фильм.
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal(); // Показываем модальное окно с заполненной формой для редактирования
    }
)
}