alter sequence item_category_id_seq restart with 1;
delete from item_category;
insert into item_category(name)
values
    ('Toys'),
    ('Vehicles'),
    ('Furniture'),
    ('Real-estate'),
    ('Electronics'),
    ('Clothes');


alter sequence item_items_id_seq restart with 1;
delete from item_items;
insert into item_items(name, item_picture, condition, long_description, category_id)
values
    ('New car', 'https://carsguide-res.cloudinary.com/image/upload/f_auto,fl_lossy,q_auto,t_cg_hero_large/v1/editorial/listicle/hero_image/2020-Bugatti%20Centodieci-1001x565-%282%29.jpg', 'great', 'Its a very nice car', 2),
    ('Old car', 'https://www.carcovers.com/media/carcover/resource/classiccar.jpg', 'not great', 'Its a bad car', 2),
    ('Doll', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIj6DJSxfo2V6wJ9jsXHUvOQOMqA7HAvcxnQ&usqp=CAU', 'Great', 'Its a doll', 1),
    ('TV', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Old_TV.jpg/2502px-Old_TV.jpg', 'Great', 'Its old but works amazingly', 5);


alter sequence catalogue_postings_id_seq restart with 1;
delete from catalogue_postings;
insert into catalogue_postings(open, creation_date, item_id_id)
values
    (True, '2022-04-05', 1),
    (False, '2022-01-15', 2),
    (True, '2022-01-01', 3),
    (True, '2021-03-07', 4);


alter sequence user_profile_userprofile_id_seq restart with 1;
delete from user_profile_userprofile;
insert into user_profile_userprofile(bio, profile_picture, user_id)
values
    ('I am the first user im so excited!', 'https://previews.123rf.com/images/kegfire/kegfire1902/kegfire190200128/117409190-excited-lady-showing-thumb-up-gesture.jpg', 1);


alter sequence catalogue_bids_id_seq restart with 1;
delete from catalogue_bids;
insert into catalogue_bids(price, accept, posting_id_id, user_id_id)
values
    (400, False, 1, 1),
    (200, False, 2, 1),
    (600, True, 3, 1),
    (16000, True, 1, 1),
    (2000, False, 4, 1);


alter sequence catalogue_ratings_id_seq restart with 1;
delete from catalogue_ratings;
insert into catalogue_ratings(rating, posting_id_id, user_id_id)
values
    (5, 2, 1),
    (2, 4, 1),
    (1, 1, 1);

select * from auth_user
select * from user_profile_userprofile