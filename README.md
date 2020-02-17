# Chat-Room-Flask

## Description

I will build a group chat web application with asynchronous
Javascript and a REST API written in Python with Flask.

Watch Party lets users start new private chats that work like group texts or
Slack rooms. A user creates a new chat, which is assigned a unique identifier.
They can invite up to 5 other users by sharing a unique link that will
authenticate the bearer to the chat. Users in a chat post messages which appear
in a single conversation thread to all users. Unlike Slack or a group chat,
Watch Party only saves or shows the last 30 messages.

Implemented the UI for Watch Party in HTML, CSS, and Javascript, and serveed it
using server-side code written in the latest stable version of Python
(3.8.1)
and Flask. 

It has features like:


- Prompt users to enter a username when they create or join a chat.
Give each chat a unique URL so users can return to it if they close their
tab or reload the page. Remember who they are if they do (hint: use
Window.localStorage)
- Allow users to be in multiple chats in multiple tabs if they want (hint: scope
storage and session tokens to chat id).
- Redirect users to the home screen if the chat they're trying to join already
has 6 users in it.
- As other users type new messages in a chat, Watch Party should asynchronously
fetch them, and those messages should appear automatically without anyone
reloading the page.
- Make sure chat messages support Unicode characters


Watch Party can be visually very simple, but should render responsively on
desktops and on mobile. Make sure the message input for for a chat is always on
the screen regardless of where the user scrolls. Chats are intended to be
ephemeral and are not saved to a database or the filesystem (ie it's ok for them
just to exist in memory on the web server). For the purposes of this Exercise,
you do not need to worry about garbage collecting chats that are not in use.

Also using Python and Flask, write a REST API for creating and hosting live
Watch Party group chats. It should support the following methods:



POST /create: Allow any user to create a new chat. Return a unique identifier
chat_idand a session_token to allow the original creator to identify
themselves in subsequent requests. All session tokens should expire within 6
hours.

- POST /<chat_id>/invite: Take chat_id as a URL param and require that
chat's creator's session_token in an authorization header.  Generate a
"magic link" that, when visited, loads the Watch Party web application,
prompts the new user for a username and authenticates them by giving them a
session_token, and displays the chat's page.

- GET /<chat_id>: Require a valid session_token in an authorization header.
Return the messages in the chat. Optionally take a parameter that allows it to
return only new messages.

- POST /<chat_id>: Require a valid session_token in an authorization header.
Post a new message to the chat.
Your web application should use these API methods. Feel free to include any
other methods you think will be useful, either as web controllers or as further
API endpoints. You can use any other libraries or frameworks you find useful, as
well.

Watch Party (though it has somewhat different
requirements) is inspired by yap.chat.
