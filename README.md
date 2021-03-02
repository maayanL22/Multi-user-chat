# Multi-user-chat
server and client of a multi user chat in python

There are 5 commands possible that are recognized by their command number:
1 - chat message
2 - manager promotion
3 - kick a user from the chat (the user to kick is recognized by his name)
4 - mute a user (the user to mute is recognized by his name)
5 - private message between users 

the protocol for doing something in the chat is as followed:
Name length - Name - Command number - Message length/Name length (of the member to promote/kick/mute/write a private message to) - Message/Name
For example: 006Maayan1005Hello

Only managers can promote/kick/mute. Names and messages are allowed to be of a max length of 999.

