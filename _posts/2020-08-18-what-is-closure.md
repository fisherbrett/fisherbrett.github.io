---
title: What is Closure in JavaScript?
date: '2020-08-18T23:46:37.121Z'
layout: post
---

I recently purchased and read the book [You Don't Know JS Yet](https://www.amazon.com/You-Dont-Know-JS-Yet-ebook/dp/B084BNMN7T/ref=sr_1_2_sspa?dchild=1&keywords=you+don%27t+know+js+yet&qid=1597812272&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyVFlYMUJaOTQ2TzY3JmVuY3J5cHRlZElkPUEwMzA3MDI4Qlo2TDdCVlMwM0xBJmVuY3J5cHRlZEFkSWQ9QTA0ODk5NDgzVVFFSE1LSjlSQ0U5JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==) by Kyle Simpson, which I found to be a great read. Even though I've worked as a JS developer for years, there were so many new things I learned by reading it (I am not endorsed by anyone affiliated with this book - I'm just recommending it because I genuinely liked it).

One of those things was "closure" - a term I had heard a couple of times but never understood what it actually meant. I think it's hard to beat Kyle Simpson's definition:

> Closure is when a function remembers and continues to access variables from outside its scope, even when the function is executed in a different scope.

So, what does that look like?

## Some Examples of Closure

You've probably already used closure before and just didn't realize it. Take the following example:

```js
function doAsyncTask(successMsg) {
  someAsyncTask().then(() => {
    console.log(`I remembered your variable! ${successMsg}`);
  });
}

getSuperImporantInfo('Hooray!');

// Some time later...
// I remembered your variable! Hooray!
```

When `someAsyncTask` finishes executing, it prints out the `successMsg` variable passed to `doAsyncTask`. `someAsyncTask` could take several seconds or even several minutes to execute, but the callback function passed to `then` "remembers" the `successMsg` variable. We say the the callback function is "closed" over `successMsg`.

I've done things like this all the time, I just didn't know I was using closure!

Now let's say you want to create a counter function. Every time you call the function, it will return the next number after the last number it returned. You can use closure to "remember" the last number returned.

```js
function createCounter() {
  let count = 0;
  return () => count++;
}

const inc = createCounter();

inc();
// 0
inc();
// 1
inc();
// 2
```

`createCounter` returns an anonymous function which has access to the `count` variable. The function returned by `createCounter` is "closed" over `count`. We can even create multiple increment functions, all of which will have their own copy of `count`.

```js
const inc1 = createCounter();
const inc2 = createCounter();

inc1();
// 0
inc2();
// 0
inc1();
// 1
inc1();
// 2
inc2();
// 1
```

These may be simple examples, but I've certainly needed to write counter functions like this before. Before I knew about closure, I would create variables visible to my entire module and increment those in my counter function. Now I know there's a better way that doesn't require me polluting my modules' scopes.

That's all there is to it! What other examples can you think of where you could use closure to your advantage?
