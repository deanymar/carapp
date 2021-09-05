select * from Person
select * from MyCarInfo
select * from checks

delete MyCarInfo
delete Person
delete checks


select licPlate from MyCarInfo where ID like '302361282'

INSERT INTO checks(insurancePDf,licPlate) VALUES (001111,123456)
INSERT INTO checks(car_registrationPDF) VALUES (123456)

select car_registrationPDF from checks 

UPDATE checks SET car_registrationPDF =? WHERE licPlate=?



select myFile from checks where licPlate like 123456


