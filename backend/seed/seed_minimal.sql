-- Minimal seed SQL
BEGIN;
INSERT INTO villas (id,name,location,price,guests,guests_detail,features,category,image,status) VALUES ('1','Villa F5 Ste Anne','Sainte-Anne',1300,10,'10 personnes','Piscine, wifi','sejour','assets/images/Villa_F5_Ste_Anne/01_piscine_principale.jpg','active');
INSERT INTO images (id,villa_id,src,alt,position) VALUES ('3b880dd6-5681-4aa1-88ad-9855b737d60c','1','assets/images/Villa_F5_Ste_Anne/01_piscine_principale.jpg','Image 1 — Villa F5 Ste Anne',1);
INSERT INTO villas (id,name,location,price,guests,guests_detail,features,category,image,status) VALUES ('2','Villa F6 Lamentin','Lamentin',1500,10,'10 personnes','Piscine, clim','sejour','assets/images/Villa_F6_Lamentin/01_piscine_jacuzzi_vue_ensemble.jpg','active');
INSERT INTO images (id,villa_id,src,alt,position) VALUES ('cb3123b6-bade-4519-9baa-8060ba7bc7c0','2','assets/images/Villa_F6_Lamentin/01_piscine_jacuzzi_vue_ensemble.jpg','Image 1 — Villa F6 Lamentin',1);
INSERT INTO settings (id,`key`,`value`) VALUES ('da42deeb-7399-416e-b7b8-11d0da729fad','site_name','KhanelConcept');
INSERT INTO settings (id,`key`,`value`) VALUES ('8879b64d-9c35-4b4f-b604-d36631c820de','currency','EUR');
INSERT INTO settings (id,`key`,`value`) VALUES ('15df25aa-4aef-4f00-84c8-4c8a297ccc2b','locale','fr-FR');
INSERT INTO settings (id,`key`,`value`) VALUES ('3c667f93-abe5-425d-979c-357e3f4f71ee','contact_phone','+596696123456');
INSERT INTO reservations (id,villa_id,user_id,checkin_date,checkout_date,guests_count,total_price,status) VALUES ('r1','1','','2025-09-01','2025-09-07',4,5200,'pending');
COMMIT;