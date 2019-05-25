# The big why...

I don't know the Python language. I have some little experience in Java, but I don't know Python.
However, I need to learn it somehow. Somehow won't just jump out from vacuum. I decided to learn it
in form of a practice way. Thus, I need a continuous project to crystallize skills. Sure the skills
are not lying on the plane of Python programming. I define the goals in the following way:

* There should be a trivial from user perspective program/application. However, it should be
non-trivial from the programmer perspective.
* Non triviality from the programming perspective should cover the following aspects:
    - The product should implement a non-simple algorithms (matrices, trees, graphs, etc.)
    - Since it is a Python learning eventually, the product should be dependent on the 3rd. party
    libraries as less as possible. As well, it is about the usage of the language itself, i.e. it
    should not use other programming languages.
    - The product should have an understood understood well defined understood inner structure.
    It should not look like a mess.
    - The product implement some "best practices" in general. I.e. it should use loggers, unit-tests,
    "pythonic" thinking in general, and so on.
    - The product should cover some concurrency.
    - The product should use cover UI and network programming.
    - The time management should be somehow reflected. It does not say that I am going to use agile
    platforms in general but the time and feature management should be documented somehow.
    - Summarizing all above in few words, **it should be a mature programming project** that will
    help with the Python language learning and programming in general.
* It needs have some non-trivial amount of work.

# The choice
## History
I was participating in yet another boring meeting at work. The meeting was in a meeting room that
actually is a shelter by the original design. Bomb shelters are our reality. The room itself is
not only reorganized as a meeting room (i.e. it has TV sets with camera and remote meeting system
plus big table and chairs) but also, since our reality is non-synchronized holidays in kindergartens
and schools with working parents, it has some (table) games for children.
There was [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) game on the table when we had
arrived to the room. I was thinking that it would be a good exercise to code such a game.
Since I was obligated in that time to start coding in Python, a nice idea to code it completely in
Python was born. Latter the idea evolved to have (useless :-)) project which main goal is to program
in Python as much as possible.
## Project Vision
The final product is a (kind of) Connect Four game. It should have an intuitive UI.
It should be possible to choose the length of connected checkers as well as the board size.
It should be possible to play by two humans on the same computer. It should be possible to play
with a computer opponent. As well, it should be possible to play the game via a network.
There should be a history with ability to go forward or backward and/or replay. As well,
for the network mode there should be a chat.