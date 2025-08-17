# Schéma MySQL (proposé) — KhanelConcept

## Tables

### villas
- id (varchar 36, PK)
- name (varchar 255)
- location (varchar 255)
- price (decimal(10,2))
- guests (int)
- guests_detail (varchar 255)
- features (text)
- category (varchar 64)
- image (varchar 512)
- description (text)
- status (varchar 32) default 'active'
- created_at (datetime) default current_timestamp

### images
- id (varchar 36, PK)
- villa_id (varchar 36, FK -> villas.id)
- src (varchar 512)
- alt (varchar 255)
- position (int)
- created_at (datetime) default current_timestamp

### reservations
- id (varchar 36, PK)
- villa_id (varchar 36, FK -> villas.id)
- user_id (varchar 36, FK -> users.id)
- checkin_date (date)
- checkout_date (date)
- guests_count (int)
- total_price (decimal(10,2))
- status (varchar 32) -- pending|confirmed|cancelled
- created_at (datetime) default current_timestamp

### users
- id (varchar 36, PK)
- email (varchar 255, unique)
- password_hash (varchar 255)
- first_name (varchar 100)
- last_name (varchar 100)
- phone (varchar 32)
- created_at (datetime) default current_timestamp

### settings
- id (varchar 36, PK)
- key (varchar 100, unique)
- value (text)
- updated_at (datetime) default current_timestamp on update current_timestamp

## Index
- IDX_villas_category (category)
- IDX_images_villa (villa_id)
- IDX_reservations_villa (villa_id), IDX_reservations_user (user_id)
- IDX_users_email (email unique)
- IDX_settings_key (key unique)
