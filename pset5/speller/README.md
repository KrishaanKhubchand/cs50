# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

An invented long word said to mean a lung disease caused by inhaling very fine ash and sand dust.


## According to its man page, what does `getrusage` do?

Returns the memory/resource usage of a thread, self, or descendants of self (functions basically).

## Per that same man page, how many members are in a variable of type `struct rusage`?

16 -- Showing operations numbers, CPU usage time, sizes of stacks, messages sent, contexts switched etc.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

No clue why...I'm guessing because we want the full thing? Or we want location as well..

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

1) Receive dictionary and text for spell check via arguments. Check if they're valid or not.
2) Declare benchmarks/starting points for resource usage and time taken to load/check etc.
3) Load dictionary and getUsage before/after, calculate diff, to see impact of dict-load. If failed, exit.
4) Open text as File pointer for reading. Check that it works.
5) Set counters. 
6) Start at the beginning of the file, iterative over every character until the end of file. 
7) Check if you have an alphabetic letter, or apostophe, then start creating word array, to be cross referenced with dict.
8) Extra check for length of word; if too long, kill it.
9) If there's a number, skip to past space to next word.
10) Once you have a word, terminate it so it becomes a checkable string.
11) Check it, with B4/After stats! 
12) For loop is done; close file, unload dict, check, calculate, and print stats.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Precision.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

We don't want to change it by mistake.
