-- Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
SELECT *
FROM tasks
WHERE user_id = 1;

-- Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
SELECT *
FROM tasks AS t
JOIN status AS s ON t.status_id = s.id
WHERE s.name = 'new';

-- Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
UPDATE tasks
SET status_id = (
    SELECT id
    FROM status
    WHERE name = 'in progress'
    )
WHERE id = (
    SELECT t.id
    FROM tasks AS t
    JOIN status AS s ON t.status_id = s.id
    WHERE s.name <> 'in progress'
    ORDER BY t.id
    LIMIT 1
    );

-- Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
SELECT *
FROM users
WHERE id NOT IN (
    SELECT user_id
    FROM tasks
);

-- Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task', 'New task description', 1, 1);

-- Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
SELECT *
FROM tasks AS t
JOIN status AS s ON t.status_id = s.id
WHERE s.name <> 'completed';

--Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
DELETE FROM tasks
WHERE id = 36;

-- Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
SELECT *
FROM users
WHERE email LIKE '%@example.net';

-- Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
UPDATE users
SET fullname = 'John Doe'
WHERE id = 1;

-- Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
SELECT s.name AS status_name, COUNT(t.id) AS task_count
FROM status AS s
JOIN tasks AS t ON s.id = t.status_id
GROUP BY s.name
ORDER BY task_count DESC;

-- Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').
SELECT t.title, t.description
FROM tasks AS t
JOIN users AS u ON t.user_id = u.id
WHERE u.email LIKE '%@example.net';

-- Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
SELECT *
FROM tasks
WHERE description IS NULL;

-- Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
SELECT u.fullname, t.title
FROM users AS u
JOIN tasks AS t ON u.id = t.user_id
JOIN status AS s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users AS u
LEFT JOIN tasks AS t ON u.id = t.user_id
GROUP BY u.fullname
ORDER BY task_count DESC;
