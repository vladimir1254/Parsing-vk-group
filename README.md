## Парсинг комментариев из VK группы

Этот скрипт позволяет осуществлять парсинг комментариев из группы ВКонтакте, используя VK API. Для работы скрипта потребуется установить необходимые библиотеки, указанные в файле `requirements.txt`.

### Использование

1. **Установка зависимостей:**
   - Убедитесь, что у вас установлен Python на вашем компьютере.
   - Установите необходимые библиотеки с помощью команды:

     ```bash
     pip install -r requirements.txt
     ```

2. **Конфигурация:**
   - Откройте файл `config.json` и предоставьте необходимую информацию (API ключ, ID группы и т. д.).

3. **Запуск скрипта:**
   - Выполните следующую команду в вашем терминале:

     ```bash
     python pars_vk.py
     ```

4. **Результат:**
   Скрипт создает директорию all_people структура следующая:
```
all_people:
  id_people:
   id_group:
     posts
       all_posts.txt
       all_posts.json
     comments
       all_comments.txt
       all_comments.json
```
JSON сохраняется на случай если потребуется посмотреть более детальное содержание поста, если он содержал видео/фото, по json'у можно будет это также отследить.
Комментарии админа группы сохраняются как idADMIN-<id группы>

