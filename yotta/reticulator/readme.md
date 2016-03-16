## Reticulator

!!! TODO: this is the idea, not everything here is done yet.

Reticulator is a library for robustly transmitting messages (such as crash
reports) from command line programs to a server.

Messages are cached to disk, so that batches of messages can be sent together,
and messages which were written by one invocation of a program (perhaps during
its death throes after crashing) can be transmitted by a subsequent one,
messages are compressed for transmission, so duplicate events .

Multiple separate programs, or versions of a program, all of which use
reticulator (and which are sending data to the same server) can send each
others messages.

Reticulator tries hard not to interfere with the normal operation of programs
(it sends data in a background thread, which will not extend the lifetime of an
application).

A consistent API for asking for user permission to transmit data is provided.
You should supply a message that clearly explains the nature of the data that
you're transmitting, and a link to the privacy policy that applies to its
collection.

Reticulator provides hooks for sending messages about abnormal program
termination, but you can use reticulator to send messages about anything, such
as usage statistics.


### Data Format

Data is POSTed as JSON data:

```JSON
{
    "messages": [
        {
            // would be nice for the unique ID to be short: can we rely on
            // counting?
            "reticulatorMessageId":"<unique ID for this message>",
            "reticulatorClientId":"<uuid hex string>",
            // ... your properties here ...
        },
        // example of a default program termination message:
        {
            "reticulatorClientId":"<uuid hex string>",
            "invocation": [<sys.argv array (i.e. how the program was invoked)],
            "bactkrace": [<list of stack frames>]
        }
    ]
}
```

### A Note About Privacy

It's really easy to unintentionally collect sensitive information in error
reports and analytics. For example, even the invocation of a program that lead
to a fatal error (critical information for reproducing a bug) might include
sensitive data such as project names that identify clients.

You will be tempted to always say "why not collect analytics on X!!", and
enthusiastically go ahead with it, but each time you should carefully consider
whether the data is actually going to be useful in making your product better
for your users, or you are merely collecting it because you can.

!!! FIXME: should we have a basic level of analytics that records, for example
that errors occurred on file XXX, line YYY, and nothing else?


