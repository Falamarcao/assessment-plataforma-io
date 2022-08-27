<br>
<br>
<img src="images/logo-plataforma.png" alt="drawing" width="400"/>

# Pre assessment: Plataforma.io | Backend Python

Job link: https://bit.ly/3JPhafa

## Prompt: 
In 2.5 hours we would like you to create a small backend API using Django. This API will be used to manage a small business that is focused on renting different rooms for events. 

## Rules: 
- There are N rooms with M capacity. **OK**
- There are two types of events: public and private. **OK**
- If the event is public, any customer can book a space. 
- If the event is private, no one else can book a space in the room. 
- A customer can book a space for an event, if the event is public and there is still space available. **1/2 OK (occupancy only)**
- A customer can cancel its booking and their space should be available again.
- A customer cannot book a space twice for the same event. **OK**

## Requirements: 
- The business can create a room with M capacity.
- The business can create events for every room.
- The business can delete a room if said room does not have any events.
- A customer can book a place for an event. 
- A customer can cancel its booking for an event. 
- A customer can see all the available public events. 

## Considerations: 
- For now, there is only one event per day. 
- Each room has a different capacity. 
- Think of each requirement as an endpoint for the API (a Django view). 

## How you’ll be evaluated in order of importance: 
- Does the project run, work and meet the requirements? 
- How well structured and high quality is your code? 
- Can you talk through your approach? 

## Extra points: 
- Throw in a couple of tests.
