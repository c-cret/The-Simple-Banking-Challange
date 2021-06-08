# The-Simple-Banking-Challange

The goal is to develop a simple ATM-application that supports the following commands:

- **login [user] [pin]** 
    - Creates a new user session
- **logout**
    - Disposes the current user session
- **get balance**
    - Displays the current balance
- **withdraw [amount]**
    - Withdraw the specified amount of money from the account
- **deposit [amount]** 
    - Deposits the specified amount of money to the account
- **transfer [amount] to [user]** 
    - Transfers the specified amount of money from the current user to the specified one
- **history (optional)**
    - Displays the account history

You are free to tweak the commands above as you see fit as long as the basic functionality remains the same. Note that the history function is an optional enhancement.

### Requirements
- All account data must be saved in persistent storage (e.g. filesystem).
- The persistence model must be append only
    - (i.e. only read and appending writes, no modifications are allowed).
- The application must expose its services over at least one remote interface (e.g. HTTP, TCP or UDP) besides the ordinary console interface.
- The application can be implemented in any language as long as it is portable.

### Example run 
A sample run of the program might look like this:

```$login ola 123
Welcome, ola
$get balance
0 
$deposit 100
ok!
$get balance
100
$withdraw 25
ok!
$get balance
75
```
