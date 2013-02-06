Bearded Ironman
===============

Design
------

###Data aquisition

Data will be aquired using a set of sensors connected to an Arduino Uno R3.Arduino's are a wonderful choice because they're 

* very cheap 
* pretty damn stable 
* have super well supported frameworks and libraries 
* let us change the electronics super easily
* have all of the inputs and outputs we need. 
* 
We'll use the Firmata standard library to handle communicating between the arduino and the python program running on the Raspberry Pi. Data will be transmitted over the USB cord attached to the Arduino and plugged into the raspberry Pi. 

It is conceivable that at some point we could remove the arduino layer and have the inputs go directly to the Pi, but having the arduino handle this makes the system a lot more resiliant. Also, we can attach a small LCD screen to the arduino to make accessing data at the reactor easy if something goes wrong with the Pi.


###Data Persistence

For Data Persistence we'll use a database called PostgresSQL. It's the rare combination of "Industry Standard" and "Best option at the moment"

Writing to/from the database inside python uses the SQLAlchemy library. 
	
A Heroku Postgres Cloud database will be used for backup to ensure that the whole project isn't tied onto one SD card. This uses the Postgres "Follower Database" technology which ensures that there is an updated identical database that "follows" the local db. This is a low setup master-slave configuration that should be easy to configure. 
